def Uninstall(cmd, path):
    import os
    import configparser
    from colorama import Fore
    
    print(Fore.BLUE + f'Desinstalando pacote {cmd}...', end='\r')
    
    config = configparser.ConfigParser()
    config.read(f'{path}/ManagerFiles/config.ini')
    downpath = config.get('Global', 'downpath')
    
    if downpath == 'null':                                  #Se downpath for null
        downpath = f'{path}/ManagerFiles/Downloads/{cmd}'   #Diretório padrão será utilizado
    else:                                                   #Caso o contrario
        downpath = ''.join([f'{downpath}', '/' ,f'{cmd}'])  #Junta o diretório de download com o do pacote
        
    if os.path.isdir(downpath) == False:
        print(Fore.RED + "\033[KO pacote selecionado não está baixado")
        return
    else:
        import shutil
        shutil.rmtree(downpath)
        print("\033[KPacote desinstalado com sucesso")