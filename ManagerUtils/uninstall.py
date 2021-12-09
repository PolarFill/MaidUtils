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
        print(Fore.RED + "\033[KO diretório do pacote selecionado não foi encontrado")
        return
    else:
        import shutil
        shutil.rmtree(downpath)
        
        with open(f'{path}/ManagerFiles/Bin/install2.bin', 'r+') as f:
            leitura = f.readlines()
            f.seek(0)
            for i in leitura:
                if i.startswith(f'{cmd} ') == False:
                    f.write(i)
            f.truncate()
        
        print("\033[KPacote desinstalado com sucesso")