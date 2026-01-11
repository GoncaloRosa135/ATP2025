import json
import FreeSimpleGUI as sg
import Interface

def ler_utilizadores():
    f = open("utilizadores.json", "r", encoding="utf-8")
    dados = json.loads(f.read())
    f.close()
    return dados

def gravar_utilizadores(bd):
    f = open("utilizadores.json", "w", encoding="utf-8")
    json.dump(bd, f, indent=4)
    f.close()

def validar_login(bd, u_input, p_input):
    usuario_encontrado = None
    for u in bd:
        if u['id'] == u_input and u['password'] == p_input:
            usuario_encontrado = u      
    return usuario_encontrado


def executar_login_controller():
    window = Interface.criar_janela_login()
    usuario_logado = None
    condi=True
    
    while condi:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            condi=False
        elif event == '-OK-':
            bd = ler_utilizadores()
            user = validar_login(bd, values['-USER-'], values['-PASS-'])
            if user:
                usuario_logado = user
                condi=False 
            else:
                window['-MSG-'].update("Credenciais inválidas.")
        elif event == '-REG-':
            w_reg = Interface.criar_janela_registo()
            e_reg, v_reg = w_reg.read()
            if e_reg == "Salvar":
                if v_reg['-NU-'] != "" and v_reg['-NP-'] != "":
                    bd = ler_utilizadores()
                    existe = False
                    for u in bd:
                        if u['id'] == v_reg['-NU-']: 
                            existe = True
                    if not existe:
                        bd.append({'id': v_reg['-NU-'], 'password': v_reg['-NP-'], 'nome': v_reg['-NN-']})
                        gravar_utilizadores(bd)
                        sg.popup_quick_message("Conta criada! Pode entrar.")
                    else:
                        sg.popup_error("Esse ID já existe.")
            w_reg.close()
    window.close()
    return usuario_logado