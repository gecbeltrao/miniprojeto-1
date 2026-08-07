"""Menu interativo no terminal.

Uso: python cli.py catalogo_final.json
"""

from catalogo import Catalogo
catalogo = Catalogo("catalogo_final.json")

def formatar_duracao(segundos: int) -> str:
    minutos = segundos // 60
    segundos_restantes = segundos % 60
    return f"{minutos}m{segundos_restantes:02d}s"


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
                usuarios = catalogo.listar_usuarios()
                print(f"{len(usuarios)} usuários (ordem alfabética):")
                largura = max(len(nome) for nome in usuarios) + 4
                for i in range(0, len(usuarios), 3):
                    linha = usuarios[i:i + 3]
                    print("".join(nome.ljust(largura) for nome in linha))
            case 2:
                nome = input("Digite o nome do usuário: ")
                usuario_id = catalogo.buscar_usuario_por_nome(nome)
                if usuario_id is None:
                    print(f"Usuário {nome} não encontrado.")
                else:
                    playlist = catalogo.playlist_de(usuario_id)
                    print(f"Playlist de {nome} ({len(playlist)} itens):")
                    for i, conteudo_id in enumerate(playlist, start=1):
                        print(f"  {i}. {catalogo.titulo_de(conteudo_id)}")
            case 3:
                nome = input("Digite o nome do usuário: ")
                usuario_id = catalogo.buscar_usuario_por_nome(nome)
                if usuario_id is None:
                    print(f"Usuário {nome} não encontrado.")
                else:
                    playlist = catalogo.playlist_de(usuario_id)
                    print(f"Playlist de {nome} tem {len(playlist)} itens (posições 1 a {len(playlist)}).")
                    posicao_digitada = int(input("Posição: "))
                    posicao = posicao_digitada - 1
                    conteudo_id = catalogo.conteudo_na_posicao(usuario_id, posicao)
                    if conteudo_id is None:
                        print(f"Posição {posicao_digitada} inválida para o usuário {nome}.")
                    else:
                        print(f"Posição {posicao_digitada} de {nome}: {catalogo.titulo_de(conteudo_id)}")
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
                    comuns = catalogo.intersecao_playlists(usuario_ids)
                    if len(comuns) == 0:
                        print("Nenhum conteúdo em comum.")
                    else:
                        print(f"Interseção ({len(comuns)} conteúdos)")
                        for conteudo_id in comuns:
                            print(f"  - {catalogo.titulo_de(conteudo_id)}")
            case 5:
                conteudo_id = input("Digite o ID do conteúdo: ")
                titulo = catalogo.titulo_de(conteudo_id)
                if titulo is None:
                    print(f"Conteúdo {conteudo_id} não encontrado.")
                else:
                    rating = catalogo.rating_de(conteudo_id)
                    duracao = catalogo.duracao_total_de(conteudo_id)
                    generos = catalogo.generos_de(conteudo_id)
                    plataformas = catalogo.plataformas_de(conteudo_id)
                    data_adicionado = catalogo.data_adicionado_de(conteudo_id)
                    execucoes = catalogo.execucoes_de(conteudo_id)

                    print(titulo)
                    print(f"  rating:       {rating}")
                    print(f"  duração:      {formatar_duracao(duracao)}")
                    print(f"  gêneros:      {', '.join(generos)}")
                    print(f"  plataformas:  {', '.join(plataformas)}")
                    print(f"  adicionado:   {data_adicionado}")
                    if execucoes is not None:
                        print(f"  execuções:    {execucoes}")
            case 6:
                genero = input("Gênero (ex.: Pop): ")
                conteudo_ids = catalogo.conteudos_do_genero(genero)
                if len(conteudo_ids) == 0:
                    print(f'Nenhum conteúdo encontrado para o gênero "{genero}".')
                else:
                    print(f'{len(conteudo_ids)} conteúdos em "{genero}":')
                    for conteudo_id in conteudo_ids:
                        print(f"  - {catalogo.titulo_de(conteudo_id)} ({conteudo_id})")
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
                    plural = "item" if len(fila_atual) == 1 else "itens"
                    print(f"Fila atual ({len(fila_atual)} {plural}, próximo primeiro):")
                    for i, conteudo_id in enumerate(fila_atual, start=1):
                        print(f"  {i}. {catalogo.titulo_de(conteudo_id)}")
            case 0:
                break
terminal()
