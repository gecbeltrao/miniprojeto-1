"""Modo batch: lê consultas.json, responde em ordem, grava respostas.json.

Uso: python main.py consultas.json respostas.json
"""

import json
from catalogo import Catalogo

def main():
    caminho_consultas = input("Caminho do consultas.json: ").strip()
    caminho_respostas = input("Caminho de saída para respostas.json: ").strip()

    catalogo = Catalogo("catalogo_final.json")  # batch sempre usa o catálogo cheio

    with open(caminho_consultas, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    respostas = {}
    for consulta in dados["consultas"]:  # em ordem — fila/proximo dependem disso
        consulta_id = consulta["id"]
        tipo = consulta["tipo"]
        parametros = consulta["parametros"]

        metodo = getattr(catalogo, tipo)
        resultado = metodo(**parametros)

        respostas[str(consulta_id)] = resultado  # regra 17: chave como string

    with open(caminho_respostas, "w", encoding="utf-8") as arquivo:
        json.dump(respostas, arquivo, ensure_ascii=False, indent=2)

    print(f"{len(respostas)} respostas gravadas em {caminho_respostas}")

main()
