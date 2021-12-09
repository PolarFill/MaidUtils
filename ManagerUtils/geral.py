def List(path): #Lista pacotes
    from colorama import Fore #Cor
    import tabulate #Cria tabela
    import os

    print(Fore.BLUE + "Analizando pacotes...", end='\r')
    
    if os.path.isfile(f'{path}/ManagerFiles/Bin/install2.bin') == True: #Checa se algum pacote foi instalado
        with open(f'{path}/ManagerFiles/Bin/install2.bin', 'r') as f: #Se for, abre o arquivo de descrição deles
            leitura = f.read() 
            leitura = leitura.split('\n') #Separa linhas
            
            versions = [] #Array de versões
            packages = [] #Array de pacotes
            for i in leitura: #Para cada item em leitura
                if '=' in i: #Se tiver um = no i
                    package, resto = i.split('=') #Separa em pacote e versão
                    host, server, branch, repo, target, version, downpath = resto.split('||')
                    packages.append(package) #Coloca versão na array de versão
                    versions.append(version) #Coloca pacote na array de pacote
             
            final_result = {"Pacotes": packages, "Versões": versions} #Coloca em um dicionario
            table = tabulate.tabulate(final_result, headers="keys", tablefmt="presto") #Cria uma tabela com o dicionario como argumento
            print(table) #Mostra a tabela
    else:
        print(Fore.RED + "Nenhum pacote foi instalado pela MaidUtils")
        return
       
########################################################
                
def Dir(path, cmd2=None, repos=False):
    from colorama import Fore
    import requests
    import configparser
    
    print(Fore.BLUE + "Analizando pacotes...", end='\r')
    
    config = configparser.ConfigParser()
    config.read(f'{path}/ManagerFiles/config.ini')
    
    host = config.get('Version', 'host')
    server = config.get('Version', 'server')

    if cmd2 == None:
        if repos == True:
            server = config.get('Version', 'server')
        else:
            repo = config.get('Version', 'repo')
    else:
        if repos == True:
            server = cmd2
        else:
            repo = cmd2
    
    try:
        if repos == False:
            request = requests.get(f'https://api.github.com/repos/{host}/{server}/contents/{repo}')
        else:
            request = requests.get(f'https://api.github.com/repos/{host}/{server}/contents/')
    except:
        print(Fore.RED + "O repositório selecionado não existe"); return
    
    index = 0
    packages = []
    while True:
        try:
            package = request.json()[index]['name']
            packages.append(package)
            index = index + 1
        except IndexError:
            break
        except KeyError:
            if repos == False:
                print(Fore.RED + "O repositório selecionado não existe"); return
            else:
                print(Fore.RED + "O servidor selecionado não existe"); return
    
    if repos == False:
        print(f'\033[KPacotes disponíveis no repositório {repo}:')
    else:
        print(f'\033[KRepositórios disponíveis no servidor {server}:')
    for i in packages:
        print(i)
    del host, server, index, packages
    if repos == False:
        del repo
    del repos
   
########################################################
        
def Listall(path):
    from colorama import Fore #Cor
    import tabulate #Cria tabela
    import os

    print(Fore.BLUE + "Analizando pacotes...", end='\r')
    
    if os.path.isfile(f'{path}/ManagerFiles/Bin/install2.bin') == True: #Checa se algum pacote foi instalado
        with open(f'{path}/ManagerFiles/Bin/install2.bin', 'r') as f:
            leitura = f.read()
            leitura = leitura.split('\n')
            
            packages = []
            versions = []
            targets = []
            hosts = []
            servers = []
            branchs = []
            repos = []
            downpaths = []
            for i in leitura:
                if '=' in i:
                    package, resto = i.split('=')
                    host, server, branch, repo, target, packageversion, downpath = resto.split('||')
                    packages.append(package)
                    versions.append(packageversion)
                    hosts.append(host)
                    servers.append(server)
                    branchs.append(branch)
                    repos.append(repo)
                    targets.append(target)
                    downpaths.append(downpath)
                
            final_result = {"Pacotes": packages, "Versões": versions, "Plataformas": targets, 
                            "Hosts": hosts, "Servers": servers, "Branchs": branchs, 'Repos': repos, 'Diretórios de download': downpaths}
            
            table = tabulate.tabulate(final_result, headers="keys", tablefmt="presto") #Cria uma tabela com o dicionario como argumento
            print(table) #Mostra a tabela
    else:
        print(Fore.RED + "Nenhum pacote foi instalado pela MaidUtils")
        return