def Analyze(cmd, path):
    import requests, base64, re, codecs
    from colorama import Fore, init
    init()
    
    if '-' in cmd: #Se o usuario especificar o repositório do pacote
        repo, cmd = cmd.split('-') #Separar o pacote e o repositório
    else: #Caso o contrario, pega o repositório definido pelo setrepo (ou definido por padrão)
        import configparser
        config = configparser.ConfigParser()
        config.read(f'{path}/ManagerFiles/config.ini')
        repo = config.get('Version', 'repo')
        
    check = requests.get(f'https://github.com/Polarfill/MaidUtilsModules/tree/main/{repo}') #Checa se o repositório existe
    if check.status_code != 200: #Se não existe, avisa o usuarío
        print(Fore.RED + "O repositório selecionado não existe")
    else: #Caso o contrarío, continua
        try:
            response = requests.get(f'https://api.github.com/repos/Polarfill/MaidUtilsModules/contents/{repo}/{cmd}/description.txt')
            content = response.json()["content"]
            decoded_content = str(base64.b64decode(content))
        except KeyError: #Se o pacote não existir (header content não existe) dá um erro
            print(Fore.RED + "O pacote selecionado não existe")
            return
        
        escape_sequences = re.compile(r'''
                                    ( \\U........
                                    | \\u....
                                    | \\x..
                                    | \\[0-7]{1,3}
                                    | \\N\{[^}]+\}
                                    | \\[\\'"abfnrtv]
                                    )''', re.UNICODE | re.VERBOSE) 
        #Pega os escape codes. Para mais detalhes, leia https://stackoverflow.com/questions/4020539/process-escape-sequences-in-a-string-in-python

        def decode_escapes(s):  #Função chamada para decodificar os escape codes
            def decode_match(match): #Função chamada para pegar o match
                return codecs.decode(match.group(0), 'unicode-escape') #Decodificando
            return escape_sequences.sub(decode_match, s) #Substituindo strings         
        
        print(Fore.BLUE + f"Descrição do pacote {cmd}:")
        print('')
        print(decode_escapes(decoded_content) + Fore.RESET)
