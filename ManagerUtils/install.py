def Install(cmd, path, reinstall=False, debug=False): #Baixa pacotes
    import os
    import requests
    import tqdm
    from colorama import Fore
    
    if debug == True: #Ativa debug caso esteja especificado
        import logging
        import http.client
        http.client.HTTPConnection.debuglevel = 1
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True
    
    
    if reinstall != True:
        print(Fore.BLUE + "Preparando download...", end='\r')
    else:
        try:
            import shutil
            print(Fore.BLUE + "Preparando reinstalação...", end='\r')
            downpath = checkpath(path, cmd) #Checando o diretório de download do pacote
            checkinstall(cmd, downpath, reinstall=True) #Checa se o pacote está instalado
            shutil.rmtree(downpath) #Removendo pacote
            print("Pacote desinstalado, começando instalação", end='\r')
        except IOError:
            print(Fore.RED); esc = input("O pacote selecionado não está baixado. Deseja baixa-lo? (Y/N) ").lower()
            if esc == 'y':
                print(Fore.BLUE, end='')
                pass
            else:
                return
    
    try:
        host = checkhost(path) #Checando o host
        server = checkserver(path) #Checando o server
        branch = checkbranch(path) #Checando a branch
        repo = checkrepo(cmd, path, host, branch, server) #Checando o repositório do pacote
        package = checkpackage(cmd, repo, host, branch, server) #Checando o pacote que o usuarío deseja instalar
        downpath = checkpath(path, package) #Checando o diretório de download do pacote
        checkinstall(cmd, downpath) #Checa se o pacote já está instalado
        target = checktarget() #Checa a plataforma do pacote
        packageversion = checkversion(cmd, repo, target, path, host, server, branch) #Checa a versão do pacote
        bartotal = checkcontentlength(repo,package,target,packageversion,host,server,branch,packageversion) #Pegando o content-lenght
    except ValueError: #Caso o repositório não exista
        print(Fore.RED + "\033[KO repositório selecionado não existe"); return
    except NameError: #Caso o pacote não exista 
        print(Fore.RED + "\033[KO pacote selecionado não existe"); return
    except EOFError: #Caso a versão não exista
        print(Fore.RED + "\033[KA versão selecionada do pacote não existe"); return
    except IOError:
        print(Fore.RED + "\033[KO pacote já está instalado. Caso deseje reinstalar ele, use o comando \"reinstall\""); return
    
    print('\033[KIniciando download...' + Fore.RESET)
    os.mkdir(downpath)
    try:
        final_link = f'https://github.com/{host}/{server}/blob/{branch}/{repo}/{package}/bin/{target}-{package}-{packageversion}.zip?raw=true'
        request = requests.get(final_link, stream=True) #Fazendo get para o zip com o arquivo para baixar
        if request.status_code != 200:
            raise ValueError
    except:
        lasthope = checkmirror(path, host, server, branch, repo, package, packageversion, target)
        if lasthope == None: 
            return
        else:
            request = requests.get(lasthope)
            
    ########################################
    
    description = Fore.BLUE + f'Baixando "{target}-{package}-{packageversion}"'
    with open(f'{downpath}/{package}-{packageversion}.zip', 'wb') as file, tqdm.tqdm(desc=description, total=bartotal, unit_scale=True, unit_divisor=1024) as loadbar:
        for data in request.iter_content(chunk_size=1024):
            loadbar.update(len(data))
            file.write(data)
        loadbar.close()
     
    bartotal = 0 #Contagem de arquivos no zip
    zipitens = [] #Items no zip
    from zipfile import ZipFile #Importa livraria zip
    with ZipFile(f'{downpath}/{package}-{packageversion}.zip', 'r') as zip: #Abrindo zip no with
        for i in zip.namelist(): #Para cada item no zip
            bartotal = bartotal + 1 #Aumenta a contagem de arquivos
            zipitens.append(i) #Coloca na array zipitens
        with tqdm.tqdm(desc="Extraindo arquivo", total=bartotal, unit='arquivos') as loadbar: #Iniciando barra de load
            for i in zipitens: #Para cada item no zip
                zip.extract(i, path=downpath) #Descompactar
                loadbar.update(1) #Atualizar a barra
            loadbar.close()
         
    ########################################
           
    print(Fore.BLUE + "Finalizando download...", end='\r') #Passos finais na finalização do download
    
    os.remove(f'{downpath}/{package}-{packageversion}.zip') #Removendo .zip
    
    line_choice = checkline(path) #Pegando onde deve escrever as novas linhas e etc

    #if target == 'win':
    #    finalizer = '\r\n'
    #else:
    #    finalizer = '\n'

    if reinstall == True:
        with open(f'{path}/ManagerFiles/Bin/install2.bin', 'r+') as f:
            leitura = f.readlines()
            f.seek(0)
            for i in leitura:
                if i.startswith(f'{package} ') == False and i != '\n':
                    f.write(i)
            f.truncate()
            
    with open(f'{path}/ManagerFiles/Bin/install2.bin', 'a') as f: #Abrndo arquivo em append
        f.write(f'{package} = {host}||{server}||{branch}||{repo}||{target}||{packageversion}||{downpath} \n') #Atualizando linhas

    if debug == True:
        http.client.HTTPConnection.debuglevel = 0

    print(Fore.BLUE + f"Download concluido! Salvo em \"{downpath}\"")

#################################
######FUNÇÕES DE CHECAGEM
#################################

def checkhost(path):
    import configparser
    print('\033[KChecando host...', end='\r')
    config = configparser.ConfigParser()
    config.read(f'{path}/ManagerFiles/config.ini')
    return config.get('Version', 'host')

def checkbranch(path):
    import configparser
    print('\033[KChecando branch...', end='\r')
    config = configparser.ConfigParser()
    config.read(f'{path}/ManagerFiles/config.ini')
    return config.get('Version', 'branch')

def checkserver(path):
    import configparser
    print('\033[KChecando servidor...', end='\r')
    config = configparser.ConfigParser()
    config.read(f'{path}/ManagerFiles/config.ini')
    return config.get('Version', 'server')

def checkrepo(cmd, path, host, branch, server): #Checa se o repositório existe
    import requests
    
    print('\033[KChecando repositório...', end='\r')
    
    if '-' in cmd: #Se o usuario especificar o repositório do pacote
        if cmd.count('-') == 1:
            repo, cmd = cmd.split('-') #Separar o pacote e o repositório
        else:
            repo, cmd, version = cmd.split('-')
        
    else: #Caso o contrario, pega o repositório definido pelo setrepo (ou definido por padrão)
        import configparser
        config = configparser.ConfigParser()
        config.read(f'{path}/ManagerFiles/config.ini')
        repo = config.get('Version', 'repo')
    
    try: #Testa pra ver se o repositório existe ou não
        request = requests.head(f'https://github.com/{host}/{server}/tree/{branch}/{repo}') 
        if request.status_code != 200:
            raise ValueError
        else:
            return repo
    except ValueError:
        raise
 
def checkpackage(cmd, repo, host, branch, server): #Checa se o pacote existe
    import requests
    
    print('\033[KChecando pacote...', end='\r')
    
    if '-' in cmd: #Se o usuario especificar o repositório do pacote
        if cmd.count('-') == 1:
            repo, cmd = cmd.split('-') #Separar o pacote e o repositório
        else:
            repo, cmd, version = cmd.split('-')
    
    request = requests.head(f'https://github.com/{host}/{server}/tree/{branch}/{repo}/{cmd}')
    try:
        if request.status_code != 200:
            raise NameError
        else:
            return cmd
    except NameError:
        raise
    
               
def checkpath(path, package): #Checa o diretório para baixar o pacote
    import configparser, os
    
    print('\033[KChecando diretório de download...', end='\r')
    
    config = configparser.ConfigParser()
    config.read(f'{path}/ManagerFiles/config.ini')
    
    downpath = config.get('Global', 'downpath')
    
    if downpath == 'null': #Se downpath for null
        downpath = f'{path}/ManagerFiles/Downloads/{package}' 
    else:
        downpath = ''.join([f'{downpath}', '/' ,f'{package}'])
    return downpath #Retorna o diretório de download

def checkversion(cmd, repo, target, path, host, server, branch):
    import requests, os
    
    print('\033[KChecando versão...', end='\r')
    
    found = False
    specified = False
    
    if '-' in cmd:
        if cmd.count('-') == 1:
            repo, cmd = cmd.split('-')
        elif cmd.count('-') == 2: #Se tiver um traço no comando
            repo, cmd, version = cmd.split('-') #Divide o comando em "repositório-pacote-versão"
            specified = True
    
    request = requests.get(f'https://raw.githubusercontent.com/{host}/{server}/{branch}/{repo}/{cmd}/versions.txt')
    with open(f'{path}/ManagerFiles/Cache/version.cache', 'wb') as f:
        f.write(request.content)
    with open(f'{path}/ManagerFiles/Cache/version.cache', 'r') as f:
        leitura = f.read()
        leitura = leitura.split('\n')
        for i in leitura:
            if specified == False:
                if i.startswith('current_global = '): #Pegando release global
                    version = i.replace('current_global = ', ''); found = True; break
                elif i.startswith('current_win = ') and target == 'win': #Pegando release windows   
                    version = i.replace('current_win = ', ''); found = True; break
                elif i.startswith('current_linux = ') and target == 'linux': #Pegando release linux
                    version = i.replace('current_linux = ', ''); found = True; break
            else:
                if i == version:
                    found = True; break
                
        try:
            if found == True:
                return version
            else:
                raise EOFError
        except EOFError:
            raise
                    
            
def checktarget():
    import platform
    
    print('\033[KChecando plataforma...', end='\r')
    
    if platform.system().startswith('W'): #Checando a plataforma do usuario
        return 'win'
    else:
        return 'linux'
    
def checkcontentlength(repo, package, target, packageversion, host, server, branch, version):
    import requests
    
    print('\033[KChecando tamanho do arquivo...', end='\r')
    
    link = f'https://raw.githubusercontent.com/{host}/{server}/{branch}/{repo}/{package}/bin/{target}-{package}-{version}'
    request = requests.head(link)
    return int(request.headers.get('content-length', 0))

def checkinstall(cmd, downpath, reinstall=False):
    import os
    
    print('\033[KChecando instalação do pacote...', end='\r')
    
    try:
        if reinstall == False:
            if os.path.isdir(downpath) == True:
                raise IOError
        else:
            if os.path.isdir(downpath) == False:
                raise IOError
    except IOError:
        raise
    
def checkmirror(path, host, server, branch, repo, package, packageversion, target):
    import requests
    from colorama import Fore
    
    print(Fore.BLUE + "Arquivo não encontrado, procurando mirror...")
    
    found = False
    request = requests.get(f'https://raw.githubusercontent.com/{host}/{server}/{branch}/{repo}/{package}/bin/mirrors.txt')
    with open(f'{path}/ManagerFiles/Cache/mirrors.cache', 'wb') as f:
        f.write(request.content)
    with open(f'{path}/ManagerFiles/Cache/mirrors.cache', 'r') as f:
        leitura = f.read()
        leitura = leitura.split('\n')
        for i in leitura:
            if i.startswith(f'{target}-{package}-{packageversion}') and '=' in i:
                cmd, downlink = i.split('=')
                if ' ' in downlink:
                    downlink = downlink.replace(' ', '')
                found = True
                break
        if found == True:
            return downlink
        else:
            print(Fore.RED + "Não foi possível obter o pacote selecionado")
            return None
        
def checkline(path):
    import configparser
    config = configparser.ConfigParser()
    config.read(f'{path}/ManagerFiles/config.ini')
    
    lines = config.get('Global', 'line_choice')
    return lines

def checkline2(path, linecount):
    import configparser
    config = configparser.ConfigParser()
    config.read(f'{path}/ManagerFiles/config.ini')
    
    linecount = str(linecount)
    config.set('Global', 'line_choice', linecount)
    with open(f'{path}/ManagerFiles/config.ini', 'w') as f:
        config.write(f)