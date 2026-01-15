"""
Módulo: analise.py
Gera gráficos.
"""
import matplotlib.pyplot as plt
import numpy as np
import simulacao

def plot_evolucao_fila(historico_fila):
    if not historico_fila: return
    tempos, tamanhos = zip(*historico_fila)
    plt.figure("Fila", figsize=(10, 5))
    plt.step(tempos, tamanhos, where='post', color="#0b6d18", linewidth=2)
    plt.fill_between(tempos, tamanhos, step='post', color='#e67e22', alpha=0.3)
    plt.title("Evolução da Fila")
    plt.xlabel("Tempo (min)")
    plt.ylabel("Pessoas")
    plt.grid(True, alpha=0.5)
    plt.tight_layout()
    plt.show(block=False)

def plot_ocupacao(historico_ocupacao):
    if not historico_ocupacao: return
    tempos, ocupacao = zip(*historico_ocupacao)
    plt.figure("Ocupação", figsize=(10, 5))
    plt.plot(tempos, ocupacao, color="#ed0ec8")
    plt.title("Ocupação Instantânea")
    plt.xlabel("Tempo (min)")
    plt.ylabel("%")
    plt.ylim(-5, 105)
    plt.grid(True, alpha=0.5)
    plt.tight_layout()
    plt.show(block=False)

def plot_sensibilidade(config_base):
    taxas = range(10, 31, 2)
    y = []
    print("A testar sensibilidade...")
    for t in taxas:
        cfg = config_base.copy()
        cfg['taxa_chegada'] = t
        res = simulacao.simular_atendimento(cfg, None)
        if res['hist_fila']:
            y.append(np.mean([val[1] for val in res['hist_fila']]))
        else:
            y.append(0)
            
    plt.figure("Sensibilidade", figsize=(8, 5))
    plt.plot(taxas, y, marker='o', color="#1b45cf")
    plt.title("Stress Test (Fila vs Chegadas)")
    plt.xlabel("Doentes/Hora")
    plt.ylabel("Média Fila")
    plt.grid(True)
    plt.tight_layout()
    plt.show(block=False)

def plot_histograma_clinica(tempos_clinica):
    if not tempos_clinica:
        return
    plt.figure("Histograma Tempo Clínica", figsize=(8,5))
    plt.hist(tempos_clinica, bins=15, color="#c2de0f", alpha=0.7, edgecolor='black')
    plt.title("Distribuição do Tempo na Clínica")
    plt.xlabel("Tempo Total na Clínica (min)")
    plt.ylabel("Frequência")
    plt.grid(True, alpha=0.5)
    plt.tight_layout()
    plt.show(block=False)

def plot_histograma_desistencias(tempos_desistencia):
    if not tempos_desistencia:
        return
    plt.figure("Desistências", figsize=(8,5))
    plt.hist(tempos_desistencia, bins=15, color="#530559", alpha=0.7, edgecolor='black')
    plt.title("Distribuição dos Tempos de Desistência (VERDE)")
    plt.xlabel("Tempo Espera (min)")
    plt.ylabel("Frequência")
    plt.grid(True, alpha=0.5)
    plt.tight_layout()
    plt.show(block=False)




