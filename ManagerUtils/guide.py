def Guide(path):
    import os
    
    print('''
Host, server, etc:

Como esse gerenciador funciona através de repositórios do github, é necessário que o usuarío coloque as
informações corretas para conseguir baixar os pacotes.

Host - O dono do repositório no github
Servidor - O repositório do github que contém os pacotes
Branch - A branch de onde será puxada os pacotes (EX: main, master...)
Repositório - A pasta de onde os pacotes serão puxados

A seguir se encontra uma representação de como isso funciona em ação:
"https://github.com/{host}/{servidor}/tree/{branch}/{repositório}/{pacote}"
"https://github.com/polarfill/maidutilsmodules/tree/main/testrepo/testpackage"

-------------------------------------------------------

Comandos:

{} = Argumento obrigatório
[] = Argumento opcional

install[debug] {pacote} - Baixa o pacote desejado
reinstall[debug] {pacote} - Reinstala o pacote desejado 
upgrade[debug] {pacote} - Atualiza o pacote desejado
uninstall {pacote} - Desinstala o pacote desejado

analyze {pacote} - Exibe uma descrição do pacote
dir [repo] - Exibe os pacotes disponiveis em um repositório
dir-repo [server] - Exibe os repositórios disponíveis em um server
list - Exibe todos os pacotes baixados e suas versões
list-all - Exibe todas as informações sobre os pacotes baixados (repo, host, server...) 

sethost {host} - Muda o host padrão
setserver {servidor} - Muda o servidor padrão
setbranch {branch} - Muda a branch padrão
setrepo {repositório} - Muda o repositório padrão

clear - Limpa a tela
restart - Reinicia o gerenciador
exit - Fecha o gerenciador
''')
#clone {pacote} - Baixa a source do pacote (caso esteja disponível)