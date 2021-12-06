print("Iniciando MaidUtils...", end='\r')

from colorama import Fore, init
import configparser
import os, platform
import socket

path = os.path.dirname(os.path.realpath(__file__))
if platform.system().startswith('W'):
    path = path.replace('\\', '/')
init()

if os.path.isfile(f'{path}/ManagerFiles/config.ini') == False:
    from genconfig import genconfig
    genconfig(path)

config = configparser.ConfigParser(allow_no_value=True)
config.read(f'{path}/ManagerFiles/config.ini')
version = config.get('Version', 'version') #Versão do MaidUtils 

#################################################################################

print(Fore.BLUE + "\033[KMaidUtils v{}".format(version)) #Mostrando versão da maidutils
print("Para uma lista de comandos, digite \"MaidUtils guide\"" + Fore.CYAN)

while True: #Pega input do usuario
    print(Fore.CYAN + 'Input ' + Fore.RESET + '>>' + Fore.CYAN, end=' ') #Gambiarra pra deixar a shell bonita
    cmd = input().lower()
    if cmd.startswith('maidutils'): #Remove o maidutils do começo (se tiver)
        cmd = cmd.replace('maidutils ', '')
    if ' ' in cmd: #Se o cmd tiver um espaço, separa em cmd1 e cmd2
        try:
            cmd, cmd2 = cmd.split(' ')
        except:
            print(Fore.RED + "Comando inválido")
    
    if cmd == 'install': #Instalar pacotes
        from ManagerUtils.install import Install
        try:
            Install(cmd2, path)
        except PermissionError:
            print(Fore.RED + "\033[KNão há permissão o suficiente para baixar o pacote. Reinicie o manager como admin/su e tente novamente")
            
    elif cmd == 'analyze': #Pegar descrição de pacotes
        from ManagerUtils.analyze import Analyze
        try:
            Analyze(cmd2, path)
        except NameError:
            print(Fore.RED + "Argumento faltando: Pacote")

    elif cmd == 'guide':
        from ManagerUtils.guide import Guide
        Guide(path)

    elif cmd == 'exit': #Fecha a maidutils
        import sys
        print(Fore.BLUE + "Encerrando MaidUtils...")
        sys.exit()
    
    elif cmd == 'setrepo':
        from ManagerUtils.setconfigs import Setrepo
        try:
            Setrepo(cmd2, path)
        except NameError:
            print(Fore.RED + "Argumento faltando: Repositório")
    
    elif cmd == 'sethost':
        from ManagerUtils.setconfigs import Sethost
        try:
            Sethost(cmd2, path)
        except NameError:
            print(Fore.RED + "Argumento faltando: Host")
    
    elif cmd == 'setserver':
        from ManagerUtils.setconfigs import Setserver
        try:
            Setserver(cmd2, path)
        except NameError:
            print(Fore.RED + "Argumento faltando: Servidor")
    
    elif cmd == 'setbranch':
        from ManagerUtils.setconfigs import Setbranch
        try:
            Setbranch(cmd2, path)
        except NameError:
            print(Fore.RED + "Argumento faltando: Branch")
    
    elif cmd == 'admin':
        from ManagerUtils.admin import Admin
        Admin()
        
    elif cmd == 'uninstall':
        from ManagerUtils.uninstall import Uninstall
        try:
            Uninstall(cmd2, path)
        except PermissionError:
            print(Fore.RED + "\033[KNão há permissão o suficiente para desinstalar o pacote. Reinicie o manager como admin/su e tente novamente")
    
    else:
        print(Fore.RED + "Comando inválido")