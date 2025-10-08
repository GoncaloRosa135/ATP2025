###funções
MainList=[]
import random

def criaLista(N):
    global MainList
    MainList=[] ###variavel interna
    n = 1
    while n <= N:
        n = n + 1
        MainList.append(random.randrange(1,101))
    return MainList



def leLista(N):
    global MainList
    MainList=[] ###variavel interna
    k = 0
    while k < N:
        k = k + 1
        MainList.append(int(input("introduza um número"))) 
    return MainList


def somaLista(N):
        global MainList
        soma = 0
        for n in N:
            soma = soma + n             
        return (soma)

def mediaLista(N):
        global MainList
        soma = 0
        for n in N:
            soma = soma + n             
        return (soma/len(MainList))

def maiorLista(N):
        global MainList
        maior=N[0]
        for x in N:
                if x>maior:
                    maior=x
        return maior
        
def menorLista(N):
        global MainList
        menor=N[0]
        for x in N:
                if x<menor:
                    menor=x
        return menor

def estaOrdenadaC(N):
        global MainList
        for i in range(len(N) - 1):
            if N[i] > N[i + 1]:
                return "Não"
        return "Sim"

def estaOrdenadaD(N):
        global MainList
        for i in range(len(N) - 1):
            if N[i] < N[i + 1]:
                return "Não"
        return "Sim"



def indiceDe(N, elem):
    cond=-1
    if elem in N:
        cond=N.index(elem)+1
    return cond






modo=-1

while modo != 0:
    modo = int(input("""Crie uma aplicação em Python que coloca no monitor o seguinte menu:\n(1) Criar Lista\n(2) Ler Lista\n(3) Soma\n(4) Média\n(5) Maior\n(6) Menor\n(7) estaOrdenada por ordem crescente\n(8) estaOrdenada por ordem decrescente\n(9) Procura um elemento\n(0) Sair"""))
    
    if modo == 1:
        print(criaLista(int(input("Intoduza o total de números que quer na lista"))))
        

    elif modo == 2:
        
        print(leLista(int(input("Intoduza o total de números que quer na lista"))))
    
    
    elif modo == 3:
        
        print(somaLista(MainList))

    elif modo == 4:
        
        print(mediaLista(MainList))

    elif modo == 5:
                 
        print(maiorLista(MainList))
    elif modo == 6:
        
        print(menorLista(MainList))
    elif modo == 7:
        resultado=estaOrdenadaC(MainList)
        print(resultado)
    elif modo == 8:
        resultado2=estaOrdenadaD(MainList)
        print(resultado2)
    elif modo == 9:
        print(MainList)
        print(indiceDe(MainList,int(input("procura um número"))))
