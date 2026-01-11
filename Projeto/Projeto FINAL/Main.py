import FreeSimpleGUI as sg
import Base
import Gráficos
import Interface
import Login

def calcular_media(lista):
    resultado = 0
    if lista and len(lista) > 0:
        soma = sum(lista)
        total = len(lista)
        resultado = soma / total
    return resultado

def calcular_media_de_listas(lista_de_listas):
    soma = 0
    count = 0
    
    i = 0
    while i < len(lista_de_listas):
        l = lista_de_listas[i]
        soma = soma + sum(l)
        count = count + len(l)
        i = i + 1
    
    media = 0
    if count > 0:
        media = soma / count
    return media

def executar_app(user):
    window = Interface.criar_janela_principal(user['nome'])
    dados_simulacao = None
    
    executando = True
    
    while executando == True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED:
            executando = False
            
        elif event == '-EXIT-':
            sg.popup(f"Aplicação encerrada com sucesso.\nAté à próxima, {user['nome']}!", title="Saída", keep_on_top=True)
            executando = False
        
        elif event == '-RUN-':
            valido = False
            
            if values['-NUM_MED-'].isdigit():
                if values['-TAXA-'].isdigit():
                    if values['-TEMPO-'].isdigit():
                        valido = True
            
            if valido == True:
                window['-STATUS_BOX-'].update(">> A inicializar motores de simulação...\n>> A processar dados estocásticos...")
                window['-PROG-'].update(visible=True, current_count=30)
                window.refresh()

                Base.NUM_MEDICOS = int(values['-NUM_MED-'])
                Base.TAXA_CHEGADA = int(values['-TAXA-']) / 60
                Base.TEMPO_SIMULACAO = int(values['-TEMPO-'])
                Base.TIPO_DISTRIBUICAO = values['-DIST-']

                window['-PROG-'].update(current_count=60)
                
                dados_simulacao = Base.simula()

                total_atend = 0
                
                if isinstance(dados_simulacao[0], int):
                    total_atend = dados_simulacao[0]
                else:
                    total_atend = sum(dados_simulacao[4])
                    
                m_fila = calcular_media(dados_simulacao[1])
                m_ocup = calcular_media(dados_simulacao[2])
                m_esp_glob = calcular_media_de_listas(dados_simulacao[3])

                historial = dados_simulacao[8]

                window['-PROG-'].update(current_count=100)
                msg = f"SIMULAÇÃO CONCLUÍDA ({Base.TIPO_DISTRIBUICAO})!\n"
                msg += f"--------------------------------------------------\n"
                msg += f"Doentes atendidos: {total_atend}\n"
                msg += f"Média Fila:      {round(m_fila, 1)} doentes\n"
                msg += f"Média Espera:    {round(m_esp_glob, 1)} min\n"
                msg += f"Taxa Ocupação:   {round(m_ocup, 1)} %\n"
                msg += f"\n>> LOG RÁPIDO (Últimos eventos):\n"
                
                ultimos = []
                if len(historial) >= 3:
                    ultimos = historial[-3:]
                else:
                    ultimos = historial
                
                idx = 0
                while idx < len(ultimos):
                    u = ultimos[idx]
                    msg += f"[{u['tempo']}m] {u['evento']} - {u['doente']} ({u['triagem']})\n"
                    idx = idx + 1

                window['-STATUS_BOX-'].update(msg)
                
                window['-LOG-'].update(disabled=False)
                window['-SHOW_GRAF-'].update(disabled=False)
                window['-TIME-'].update(disabled=False)
            
            else:
                window['-STATUS_BOX-'].update("⚠️ ERRO CRÍTICO: Insira apenas números inteiros nos parâmetros.")

        elif event == '-SHOW_GRAF-':
            escolha = values['-COMBO_GRAF-']
            
            if "1." in escolha:
                Gráficos.graf_1_media_triagem(dados_simulacao)
            elif "2." in escolha:
                Gráficos.graf_2_volume_triagem(dados_simulacao)
            elif "3." in escolha:
                Gráficos.graf_3_evolucao_fila(dados_simulacao)
            elif "4." in escolha:
                Gráficos.graf_4_taxa_ocupacao(dados_simulacao)
            elif "5." in escolha:
                Gráficos.graf_5_impacto_chegada(dados_simulacao)
            elif "6." in escolha:
                Gráficos.graf_6_especialidades(dados_simulacao)
            elif "7." in escolha:
                Gráficos.graf_7_eficiencia(dados_simulacao)
            elif "8." in escolha:
                Gráficos.graf_8_evolucao_desistencias(dados_simulacao)

        elif event == '-LOG-':
            raw_hist = dados_simulacao[8]
            dados_formatados = []
            
            k = 0
            while k < len(raw_hist):
                h = raw_hist[k]
                medico = h.get('medico', '---')
                triagem = h.get('triagem', '---')
                
                dados_formatados.append([h['tempo'], h['evento'], h['doente'], medico, triagem])
                k = k + 1
                
            Interface.janela_log_popup(dados_formatados)

        elif event == '-TIME-':
            lista_medicos = dados_simulacao[5]
            tempo_total = dados_simulacao[6]
            dados_formatados = []
            
            j = 0
            while j < len(lista_medicos):
                m = lista_medicos[j]
                nome = m[0]
                tempo_trab = m[3]
                espec = m[5]
                
                perc = 0
                if tempo_total > 0:
                    perc = (tempo_trab / tempo_total) * 100
                    
                dados_formatados.append([nome, espec, round(tempo_trab, 1), f"{round(perc, 1)}%"])
                j = j + 1
            
            Interface.janela_medicos_popup(dados_formatados)

    window.close()

if __name__ == "__main__":
    usuario = Login.executar_login_controller()
    if usuario:
        executar_app(usuario)