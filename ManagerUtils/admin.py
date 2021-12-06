def Admin():
    import platform
    from colorama import Fore
    
    if platform.system() != "Windows":
        print(Fore.RED + "Esse comando só é compatível com sistemas Windows")
        
    import ctypes, sys
    check_admin = ctypes.windll.shell32.IsUserAnAdmin() #Checando se o usuario atual é admin usando ctypes
    if check_admin == 0:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1) #Reinicia a maid se n tiver adm
        exit()
    else:
        print(Fore.RED + "O manager já está sendo executado com administrador")