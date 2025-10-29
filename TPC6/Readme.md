from matplotlib import pyplot as plt
tabMeteo = [((2022,1,20), 2, 16, 0), ((2022,1,21), 1, 13, 0.2), ((2022,1,23), 6, 19, 0.6), ((2022,1,24), 3, 18, 0.8),((2022,2,20), 6, 19, 0.2), ((2022,2,24), 3, 18, 0.2), ((2022,2,28), 3, 18, 0.2)]

def medias(tabMeteo):
    res = []
    for data, tmin, tmax, prec in tabMeteo:
        media = (tmin + tmax)/2
        res.append((data,media))
    return res

def guardaTabMeteo(t, fnome):
    f = open(fnome, "w")

    for data, tmin, tmax, prec in t:
        ano, mes, dia = data
        f.write(f"{ano}-{mes}-{dia};{tmin};{tmax};{prec}\n")

    f.close()
    return

guardaTabMeteo(tabMeteo, "meteorologia.txt")

def carregaTabMeteo(fnome):
    res = []
    file = open(fnome,"r")
    for line in file:
        #line=line[:-1]
        line = line.strip("\n")
        print(line)
        campos = line.split(";")
        data, tmin, tmax, prec = campos
        ano, mes, dia = data.split("-")
        tuplo = ((int(ano),int(mes),int(dia)), float(tmin), float(tmax), float(prec))
        res.append(tuplo)
    file.close()
    return res


def minMin(tabMeteo):
    minima = tabMeteo[0][1]
    for i in tabMeteo:
        if i[1]<minima:
            minima=i[1]
    return minima

def amplTerm(tabMeteo):
    res = []
    for i in tabMeteo:
        data,tmin,tmax,prec=i
        amplitude = tmax-tmin
        res.append((data,amplitude))
    return res

def maxChuva(tabMeteo):
    max_prec=tabMeteo[0][3]
    for i in tabMeteo:
        if i[3]>max_prec:
            max_prec = i[3]
            max_dia = i[0]

    return (max_dia,max_prec)

def diasChuvosos(tabMeteo,p):
    res = []
    for i in tabMeteo:
        if i[3]>p:
            res.append((i[0],i[3]))
    return res

def maxPeriodoCalor(tabMeteo,p):
    res = 0
    for i in tabMeteo:
        if i[3]<p:
            res = res + 1
        else:
            res = 0
    return res

def grafTabMeteo(t):
    x = [f"{data[0]}-{data[1]}-{data[2]}"for data, tmin, tmax, prec in t]
    ytmin = [tmin for data, tmin, tmax, prec in t]
    ytmax = [tmax for data, tmin, tmax, prec in t]

    y_prec = [prec for *_, prec in t]
  
    plt.plot(x,ytmin, label= "Temperatura mínima (ºC)", color="blue", marker = "o")
    plt.plot(x,ytmax, label= "Temperatura máxima (ºC)", color="red",marker="o")
    plt.legend()
    plt.title("Tabela Meteorológica")
    plt.grid()
    plt.xticks(rotation=45)
    plt.show()

    plt.bar(x, y_prec, label = "Pluviosidade (mm)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()
    return

modo=-1
print("""\n----Aplicação Meteorológica----
    1---> Temperatura média de cada dia
    2---> Temperatura mínima absoluta
    3---> Amplitude térmica
    4---> Dia em que a precipitação foi máxima
    5---> Dias em que a precipitação foi maior que um limite p
    6---> Dias consecutivos com precipitação abaixo de um limite p
    7---> Guardar Tabela num ficheiro
    8---> Carregar Tabela de um ficheiro
    9--> Mostrar Gráfico
    0--->Sair""")


while modo != 0:
    modo = int(input("Escolha uma opção:"))
    if modo == 1:
        print("Temperatura média de cada dia: ",medias(tabMeteo))

    elif modo == 2:    
        print("A temperatura mínima absoluta é: ",minMin(tabMeteo))
    
    elif modo == 3:
        print("A amplitude térmica é: ", amplTerm(tabMeteo))

    elif modo == 4:
        print("A precipitação foi máxima em: ",maxChuva(tabMeteo))

    elif modo == 5:      
        p=float(input("Introduza o limite de precipitação a considerar:"))
        print(f"Dias com precipitação maior que {p}: ",diasChuvosos(tabMeteo,p))

    elif modo == 6:
        p=float(input("Introduza o limite de precipitação a considerar:"))
        print(f"Houve {maxPeriodoCalor(tabMeteo,p)} dias consecutivos com limite de precipitação abaixo de {p}.")

    elif modo == 7:
         fnome = input("Nome do ficheiro: ")
         guardaTabMeteo(tabMeteo,fnome)
         print("TAbela guardada com sucesso!")

    elif modo == 8:
        fnome=input("Nome do ficheiro: ")
        tabMeteo=carregaTabMeteo(fnome)
        print("Tabela carregada com sucesso!")

    elif modo == 9:
        grafTabMeteo(tabMeteo)
