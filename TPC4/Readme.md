sala1=("Sala 1",100,[],"Twilight")
sala2=("Sala 2",80,[],"Hannibal")
sala3=("Sala 3",120,[],"Interstellar")
Cinema=[sala1,sala2,sala3]

import random

def listar(cinema):
    print("Filmes:")
    for sala in cinema:
        print(sala[0]+str(": ")+sala[3])
    return


def disponivel(cinema,filme,lugar):
    disponibilidade=False
    for sala in cinema:
        if filme == sala[3] and lugar not in sala[2]:
            disponibilidade=True
    return disponibilidade

def vendeBilhetes(cinema,filme,escolha):
    if escolha=="Sim":
        for sala in cinema:
            if filme==sala[3]:
                lugar=int(input("Escolha o lugar que deseja reservar:"))
                if disponivel(cinema,filme,lugar):
                    sala[2].append(lugar)
                    print("O lugar ",str(lugar)," foi reservado com sucesso.")
                    print(sala)
                else:
                    print("Este lugar já se encontra ocupado, por favor escolha outro.")
    
    if escolha=="Não":
        for sala in cinema:
            if filme==sala[3]:
                res = ""
                while res != "aceite":
                    lugar = random.randrange(1,sala[1]+1) 
                    if disponivel(Cinema, filme, lugar): 
                        sala[2].append(lugar)
                        print("O lugar "+str(lugar)+" foi reservado com sucesso, bom filme!")
                        print(sala)
                        res = "aceite"
                    else:
                        res = "recusado"

def listarDisponibilidades(Cinema):
    print("Estes são os filmes disponiveis no cinema:")
    for sala in Cinema:
        x= sala[1] - len(sala[2]) 
        
        print(sala[0] + ", com "+str(x)+" lugares disponiveis.")
    return
        
def inserirSala( Cinema, sala, lotação, filme ):
    sala=[sala,lotação,[],filme]
    
    if sala not in Cinema:
        Cinema.append(sala)
        print("A sala foi adicionada com sucesso!")
        print(sala[0]+": com lotação de "+str(sala[1])+" lugares. Filme em exibição: "+sala[3])
    else:
        print("A sala já existe.")
    




menu=-1
print("""Olá! Obrigado por escolher o nosso Cinema, o que deseja fazer? 
      (1) Listar todos os filmes em exibição;
      (2) Verificar a disponibilidade da sala e do lugar;
      (3) Comprar bilhete;
      (4) Listar os lugares restantes em cada sala;
      (5) Adicionar uma sala ao cinema;
      (6) Fechar o menu.""")
while menu !=6:
    menu=int(input("Escolhe a tua opção."))

    if menu==1:
        listar(Cinema)

    elif menu ==2:
        print(disponivel(Cinema,input("Escolhe o filme que queres ver"),int(input("Escolhe um lugar da sala"))))

    elif menu ==3:
        vendeBilhetes(Cinema,input("Escolhe o filme que queres ver"), input("Deseja escolher o lugar?(Sim ou Não)"))

    
    elif menu ==4:
        listarDisponibilidades(Cinema)

    elif menu ==5:
        inserirSala(Cinema,input("Qual o nome da nova sala?"),int(input("Qual a lotação da sala?")),input(("Qual o filme em exibição?")))
    
print("Obrigado e volte sempre!")
