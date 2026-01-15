"""
Módulo: simulacao.py
Estrutura ESTRITA do docente + Lógica de Pulseiras/Especialidades.
"""
import random
import numpy as np
import json

CHEGADA = 1
SAIDA = 2
DESISTENCIA=3

VERMELHA = 0
AMARELA = 1
VERDE = 2
CORES_STR = {0: "Vermelha", 1: "Amarela", 2: "Verde"}
T_MAX_ESPERA_VERDE = 120 

def carregar_pessoas(ficheiro="pessoas.json"):
    try:
        with open(ficheiro, "r", encoding="utf-8") as f:
            pessoas_raw = json.load(f)
    except Exception as e:
        print(f"Erro ao ler {ficheiro}: {e}")
        return []

    pessoas = []
    for idx, p in enumerate(pessoas_raw):
        pessoa = {
            'id': p.get('id', f"P{idx+1}"),
            'nome': p.get('nome', f"Paciente{idx+1}"),
            'idade': p.get('idade', 30)
        }
        pessoas.append(pessoa)
    return pessoas



PROB_ESPECIALIDADES = {"GERAL": 0.40, "INTERN": 0.30, "ORTO": 0.15, "CARD": 0.10, "PED": 0.05}
TEMPO_MEDIO_ESP = {"GERAL": 10, "INTERN": 15, "PED": 15, "ORTO": 20, "CARD": 25}

def e_tempo(e): 
    return e[0]
def e_tipo(e): 
    return e[1]
def e_doente(e): 
    return e[2]


def procuraPosQueue(q, t):
    i = 0
    while i < len(q) and t > q[i][0]:
        i = i + 1
    return i

def enqueue(q, e):
    pos = procuraPosQueue(q, e[0])
    return q[:pos] + [e] + q[pos:]

def dequeue(q):
    if not q: 
        return None, []
    e = q[0]
    q = q[1:]
    return e, q


def m_id(e): 
    return e[0]
def m_ocupado(e): 
    return e[1]

def mOcupa(m):

    m[1] = not m[1]
    return m

def m_doente_corrente(e): 
    return e[2]
def mDoenteCorrente(m, d):
    m[2] = d
    return m

def m_total_tempo_ocupado(e): 
    return e[3]
def mTempoOcupado(m, t):
    m[3] = t
    return m

def m_inicio_ultima_consulta(e): 
    return e[4]
def mInicioConsulta(m, t):
    m[4] = t
    return m


def m_especialidade(m): 
    return m[5]

def gera_intervalo_tempo_chegada(lmbda):
    return np.random.exponential(60.0 / lmbda)

def gera_tempo_consulta(media, dist="exponential"):
    if dist == "normal":
        duracao=np.random.normal(media, 4.0)
        if duracao<2.0:
            duracao=2.0
        return duracao
    elif dist == "uniform":
        return np.random.uniform(media * 0.8, media * 1.2)
    return np.random.exponential(media)

def procuraMedico(lista, especialidade_paciente):
    candidato=None
    i = 0
    while i < len(lista):
        if not m_ocupado(lista[i]) and m_especialidade(lista[i]) == especialidade_paciente:
            candidato=lista[i]
        i += 1
    if candidato is not None:
        return candidato

    if especialidade_paciente == "PED":
        i = 0
        while i < len(lista):
            if not m_ocupado(lista[i]) and m_especialidade(lista[i]) == "GERAL":
                candidato=lista[i]
            i +=1
        if candidato is not None:
            return candidato

            

    if especialidade_paciente != "PED":
        i = 0
        while i < len(lista):

            med = lista[i]
            if not m_ocupado(med):
                esp_med = m_especialidade(med)
                if esp_med == "GERAL" or esp_med != "PED":
                    candidato=med
            i += 1
        if candidato is not None:
            return candidato
            
    return None


def atribuir_pulseira(idade):
    cores = [VERDE, AMARELA, VERMELHA]
    pesos = [0.3, 0.5, 0.2] if idade >= 70 else [0.7, 0.2, 0.1]
    return random.choices(cores, weights=pesos, k=1)[0]

def atribuir_especialidade(idade):
    if idade < 18: return "PED"
    esps = ["GERAL", "INTERN", "ORTO", "CARD"]
    pesos = [0.45, 0.35, 0.15, 0.05]
    return random.choices(esps, weights=pesos, k=1)[0]
def simular_atendimento(config, db_pessoas=None):
    if db_pessoas is None:
        db_pessoas = carregar_pessoas()  
    # Parâmetros
    lmbda = config['taxa_chegada']
    n_medicos = config['num_medicos']
    tempo_sim = config['tempo_max']
    dist_tipo = config['distribuicao']

    tempo_atual = 0.0
    contadorDoentes = 1
    queueEventos = [] 
    queue = []
    desistencias=0
    total_verdes=0

    esps_fixas = ["GERAL", "INTERN", "ORTO", "CARD", "PED"]
    medicos = []
    for i in range(n_medicos):
        esp = esps_fixas[i % 5]

        medicos.append([f"M{i+1}", False, None, 0.0, 0.0, esp])


    t = 0.0
    while t < tempo_sim:
        t += gera_intervalo_tempo_chegada(lmbda)

        if db_pessoas:
            idx = (contadorDoentes - 1) % len(db_pessoas)
            p_raw = db_pessoas[idx]
            nome = p_raw.get("nome", f"P{contadorDoentes}")
            idade = p_raw.get("idade", 30)
        else:
            nome = f"P{contadorDoentes}"; idade = 30
            
        prio = atribuir_pulseira(idade)
        esp = atribuir_especialidade(idade)
        

        doente = {
            'id': contadorDoentes, 'nome': nome, 'idade': idade,
            'chegada': t, 'prioridade': prio, 'cor': CORES_STR[prio], 'esp': esp
        }

        queueEventos = enqueue(queueEventos, (t, CHEGADA, doente))
        contadorDoentes += 1



    hist_fila = [(0.0, 0)]
    hist_ocup = []
    log = []
    pessoas_final=[]
    tempos_espera = []
    tempos_clinica = []
    tempos_consulta = []
    tempos_desistencia=[]
    max_fila = 0
    atendidos = 0
    


    while queueEventos:
        evento, queueEventos = dequeue(queueEventos)
        tempo_atual = e_tempo(evento)
        tipo = e_tipo(evento)
        paciente = e_doente(evento)

        if len(queue) > max_fila: 
            max_fila = len(queue)
        hist_fila.append((tempo_atual, len(queue)))

        if tipo == CHEGADA:
            medico = procuraMedico(medicos, paciente['esp'])
            
            if paciente['prioridade'] == VERDE:
                total_verdes += 1

            if medico:
                mOcupa(medico)
                mInicioConsulta(medico, tempo_atual)
                mDoenteCorrente(medico, paciente)
                
                t_base = config.get("tempo_medio", TEMPO_MEDIO_ESP.get(paciente['esp'], 15))
                duracao = gera_tempo_consulta(t_base, dist_tipo)
                
              
                queueEventos = enqueue(queueEventos, (tempo_atual + duracao, SAIDA, paciente))
                
                tempos_espera.append(0.0)
                log.append(f"[{tempo_atual:1f}min] CHEGADA: {paciente['nome']} ({paciente['esp']}/{paciente['cor']}) -> Dr.{m_id(medico)}")
            else:
                
                queue.append(paciente)
                queue.sort(key=lambda x: x['prioridade'])
                log.append(f"[{tempo_atual:.1f} min] CHEGADA: {paciente['nome']} ({paciente['esp']}/{paciente['cor']}) -> Aguarda")

                
                if paciente['prioridade'] == VERDE:
                    if paciente['idade'] >= 70:
                        t_desiste = tempo_atual + 180
                    else:
                        t_desiste = tempo_atual + 90

                    queueEventos = enqueue(queueEventos, (t_desiste, DESISTENCIA, paciente))


        elif tipo == SAIDA:
            atendidos += 1
            
            
            medico_livre = None
            for m in medicos:
                if medico_livre is None and m_doente_corrente(m)==paciente:
                    
                    duracao = tempo_atual - m_inicio_ultima_consulta(m)
                    mTempoOcupado(m, m_total_tempo_ocupado(m) + duracao)
                    
                  
                    mOcupa(m) 
                    mDoenteCorrente(m, None)
                    
                    tempos_clinica.append(tempo_atual - paciente['chegada'])
                    tempos_consulta.append(duracao)
                    medico_livre = m
                    pessoas_final.append({
                        "nome": paciente["nome"],
                        "idade": paciente["idade"],
                        "prioridade": paciente["cor"],
                        "especialidade": paciente["esp"],
                        "tempo_espera": tempo_atual - paciente["chegada"] - duracao,
                        "tempo_clinica": tempo_atual - paciente["chegada"]
                    })

            

            if queue and medico_livre:
 
                idx_candidato = -1
                

                sou_pediatra = (m_especialidade(medico_livre) == "PED")
                
                idx_candidato=-1
                for i, p_fila in enumerate(queue):
                    e_crianca = (p_fila['esp'] == "PED")
                    if idx_candidato==-1:
    
                        if sou_pediatra and e_crianca:
                            idx_candidato = i
                        elif not sou_pediatra and not e_crianca:
                  
                            idx_candidato = i
                
                if idx_candidato != -1:
                    prox = queue.pop(idx_candidato)
                    
                    mOcupa(medico_livre)
                    mInicioConsulta(medico_livre, tempo_atual)
                    mDoenteCorrente(medico_livre, prox)
                    
                    espera = tempo_atual - prox['chegada']
                    tempos_espera.append(espera)
                    
                    t_base = TEMPO_MEDIO_ESP.get(prox['esp'], 15)
                    duracao = gera_tempo_consulta(t_base, dist_tipo)
                    
                    queueEventos = enqueue(queueEventos, (tempo_atual + duracao, SAIDA, prox))
                    log.append(f"[{tempo_atual:.1f}min] ATENDIMENTO: {prox['nome']} (Espera:{espera:.1f}m) -> Dr.{m_id(medico_livre)}")
        
        elif tipo == DESISTENCIA:
            if paciente in queue:
                queue.remove(paciente)
                desistencias += 1
                tempos_desistencia.append(tempo_atual-paciente['chegada'])
                paciente["desistiu"]=True
                log.append(
                    f"[{tempo_atual:.1f} min]   DESISTENCIA: {paciente['nome']} (VERDE) "
                    f"após {tempo_atual - paciente['chegada']:.1f} min"
                )

        ocupados = sum(1 for m in medicos if m_ocupado(m))
        perc = (ocupados/n_medicos)*100
        hist_ocup.append((tempo_atual, min(perc, 100)))


    total_trab = 0
    stats = []
    for m in medicos:
        t_util = min(m_total_tempo_ocupado(m), tempo_sim)
        total_trab += t_util
        stats.append(f"{m_id(m)} [{m_especialidade(m)}]: {(t_util/tempo_sim)*100:.1f}%")
    
    ocup_media = (total_trab / (n_medicos * tempo_sim)) * 100

    try:
        with open("relatorio_final.txt", "w", encoding="utf-8") as f:
            for linha in log:
                f.write(linha+"\n")
    except Exception as e:
        log.append(f"ERRO: Não foi possivel gravar relatorio_final.txt:{e}")

    return {
        'doentes_atendidos': atendidos,
        'media_espera': np.mean(tempos_espera) if tempos_espera else 0,
        'media_clinica': np.mean(tempos_clinica) if tempos_clinica else 0,
        'media_consulta': np.mean(tempos_consulta) if tempos_consulta else 0,
        'ocupacao_media': min(ocup_media, 100.0),
        'max_fila': max_fila,
        'stats_medicos': stats,
        'hist_fila': hist_fila,
        'hist_ocupacao': hist_ocup,
        'pessoas': pessoas_final,
        'desistencias_verdes':desistencias,
        'taxa_desistencia_verdes': desistencias / (total_verdes)
            if total_verdes > 0 else 0,
        'tempos_desistencia':tempos_desistencia,
        'media_tempo_desistencia': np.mean(tempos_desistencia) if tempos_desistencia else 0
    }
    
    
