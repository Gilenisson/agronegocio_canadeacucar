import json
from datetime import datetime

# Lista principal
colheitas = []

# Tupla com classificações
CLASSIFICACAO_PERDAS = ("BAIXA", "MODERADA", "ALTA")


def ler_texto(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("Digite um texto válido!")


def ler_float(mensagem):
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))
            if valor >= 0:
                return valor
            else:
                print("Digite um número positivo.")
        except:
            print("Digite um número válido!")


def calcular_perda(esperado, colhido):
    perda = esperado - colhido
    if esperado > 0:
        percentual = (perda / esperado) * 100
    else:
        percentual = 0
    return perda, percentual


def classificar_perda(percentual):
    if percentual <= 5:
        return CLASSIFICACAO_PERDAS[0]
    elif percentual <= 10:
        return CLASSIFICACAO_PERDAS[1]
    else:
        return CLASSIFICACAO_PERDAS[2]


def cadastrar_colheita():
    print("\n--- Cadastro de Colheita ---")

    fazenda = ler_texto("Nome da fazenda: ")
    talhao = ler_texto("Talhão: ")
    area = ler_float("Área (hectares): ")
    esperado = ler_float("Produção esperada (t): ")
    colhido = ler_float("Produção colhida (t): ")

    if colhido > esperado:
        print("Erro: colhido não pode ser maior que esperado!")
        return

    perda, percentual = calcular_perda(esperado, colhido)
    classificacao = classificar_perda(percentual)

    registro = {
        "fazenda": fazenda,
        "talhao": talhao,
        "area": area,
        "esperado": esperado,
        "colhido": colhido,
        "perda": round(perda, 2),
        "percentual": round(percentual, 2),
        "classificacao": classificacao,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M")
    }

    colheitas.append(registro)

    print("\nColheita cadastrada!")
    print(f"Perda: {perda:.2f} t")
    print(f"Percentual: {percentual:.2f}%")
    print(f"Classificação: {classificacao}")


def listar_colheitas():
    print("\n--- Relatório ---")

    if not colheitas:
        print("Nenhuma colheita cadastrada.")
        return

    for i, c in enumerate(colheitas, 1):
        print(f"\nColheita {i}")
        print(f"Fazenda: {c['fazenda']}")
        print(f"Talhão: {c['talhao']}")
        print(f"Área: {c['area']} ha")
        print(f"Esperado: {c['esperado']} t")
        print(f"Colhido: {c['colhido']} t")
        print(f"Perda: {c['perda']} t")
        print(f"Percentual: {c['percentual']}%")
        print(f"Classificação: {c['classificacao']}")
        print(f"Data: {c['data']}")


def salvar_json():
    with open("dados_colheita.json", "w", encoding="utf-8") as f:
        json.dump(colheitas, f, indent=4, ensure_ascii=False)
    print("Dados salvos!")


def carregar_json():
    global colheitas
    try:
        with open("dados_colheita.json", "r", encoding="utf-8") as f:
            colheitas = json.load(f)
    except:
        colheitas = []


def salvar_txt():
    with open("relatorio_colheitas.txt", "w", encoding="utf-8") as f:
        for c in colheitas:
            f.write(f"Fazenda: {c['fazenda']}\n")
            f.write(f"Talhão: {c['talhao']}\n")
            f.write(f"Perda: {c['perda']} t\n")
            f.write(f"Percentual: {c['percentual']}%\n")
            f.write(f"Classificação: {c['classificacao']}\n")
            f.write("-" * 30 + "\n")
    print("Relatório gerado!")


def menu():
    carregar_json()

    while True:
        print("\n1 - Cadastrar colheita")
        print("2 - Listar colheitas")
        print("3 - Salvar JSON")
        print("4 - Gerar TXT")
        print("5 - Sair")

        op = input("Escolha: ")

        if op == "1":
            cadastrar_colheita()
        elif op == "2":
            listar_colheitas()
        elif op == "3":
            salvar_json()
        elif op == "4":
            salvar_txt()
        elif op == "5":
            salvar_json()
            print("Encerrando...")
            break
        else:
            print("Opção inválida!")


menu()