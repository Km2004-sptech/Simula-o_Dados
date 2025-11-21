import csv
import random
from datetime import datetime, timedelta
import json

ARQUIVO = "dados_simulados.py.csv"

# 15 números seriais
NUM_SERIAIS = [f"{i:04d}" for i in range(1, 16)]

# 🎯 Setor fixo por número serial
SETOR_POR_SERIAL = {
    "0001": "Fabricação de Componentes",
    "0002": "Fabricação de Componentes",
    "0003": "Fabricação de Componentes",

    "0004": "Desenvolvimento de Tecnologias",
    "0005": "Desenvolvimento de Tecnologias",
    "0006": "Desenvolvimento de Tecnologias",
    "0007": "Desenvolvimento de Tecnologias",

    "0008": "Estamparia",
    "0009": "Estamparia",
    "0010": "Estamparia",
    "0011": "Estamparia",

    "0012": "Montagem final",
    "0013": "Montagem final",
    "0014": "Montagem final",
    "0015": "Montagem final",
}

# Valores iniciais do disco para cada serial (20% a 40%)
disco_usado_atual = {serial: random.uniform(20, 40) for serial in NUM_SERIAIS}

# Contador global de dias simulados
dias_passados = 0


# ---------------------- FUNÇÃO DISCO GRADUAL ----------------------
def atualizar_disco(serial, dias_passados):
    """Atualiza lentamente o uso de disco com comportamento realista."""

    valor = disco_usado_atual[serial]

    # 1) Aumento diário leve
    valor += random.uniform(0.02, 0.15)

    # 2) A cada 14 dias → acúmulo maior
    if dias_passados % 14 == 0 and dias_passados != 0:
        valor += random.uniform(0.8, 2.5)

    # 3) A cada 60 dias → limpeza (queda)
    if dias_passados % 60 == 0 and dias_passados != 0:
        valor -= random.uniform(1.5, 5.0)

    # Mantém em limites realistas
    valor = max(5.0, min(95.0, valor))

    # Atualiza o valor armazenado
    disco_usado_atual[serial] = valor
    return round(valor, 2)


# ---------------------- TOPO DO CSV ----------------------
with open(ARQUIVO, "w", newline="") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow([
        "timestamp", "numSerial", "setor", "cpu", "ramTotal",
        "ramUsada", "discoTotal", "discoUsado",
        "numProcessos", "top5Processos"
    ])


# ---------------------- CONFIGURAÇÃO DE DATAS ----------------------
ano_atual = datetime.now().year

inicio_geral = datetime(ano_atual, 1, 1, 0, 0)
fim_geral = datetime(ano_atual, 12, 1, 23, 0)

inicio_dia2 = datetime(ano_atual, 12, 2, 0, 0)
fim_dia2 = datetime(ano_atual, 12, 2, 23, 59)


# ---------------------- FUNÇÃO TOP 5 PROCESSOS ----------------------
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


# ---------------------- GERAR CSV ----------------------
with open(ARQUIVO, "a", newline="") as f:
    writer = csv.writer(f, delimiter=";")

    # ---------------------- PARTE 1: 1 captura por HORA ----------------------
    tempo = inicio_geral
    incremento_horas = timedelta(hours=1)

    dias_passados = 0
    ultimo_dia = tempo.day

    while tempo <= fim_geral:

        # Detecta mudança de dia
        if tempo.day != ultimo_dia:
            dias_passados += 1
            ultimo_dia = tempo.day

        for serial in NUM_SERIAIS:

            setor = SETOR_POR_SERIAL[serial]  # ← setor fixo por serial
            cpu = round(random.uniform(1, 95), 2)
            ram_total = 8 * (1024 ** 3)
            ram_usada = round(random.uniform(20, 95), 2)
            disco_total = 250 * (1024 ** 3)

            # DISCO REALISTA
            disco_usado = atualizar_disco(serial, dias_passados)

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

    # ---------------------- PARTE 2: 1 captura por MINUTO no dia 02/12 ----------------------
    tempo = inicio_dia2
    incremento_minutos = timedelta(minutes=1)

    while tempo <= fim_dia2:

        for serial in NUM_SERIAIS:

            setor = SETOR_POR_SERIAL[serial]  # ← setor fixo
            cpu = round(random.uniform(1, 95), 2)
            ram_total = 8 * (1024 ** 3)
            ram_usada = round(random.uniform(20, 95), 2)
            disco_total = 250 * (1024 ** 3)

            disco_usado = atualizar_disco(serial, dias_passados)

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
