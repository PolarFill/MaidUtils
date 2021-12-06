def genconfig(path):
    import configparser, platform, os
    config = configparser.ConfigParser(allow_no_value=True)

    if platform.system() == 'Windows': #Determinando plataforma para atualizar a maidutils depois
        target = 'win'
    else:
        target = 'linux'

    if os.path.isdir(f'{path}/ManagerFiles') == False:
        os.mkdir(f'{path}/ManagerFiles')
        
    if os.path.isdir(f'{path}/ManagerFiles/Downloads') == False:
        os.mkdir(f'{path}/ManagerFiles/Downloads')
        
    if os.path.isdir(f'{path}/ManagerFiles/Cache') == False:
        os.mkdir(f'{path}/ManagerFiles/Cache')

    config['Version'] = {
        'version': '1.0',
        'target': f'{target}',
        'branch': '',
        'repo': '',
        'server': '',
        'host': ''
    }
    config['Global'] = {
        'downpath': 'null',
    }
    #config['Preferences'] = {
    #    'no-prefix': 'true'
    #}
    with open(f'{path}/ManagerFiles/config.ini', 'w') as configfile:
        config.write(configfile)