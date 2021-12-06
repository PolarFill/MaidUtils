def Guide(path):
    import os
    
    print('''
Comandos:

install {pacote} - Baixa o pacote desejado
uninstall {pacote} - Desinstala o pacote desejado
clone {pacote} - Baixa a source do pacote (caso esteja disponível)
analyze {pacote} - Exibe uma descrição do pacote

sethost {host} - Muda o host padrão
setserver {servidor} - Muda o servidor padrão
setbranch {branch} - Muda a branch padrão
setrepo {repositório} - Muda o repositório padrão

exit - Fecha o gerenciador
restart - Reinicia o gerenciador

-------------------------------------------------------

Host, server, etc

Como esse gerenciador funciona através de repositórios do github, é necessário que o usuarío coloque as
informações corretas para conseguir baixar os pacotes.

Host - O dono do repositório no github
Servidor - O repositório do github que contém os pacotes
Branch - A branch de onde será puxada os pacotes (EX: main, master...)
Repositório - A pasta de onde os pacotes serão puxados

A seguir se encontra uma representação de como isso funciona em ação:
"https://github.com/{host}/{servidor}/tree/{branch}/{repositório}/{pacote}"
"https://github.com/polarfill/maidutilsmodules/tree/main/testrepo/testpackage"
''')