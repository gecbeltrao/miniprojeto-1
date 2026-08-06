"""Menu interativo no terminal.

Uso: python cli.py catalogo_final.json
"""

from catalogo import Catalogo
catalogo = Catalogo("catalogo_final.json")

def terminal():
    while True:
        print("Trilha sonora")
        print("============")
        print("1. Listar todos os usuários")
        print("2. Ver playlist completa de um usuário")
        print("3. Conteúdo na posição N da playlist")
        print("4. Interseção de playlists (N usuários)")
        print("5. Dados de um conteúdo (rating, duração, gêneros, plataformas, data, execuções)")
        print("6. Conteúdos de um gênero")
        print("7. Enfileirar conteúdo na fila de reprodução")
        print("8. Tocar próximo da fila")
        print("9. Ver fila atual")
        print("0. Sair")
        op = int(input("Digite sua opção: "))
        match op:
            case 1:
                print(catalogo.listar_usuarios())
            case 2:
                nome = input("Digite o nome do usuário: ")
                usuario_id = catalogo.buscar_usuario_por_nome(nome)
                if usuario_id is None:
                    print(f"Usuário {nome} não encontrado.")
                else:
                    playlist = catalogo.playlist_de(usuario_id)
                    for i, conteudo_id in enumerate(playlist):
                        print(f"{i+1}. {catalogo.titulo_de(conteudo_id)}")
            case 3:
                nome = input("Digite o nome do usuário: ")
                usuario_id = catalogo.buscar_usuario_por_nome(nome)
                if usuario_id is None:
                    print(f"Usuário {nome} não encontrado.")
                else:
                    posicao = int(input("Digite a posição (1 a N): ")) - 1
                    conteudo_id = catalogo.conteudo_na_posicao(usuario_id, posicao)
                    if conteudo_id is None:
                        print(f"Posição {posicao + 1} inválida para o usuário {nome}.")
                    else:
                        print(conteudo_id)
            case 4:
                nomes = input("Digite os nomes dos usuários separados por vírgula: ").split(",")
                usuario_ids = []
                for nome in nomes:
                    usuario_id = catalogo.buscar_usuario_por_nome(nome.strip())
                    if usuario_id is None:
                        print(f"Usuário {nome.strip()} não encontrado.")
                    else:
                        usuario_ids.append(usuario_id)
                if len(usuario_ids) > 0:
                    print(catalogo.intersecao_playlists(usuario_ids))
            case 5:
                conteudo_id = input("Digite o ID do conteúdo: ")
                rating = catalogo.rating_de(conteudo_id)
                duracao = catalogo.duracao_total_de(conteudo_id)
                generos = catalogo.generos_de(conteudo_id)
                plataformas = catalogo.plataformas_de(conteudo_id)
                data_adicionado = catalogo.data_adicionado_de(conteudo_id)
                execucoes = catalogo.execucoes_de(conteudo_id)
                print(f"Rating: {rating}")
                print(f"Duração: {duracao} segundos")
                print(f"Gêneros: {generos}")
                print(f"Plataformas: {plataformas}")
                print(f"Data adicionado: {data_adicionado}")
                print(f"Execuções: {execucoes}")
            case 6:
                genero = input("Digite o gênero: ")
                print(catalogo.conteudos_do_genero(genero))
            case 7:
                conteudo_id = input("Digite o ID do conteúdo: ")
                if catalogo.enfileirar(conteudo_id):
                    print(f"Conteúdo {conteudo_id} enfileirado com sucesso.")
                else:
                    print(f"Falha ao enfileirar o conteúdo {conteudo_id}.")
            case 8:
                proximo_conteudo = catalogo.proximo()
                if proximo_conteudo is None:
                    print("Fila de reprodução vazia.")
                else:
                    print(f"Tocando próximo conteúdo: {proximo_conteudo}")
            case 9:
                fila_atual = catalogo.fila_atual()
                if len(fila_atual) == 0:
                    print("Fila de reprodução vazia.")
                else:
                    print("Fila atual:")
                    for conteudo_id in fila_atual:
                        print(conteudo_id)
            case 0:
                break
terminal()
