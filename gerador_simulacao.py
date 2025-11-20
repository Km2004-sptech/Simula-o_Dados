import csv
import random
from datetime import datetime, timedelta
import json

ARQUIVO = "dados_simulados.py.csv"

NUM_SERIAIS = [f"{i:04d}" for i in range(1, 16)]

SETORES = [
    "Fabricação de Componentes",
    "Desenvolvimento de Tecnologias",
    "Estamparia",
    "Montagem final"
]

with open(ARQUIVO, "w", newline="") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow([
        "timestamp", "numSerial", "setor", "cpu", "ramTotal",
        "ramUsada", "discoTotal", "discoUsado",
        "numProcessos", "top5Processos"
    ])

ano_atual = datetime.now().year

inicio_geral = datetime(ano_atual, 1, 1, 0, 0)
fim_geral = datetime(ano_atual, 12, 1, 23, 0)

inicio_dia2 = datetime(ano_atual, 12, 2, 0, 0)
fim_dia2 = datetime(ano_atual, 12, 2, 23, 59)

def gerar_top5():
    lista = []
    for i in range(5):
        lista.append({
            "pid": random.randint(100, 9999),
            "name": f"processo{i+1}",
            "cpu_percent": round(random.uniform(0, 40), 2),
            "memory_rss": random.randint(50_000_000, 500_000_000)
        })
    return lista

with open(ARQUIVO, "a", newline="") as f:
    writer = csv.writer(f, delimiter=";")

    # Parte 1: 01/01 até 01/12 - 1 captura por hora
    tempo = inicio_geral
    incremento_horas = timedelta(hours=1)

    while tempo <= fim_geral:
        for serial in NUM_SERIAIS:
            setor = random.choice(SETORES)
            cpu = round(random.uniform(1, 95), 2)
            ram_total = 8 * (1024 ** 3)
            ram_usada = round(random.uniform(20, 95), 2)
            disco_total = 250 * (1024 ** 3)
            disco_usado = round(random.uniform(10, 95), 2)
            num_processos = random.randint(50, 300)
            top5 = gerar_top5()

            writer.writerow([
                tempo.strftime("%Y-%m-%d %H:%M:%S"),
                serial,
                setor,
                cpu,
                ram_total,
                ram_usada,
                disco_total,
                disco_usado,
                num_processos,
                json.dumps(top5)
            ])
        tempo += incremento_horas

    # Parte 2: 02/12 - 1 captura por minuto
    tempo = inicio_dia2
    incremento_minutos = timedelta(minutes=1)

    while tempo <= fim_dia2:
        for serial in NUM_SERIAIS:
            setor = random.choice(SETORES)
            cpu = round(random.uniform(1, 95), 2)
            ram_total = 8 * (1024 ** 3)
            ram_usada = round(random.uniform(20, 95), 2)
            disco_total = 250 * (1024 ** 3)
            disco_usado = round(random.uniform(10, 95), 2)
            num_processos = random.randint(50, 300)
            top5 = gerar_top5()

            writer.writerow([
                tempo.strftime("%Y-%m-%d %H:%M:%S"),
                serial,
                setor,
                cpu,
                ram_total,
                ram_usada,
                disco_total,
                disco_usado,
                num_processos,
                json.dumps(top5)
            ])
        tempo += incremento_minutos

print("Arquivo CSV gerado com sucesso:", ARQUIVO)
