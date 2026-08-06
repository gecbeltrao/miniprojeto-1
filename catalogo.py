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
            self.conteudos[conteudo_id] = conteudo

        self.fila_musicas = []



    # --- usuários e playlists ---
    def listar_usuarios(self) -> list[str]:
        nomes = [usuario["nome"] for usuario in self.dados["usuarios"]]
        return sorted(nomes)

    def buscar_usuario_por_nome(self, nome: str) -> str | None:
        return self.nome_usuarios.get(nome.lower())

    def playlist_de(self, usuario_id: str) -> list[str] | None:
        usuario = self.id_usuarios.get(usuario_id)
        if usuario is None:
            return None
        return usuario["playlist"][:]

    def conteudo_na_posicao(self, usuario_id: str, posicao: int) -> str | None:
        playlist = self.playlist_de(usuario_id)
        if playlist is None:
            return None
        if posicao < 0 or posicao >= len(playlist):
            return None
        return playlist[posicao]

    def intersecao_playlists(self, usuario_ids: list[str]) -> list[str]:
        conjuntos = []
        for usuario_id in usuario_ids:
            playlist = self.playlist_de(usuario_id)
            if playlist is None:
                return []
            conjuntos.append(set(playlist))
        if not conjuntos:
            return []
        return sorted(set.intersection(*conjuntos))
    
    # --- dados de um conteúdo ---
    def rating_de(self, conteudo_id: str) -> float | None:
        conteudo = self.id_conteudos.get(conteudo_id)
        if conteudo is None:
            return None
        if "rating" not in conteudo:
            return None
        return float(conteudo["rating"])

    def duracao_total_de(self, conteudo_id: str) -> int | None:
        conteudo = self.id_conteudos.get(conteudo_id)
        if conteudo is None:
            return None
        if conteudo["tipo"] == "musica":
            return conteudo["duracao_seg"]
        total = 0
        for faixa in conteudo["faixas"]:
            duracao = faixa["duracao_seg"]
            if duracao is not None:
                total += duracao
        return total

    def generos_de(self, conteudo_id: str) -> list[str] | None:
        conteudo = self.id_conteudos.get(conteudo_id)
        if conteudo is None:
            return None
        return sorted(self._achatar_generos(conteudo["generos"]))

    def _achatar_generos(self, generos) -> list[str]:
        if isinstance(generos, str):
            return [generos]
        achatados = []
        pilha = list(generos)
        while pilha:
            item = pilha.pop()
            if isinstance(item, list):
                pilha.extend(item)
            else:
                achatados.append(item)
        return achatados

    def plataformas_de(self, conteudo_id: str) -> list[str] | None:
        conteudo = self.id_conteudos.get(conteudo_id)
        if conteudo is None:
            return None
        return sorted(conteudo.get("plataformas", []))

    def data_adicionado_de(self, conteudo_id: str) -> str | None:
        conteudo = self.id_conteudos.get(conteudo_id)
        if conteudo is None:
            return None
        data = conteudo["data_adicionado"]
        if "/" in data:
            dia, mes, ano = data.split("/")
            return f"{ano}-{mes}-{dia}"
        return data

    def execucoes_de(self, conteudo_id: str) -> int | None:
        conteudo = self.id_conteudos.get(conteudo_id)
        if conteudo is None:
            return None
        execucoes = conteudo["engajamento"]["execucoes"]
        if isinstance(execucoes, str):
            execucoes = execucoes.replace(",", "")
        return int(execucoes)

    def conteudos_do_genero(self, genero: str) -> list[str]:
        resultado = []
        for conteudo_id in self.id_conteudos:
            generos = self.generos_de(conteudo_id)
            if genero in generos:
                resultado.append(conteudo_id)
        return sorted(resultado)

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
