import matplotlib.pyplot as plt
import Base 

LABELS_TRI = ['Normal', 'Pouco Urg.', 'Urgente', 'Emergência']
CORES_NEON = ['#00f2c3', '#f1c40f', '#fd7e14', '#ff005c'] 

def aplicar_tema():
    plt.style.use('default')
    
    plt.rcParams['figure.facecolor'] = '#212529'
    plt.rcParams['axes.facecolor'] = '#2c3e50'
    
    plt.rcParams['axes.edgecolor'] = '#ecf0f1'
    plt.rcParams['axes.labelcolor'] = 'white'
    plt.rcParams['text.color'] = 'white'
    plt.rcParams['xtick.color'] = 'white'
    plt.rcParams['ytick.color'] = 'white'
    
    plt.rcParams['grid.color'] = 'white'
    plt.rcParams['grid.alpha'] = 0.15
    
    plt.rcParams['font.weight'] = 'bold'
    plt.rcParams['legend.facecolor'] = '#2c3e50'
    plt.rcParams['legend.edgecolor'] = 'white'

def adicionar_valores(barras, decimais):
    i = 0
    while i < len(barras):
        b = barras[i]
        altura = b.get_height()
        
        if decimais == 0:
            texto = str(int(altura))
        else:
            texto = str(round(altura, decimais))
            
        if altura >= 0:
            plt.text(
                b.get_x() + b.get_width()/2, 
                altura, 
                texto, 
                ha='center', va='bottom', 
                color='white', fontweight='bold', fontsize=11
            )
        i = i + 1

def desembrulhar_seguro(dados):
    res = ([], [], [], [[],[],[],[]], [0,0,0,0], [], 0, [], [])
    
    if dados != None:
        if len(dados) >= 9:
            res = dados    
    return res

def graf_1_media_triagem(dados_raw):
    aplicar_tema()
    d = desembrulhar_seguro(dados_raw)
    esperas = d[3]
    medias = []
    
    i = 0
    while i < len(esperas):
        lista = esperas[i]
        media = 0
        if len(lista) > 0:
            media = sum(lista) / len(lista)
        medias.append(media)
        i = i + 1

    plt.figure("1. Médias Espera", figsize=(10, 6))
    barras = plt.bar(LABELS_TRI, medias, color=CORES_NEON, edgecolor='white')
    plt.title("TEMPO MÉDIO DE ESPERA (MIN)", color='#00f2c3')
    adicionar_valores(barras, 1)
    plt.tight_layout()
    plt.show()

def graf_2_volume_triagem(dados_raw):
    aplicar_tema()
    d = desembrulhar_seguro(dados_raw)
    volumes = d[4]
    
    plt.figure("2. Volume Total", figsize=(10, 6))
    barras = plt.bar(LABELS_TRI, volumes, color=CORES_NEON, edgecolor='white')
    plt.title("TOTAL DE PACIENTES ATENDIDOS", color='#f1c40f')
    adicionar_valores(barras, 0)
    plt.tight_layout()
    plt.show()

def graf_3_evolucao_fila(dados_raw):
    aplicar_tema()
    d = desembrulhar_seguro(dados_raw)
    
    plt.figure("3. Evolução Fila", figsize=(10, 5))
    plt.plot(d[0], d[1], color='#00f2c3', linewidth=2)
    plt.fill_between(d[0], d[1], color='#00f2c3', alpha=0.1)
    plt.title("TAMANHO DA FILA EM TEMPO REAL", color='#00f2c3')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def graf_4_taxa_ocupacao(dados_raw):
    aplicar_tema()
    d = desembrulhar_seguro(dados_raw)
    
    plt.figure("4. Ocupação", figsize=(10, 5))
    plt.plot(d[0], d[2], color='#ff005c', linewidth=2)
    plt.axhspan(80, 110, color='#fd7e14', alpha=0.2, label='Zona Crítica')
    plt.title("TAXA DE OCUPAÇÃO DA EQUIPA (%)", color='#ff005c')
    plt.legend()
    plt.ylim(0, 110)
    plt.tight_layout()
    plt.show()

def graf_5_impacto_chegada(dados_raw):
    aplicar_tema()
    
    plt.figure("5. Stress Test", figsize=(10, 5))
    taxas = [10, 20, 30, 40, 50]
    medias_fila = []
    
    original = Base.TAXA_CHEGADA
    
    i = 0
    while i < len(taxas):
        Base.TAXA_CHEGADA = taxas[i] / 60
        r = Base.simula()
        fila = r[1]
        
        media = 0
        if len(fila) > 0:
            media = sum(fila) / len(fila)
        medias_fila.append(media)
        
        i = i + 1
        
    Base.TAXA_CHEGADA = original
    
    plt.plot(taxas, medias_fila, marker='o', color='#f1c40f', linestyle='-')
    plt.title("IMPACTO DO FLUXO NA FILA", color='#f1c40f')
    plt.ylabel("Média na Fila")
    plt.xlabel("Pacientes/Hora")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def graf_6_especialidades(dados_raw):
    aplicar_tema()
    d = desembrulhar_seguro(dados_raw)
    contagens = d[7]
    nomes = Base.ESPECIALIDADES

    plt.figure("6. Especialidades", figsize=(11, 6))
    
    if len(contagens) > 0:
        nomes_usar = nomes[0:len(contagens)]
        barras = plt.bar(nomes_usar, contagens, color='#3a7bd5', edgecolor='white')
        plt.title("CONSULTAS POR ÁREA MÉDICA", color='#3a7bd5')
        plt.xticks(rotation=15)
        adicionar_valores(barras, 0)
        
    plt.tight_layout()
    plt.show()

def graf_7_eficiencia(dados_raw):
    aplicar_tema()
    d = desembrulhar_seguro(dados_raw)
    lista_m = d[5]
    tempo_f = d[6]
    
    plt.figure("7. Eficiência", figsize=(8, 6))
    
    if len(lista_m) > 0:
        if tempo_f > 0:
            s_esp = 0
            c_esp = 0
            s_res = 0
            c_res = 0
            
            i = 0
            while i < len(lista_m):
                m = lista_m[i]
                rendimento = (m[3] / tempo_f) * 100
                
                if m[6] == True: 
                    s_res = s_res + rendimento
                    c_res = c_res + 1
                else: 
                    s_esp = s_esp + rendimento
                    c_esp = c_esp + 1
                i = i + 1
            
            media_esp = 0
            if c_esp > 0: 
                media_esp = s_esp / c_esp
                
            media_res = 0
            if c_res > 0: 
                media_res = s_res / c_res
            
            barras = plt.bar(['Especialistas', 'Reservas'], [media_esp, media_res], 
                             color=['#3a7bd5', '#2ecc71'], width=0.5, edgecolor='white')
            
            plt.axhspan(80, 110, color='#fd7e14', alpha=0.2, label='Zona Crítica (>80%)')
            plt.title("OCUPAÇÃO MÉDIA POR TIPO (%)", color='#2ecc71')
            plt.ylim(0, 110)
            adicionar_valores(barras, 1)
            plt.legend(loc='upper left')
        
    plt.tight_layout()
    plt.show()

def graf_8_evolucao_desistencias(dados_raw):
    aplicar_tema()
    d = desembrulhar_seguro(dados_raw)
    historial = d[8]
    
    tempos = [0]
    total_acumulado = [0]
    contador = 0
    
    i = 0
    while i < len(historial):
        evento = historial[i]
        
        if evento['evento'] == "DESISTÊNCIA":
            tempo = evento['tempo']
            contador = contador + 1
            
            tempos.append(tempo)
            total_acumulado.append(contador)
            
        i = i + 1
        
    plt.figure("8. Evolução Desistências", figsize=(10, 5))
    
    plt.plot(tempos, total_acumulado, color='#e74c3c', linewidth=2, marker='o', markersize=4)
    plt.fill_between(tempos, total_acumulado, color='#e74c3c', alpha=0.1)
    
    plt.title("EVOLUÇÃO CUMULATIVA DE DESISTÊNCIAS", color='#e74c3c')
    plt.ylabel("Total de Pessoas que Saíram")
    plt.xlabel("Tempo de Simulação (min)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()