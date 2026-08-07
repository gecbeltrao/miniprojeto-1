"""Confere respostas.json contra o gabarito_publico.json."""

import json

def bate(esperado, obtido) -> bool:
    if isinstance(esperado, float) or isinstance(obtido, float):
        if not isinstance(esperado, (int, float)) or not isinstance(obtido, (int, float)):
            return False
        return abs(esperado - obtido) < 1e-6
    return esperado == obtido

def main():
    caminho_gabarito = input("Caminho do gabarito_publico.json: ").strip()
    caminho_respostas = input("Caminho do respostas.json: ").strip()

    with open(caminho_gabarito, "r", encoding="utf-8") as arquivo:
        gabarito = json.load(arquivo)

    with open(caminho_respostas, "r", encoding="utf-8") as arquivo:
        respostas = json.load(arquivo)

    acertos = 0
    ausentes = []
    erradas = []

    for consulta_id, esperado in gabarito.items():
        if consulta_id not in respostas:
            ausentes.append(consulta_id)
            continue

        obtido = respostas[consulta_id]
        if bate(esperado, obtido):
            acertos += 1
        else:
            erradas.append((consulta_id, esperado, obtido))

    total = len(gabarito)
    print(f"{acertos}/{total} corretas")

    if ausentes:
        print(f"\n{len(ausentes)} ausentes (não apareceram em respostas.json):")
        for consulta_id in ausentes:
            print(f"  {consulta_id}")

    if erradas:
        print(f"\n{len(erradas)} erradas:")
        for consulta_id, esperado, obtido in erradas:
            print(f"  {consulta_id}: esperado {esperado!r}, obtido {obtido!r}")

main()