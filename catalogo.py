"""A classe Catalogo. Leia o README.md antes de começar.

Esta é a peça central do projeto: carrega o JSON uma vez, constrói os
índices no __init__ e expõe os 16 métodos que o main.py e o cli.py usam.
"""

import json

class Catalogo:
    def __init__(self, caminho_json: str):
        with open(caminho_json, "r", encoding="utf-8") as arquivo:
            self.dados = json.load(arquivo)

        self.id_usuarios = {}

        for usuario in self.dados["usuarios"]:
            usuario_id = usuario["id"]
            self.id_usuarios[usuario_id] = usuario   

        self.nome_usuarios = {}

        for usuario in self.dados["usuarios"]:
            nome = usuario["nome"].lower()
            usuario_id = usuario["id"]
            self.nome_usuarios[nome] = usuario_id

        self.conteudos = {}

        for conteudo in self.dados["conteudos"]:
            conteudo_id = conteudo["id"]
            self.id_conteudos[conteudo_id] = conteudo

        self.fila_musicas = []



    # --- usuários e playlists ---
    def listar_usuarios(self) -> list[str]:
    def buscar_usuario_por_nome(self, nome: str) -> str | None: ...
    def playlist_de(self, usuario_id: str) -> list[str] | None: ...
    def conteudo_na_posicao(self, usuario_id: str, posicao: int) -> str | None: ...
    def intersecao_playlists(self, usuario_ids: list[str]) -> list[str]: ...

    # --- dados de um conteúdo ---
    def rating_de(self, conteudo_id: str) -> float | None: ...
    def duracao_total_de(self, conteudo_id: str) -> int | None: ...
    def generos_de(self, conteudo_id: str) -> list[str] | None: ...
    def plataformas_de(self, conteudo_id: str) -> list[str] | None: ...
    def data_adicionado_de(self, conteudo_id: str) -> str | None: ...
    def execucoes_de(self, conteudo_id: str) -> int | None: ...
    def conteudos_do_genero(self, genero: str) -> list[str]: ...

    # --- fila de reprodução ---
    def enfileirar(self, conteudo_id: str) -> bool:

        if conteudo_id not in self.id_conteudo:
            print(f"Conteúdo {conteudo_id} não encontrado.")
            return False

        self.fila_musicas.append(conteudo_id)
        return True

    def proximo(self) -> str | None: 
        if self.fila_musicas:
            return self.fila_musicas.pop(0)
        else:
            print("Fila vazia")
            return None
        
    def fila_atual(self) -> list[str]:
        return self.fila_musicas[:]
