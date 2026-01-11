import json
import random
import numpy as np

# =============================================================================
# PARÂMETROS E CONFIGURAÇÕES
# =============================================================================

# Médico = [Nome, Ocupado, Doente, TempoTrab, InicioConsulta, Especialidade, É Reserva]
# Doente = (Tempo, Tipo, Nome, Triagem, Especialidade, ChegadaOriginal)

NUM_MEDICOS = 6
TAXA_CHEGADA = 25 / 60
TEMPO_SIMULACAO = 480 
TIPO_DISTRIBUICAO = "Exponencial" 

CHEGADA, SAIDA, DESISTENCIA = "chegada", "saída", "desistência"
ESPECIALIDADES = ["Ginecologia", "Cardiologia", "Urologia", "Medicina Geral", "Otorrinolaringologia", "Ortopedia"]

# =============================================================================
# FUNÇÕES DE ACESSO A DADOS (EVENTOS)
# =============================================================================

def e_tempo(e): 
    return e[0]

def e_tipo(e): 
    return e[1]

def e_doente(e): 
    return e[2]

def e_triagem(e): 
    return e[3]

def e_especialidade(e): 
    return e[4]

def e_chegada_original(e): 
    return e[5]

# =============================================================================
# GESTÃO DE FILAS E PROBABILIDADES
# =============================================================================

def procuraPosQueue(q, t): 
    i = 0
    pos = len(q)
    parar = False 
    
    while i < len(q) and parar == False:
        if t < q[i][0]: 
            pos = i
            parar = True 
        else: 
            i = i + 1
    return pos

def enqueue(q, e):
    q.insert(procuraPosQueue(q, e[0]), e)
    return q

def dequeue(q):
    elem = q[0]   
    q = q[1:]
    return elem, q

def procuraPosEspera(q, tri_nova):  
    i = 0
    pos = len(q)
    parar = False
    
    while i < len(q) and parar == False:
        if tri_nova > q[i][3]: 
            pos = i
            parar = True
        else: 
            i = i + 1
    return pos
 
def enqueue_espera(q, ev):
    q.insert(procuraPosEspera(q, ev[3]), ev) 
    return q

def gera_tempo_consulta(tri):
    base = 15
    if tri == 3: 
        base = 60
    elif tri == 2: 
        base = 40
    elif tri == 1: 
        base = 20
    elif tri == 0: 
        base = 10
    
    tempo_min = int(np.random.exponential(base))
    if tempo_min < 15: 
        tempo_min = 15
    return tempo_min

def gera_tempo_paciencia(tri):
    if tri == 0:
        media = 90
    else:
        media=150
    tempo = np.random.normal(media, 30)
    if tempo < 15: 
        tempo = 15
    return tempo

# =============================================================================
# MOTOR DE SIMULAÇÃO PRINCIPAL
# =============================================================================

def simula():
    tempo_atual = 0.0
    q_eventos = []   
    q_espera = []  
    medicos = []
    
    h_tempo, h_fila, h_ocup = [], [], []
    h_esp = [[], [], [], []]        
    h_atend = [0, 0, 0, 0]          
    h_esp_atend = []                
    historial = []                  
    
    k = 0
    while k < len(ESPECIALIDADES):
        h_esp_atend.append(0)
        k = k + 1

    lista_nomes_medicos = []
    with open("nomes médicos.txt", "r", encoding="utf-8") as f:
        linhas = f.readlines()
    for l in linhas:
        nome_limpo = l.strip()
        if len(nome_limpo) > 0:
            lista_nomes_medicos.append(nome_limpo)
    

    n_especialistas = NUM_MEDICOS // 2 
    if NUM_MEDICOS >= 6:
        n_especialistas = (NUM_MEDICOS // 6) * 6
    
    if n_especialistas == 0: 
        n_especialistas = NUM_MEDICOS
    
    if len(lista_nomes_medicos) > 0:
        random.shuffle(lista_nomes_medicos)
    
    i = 0
    while i < NUM_MEDICOS:
        if i < len(lista_nomes_medicos):
            nome_medico = "Dr. " + lista_nomes_medicos[i]
        else:
            nome_medico = "Dr. " + str(i+1)

        if i < n_especialistas:
            identificar_especialidade = i % 6
            nome_especialidade = ESPECIALIDADES[identificar_especialidade]
            m = [nome_medico, False, None, 0.0, 0.0, nome_especialidade, False]
        else:
            m = [nome_medico + " (Reserva)", False, None, 0.0, 0.0, "Geral", True]
            
        medicos.append(m)
        i = i + 1

    doentes = []
  
    f = open("pessoas.json", "r", encoding="utf-8")
    doentes = json.loads(f.read())
    f.close()

    t_acum = 0.0
    
    for d in doentes:
        sort_tri = np.random.random()
        tri = 0
        if sort_tri < 0.50: 
            tri = 0
        elif sort_tri < 0.80: 
            tri = 1
        elif sort_tri < 0.95: 
            tri = 2
        else: 
            tri = 3
        
        especialidade = random.choice(ESPECIALIDADES)
        
        intervalo = 0
        media_chegada = 1 / TAXA_CHEGADA 
        
        if TIPO_DISTRIBUICAO == "Exponencial":
            intervalo = np.random.exponential(scale=media_chegada)
        elif TIPO_DISTRIBUICAO == "Normal":
            intervalo = np.random.normal(loc=media_chegada, scale=media_chegada * 0.2)
        elif TIPO_DISTRIBUICAO == "Uniforme":
            intervalo = np.random.uniform(low=media_chegada * 0.5, high=media_chegada * 1.5)
            
        if intervalo < 0: 
            intervalo = 0
        t_acum = t_acum + intervalo
        
        if t_acum < TEMPO_SIMULACAO:
            evento = (t_acum, CHEGADA, d["nome"], tri, especialidade, t_acum)
            q_eventos = enqueue(q_eventos, evento)

            vai_desistir = False
            prob = np.random.random() 
            
            if tri == 0 and prob < 0.65: 
                vai_desistir = True
            elif tri == 1 and prob < 0.35: 
                vai_desistir = True
            
            if vai_desistir == True:
                tempo_limite = gera_tempo_paciencia(tri)
                momento_saida = t_acum + tempo_limite
                
                if momento_saida < TEMPO_SIMULACAO:
                    ev_desistencia = (momento_saida, DESISTENCIA, d["nome"], tri, especialidade, t_acum)
                    q_eventos = enqueue(q_eventos, ev_desistencia)

    while len(q_eventos) > 0:
        evento, q_eventos = dequeue(q_eventos)
        tempo_atual = e_tempo(evento)
        tipo_ev = e_tipo(evento)
            
        if tipo_ev == CHEGADA:
            q_espera = enqueue_espera(q_espera, evento)
            label_tri = ["T0", "T1", "T2", "T3"][e_triagem(evento)]
            historial.append({
                "tempo": round(tempo_atual, 1), "evento": "ENTRADA", 
                "doente": e_doente(evento), "medico": "---", "triagem": label_tri
            })

        elif tipo_ev == DESISTENCIA:
            nome_paciente = e_doente(evento)
            indice_na_fila = -1
            encontrou = False
            
            k = 0
            while k < len(q_espera) and encontrou == False:
                if e_doente(q_espera[k]) == nome_paciente:
                    indice_na_fila = k
                    encontrou = True
                else:
                    k = k + 1
            
            if encontrou == True:
                q_espera.pop(indice_na_fila)
                label_tri = ["T0", "T1", "T2", "T3"][e_triagem(evento)]
                historial.append({
                    "tempo": round(tempo_atual, 1), "evento": "DESISTÊNCIA", 
                    "doente": nome_paciente, "medico": "---", "triagem": label_tri
                })
            
        elif tipo_ev == SAIDA: 
            for m in medicos:
                if m[2] == e_doente(evento):
                    m[3] += (tempo_atual - m[4]) 
                    m[1] = False 
                    m[2] = None
                    label_tri = ["T0", "T1", "T2", "T3"][e_triagem(evento)]
                    historial.append({
                        "tempo": round(tempo_atual, 1), "evento": "ALTA", 
                        "doente": e_doente(evento), "medico": m[0], "triagem": label_tri
                    })

        for m in medicos:
            if m[1] == False: 
                j = 0
                atribuiu = False 
                
                while j < len(q_espera) and atribuiu == False:
                    p = q_espera[j] 
                    compativel = False
                    
                    if m[6] == True: 
                        compativel = True
                    elif m[5] == e_especialidade(p): 
                        compativel = True
                    
                    if compativel:
                        paciente = q_espera.pop(j) 
                        
                        tempo_espera = tempo_atual - e_chegada_original(paciente)
                        tri = e_triagem(paciente)
                        esp_nome = e_especialidade(paciente)
                        
                        h_esp[tri].append(tempo_espera) 
                        h_atend[tri] = h_atend[tri] + 1
                        
                        k = 0
                        while k < len(ESPECIALIDADES):
                            if ESPECIALIDADES[k] == esp_nome: 
                                h_esp_atend[k] = h_esp_atend[k] + 1
                            k = k + 1 
                        
                        m[1] = True 
                        m[2] = e_doente(paciente) 
                        m[4] = tempo_atual 
                        
                        duracao = gera_tempo_consulta(tri)
                        tempo_saida = tempo_atual + duracao
                        novo_ev = (tempo_saida, SAIDA, e_doente(paciente), tri, esp_nome, e_chegada_original(paciente))
                        q_eventos = enqueue(q_eventos, novo_ev)
                        
                        label_tri = ["T0", "T1", "T2", "T3"][tri]
                        historial.append({
                            "tempo": round(tempo_atual, 1), "evento": "CONSULTA", 
                            "doente": e_doente(paciente), "medico": m[0], "triagem": label_tri
                        })
                        atribuiu = True 
                    else: 
                        j = j + 1

        ocupados = 0
        for md in medicos:
            if md[1]: 
                ocupados = ocupados + 1
            
        h_tempo.append(tempo_atual)
        h_fila.append(len(q_espera))
        h_ocup.append((ocupados / NUM_MEDICOS) * 100)

    return h_tempo, h_fila, h_ocup, h_esp, h_atend, medicos, tempo_atual, h_esp_atend, historial