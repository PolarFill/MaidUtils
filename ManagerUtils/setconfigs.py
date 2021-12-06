def Setrepo(cmd, path): #Muda o repositório padrão
    import configparser
    import requests
    from colorama import Fore
    
    print(Fore.BLUE + "Analizando repositório...", end='\r')
    
    config = configparser.ConfigParser()
    config.read(f'{path}/ManagerFiles/config.ini')
    
    branch = config.get('Version', 'branch')
    server = config.get('Version', 'server')
    host = config.get('Version', 'host')
    old_repo = config.get('Version', 'repo')
    
    if old_repo == cmd:
        print(Fore.RED + "O repositório selecionado já está definido como padrão")
        del old_repo
        return
    
    request = requests.get(f'https://github.com/{host}/{server}/tree/{branch}/{cmd}')
    if request.status_code == 200:
        config.set('Version', 'repo', cmd)
        with open(f'{path}/ManagerFiles/config.ini', 'w') as f:
            config.write(f)
        print(f"\033[KRepositório mudado de \"{old_repo}\" para \"{cmd}\"")
    else:
        print(Fore.RED + f"\033[KO repositório selecionado não existe")
    del old_repo
    
    
def Sethost(cmd, path): #Muda o host padrão
    import configparser
    import requests
    from colorama import Fore
    
    print(Fore.BLUE + "Analizando host...", end='\r')
    
    config = configparser.ConfigParser()
    config.read(f'{path}/ManagerFiles/config.ini')
    old_host = config.get('Version', 'host')
    
    if old_host == cmd:
        print(Fore.RED + "O host selecionado já está definido como padrão")
        del old_host
        return
    
    request = requests.get(f'https://github.com/{cmd}')
    if request.status_code == 200:
        config.set('Version', 'host', cmd)
        with open(f'{path}/ManagerFiles/config.ini', 'w') as f:
            config.write(f)
        print(f"\033[KHost mudado de \"{old_host}\" para \"{cmd}\"")
    else:
        print(Fore.RED + f"\033[KO host selecionado não existe")
    del old_host
    
    
def Setserver(cmd, path): #Muda o server padrão
    import configparser
    import requests
    from colorama import Fore
    
    print(Fore.BLUE + "Analizando servidor...", end='\r')
    
    config = configparser.ConfigParser()
    config.read(f'{path}/ManagerFiles/config.ini')
    host = config.get('Version', 'host')
    old_server = config.get('Version', 'server')
    
    if old_server == cmd:
        print(Fore.RED + "O servidor selecionado já está definido como padrão")
        del old_server
        return
    
    request = requests.get(f'https://github.com/{host}/{cmd}')
    if request.status_code == 200:
        config.set('Version', 'server', cmd)
        with open(f'{path}/ManagerFiles/config.ini', 'w') as f:
            config.write(f)
        print(f"\033[KServidor mudado de \"{old_server}\" para \"{cmd}\"")
    else:
        print(Fore.RED + f"\033[KO servidor selecionado não existe")
    del old_server
    
def Setbranch(cmd, path): #Muda o server padrão
    import configparser
    import requests
    from colorama import Fore
    
    print(Fore.BLUE + "Analizando branch...", end='\r')
    
    config = configparser.ConfigParser()
    config.read(f'{path}/ManagerFiles/config.ini')
    host = config.get('Version', 'host')
    server = config.get('Version', 'server')
    old_branch = config.get('Version', 'branch')
    
    if old_branch == cmd:
        print(Fore.RED + "A branch selecionada já está definida como padrão")
        del old_branch
        return
    
    request = requests.get(f'https://github.com/{host}/{server}/tree/{cmd}')
    if request.status_code == 200:
        config.set('Version', 'branch', cmd)
        with open(f'{path}/ManagerFiles/config.ini', 'w') as f:
            config.write(f)
        print(f"\033[KBranch mudada de \"{old_branch}\" para \"{cmd}\"")
    else:
        print(Fore.RED + f"\033[KA branch selecionada não existe")
    del old_branch