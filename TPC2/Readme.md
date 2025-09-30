import random
print("Olá, bem vindo ao jogo dos fósforos, existem 21 fósforos ao todo, podes tirar entre 1 e 4 fósforos de cada vez, quem tirar o último perde ")
jogar= int(input("Quem será o primeiro a jogar? 1=jogador, 2=computador: "))
soma = 21

while jogar not in [1, 2]:
        jogar = int(input("Escolha inválida. Quem será o primeiro a jogar? 1=jogador, 2=computador: "))

if jogar == 1:
    while soma > 1:
        n = int(input("Quantos fósforos quer retirar?"))
        while n<1 or n>4 or n>soma:
            print("Número fora do intervalo de valores, escolhe um número entre 1 e 4 e menor ou igual aos restantes.")
            n = int(input("Quantos fósforos quer retirar?"))
        soma -= n 
        print(f"Tiraste {n} fósforos, faltam {soma}.")
        if soma == 1:
            print("Parabéns, ganhaste o jogo!")
            break
        comp = min(5-n,soma-1)
        soma -= comp
        print(f"o computador tirou {comp} fósforos. Faltam {soma}.")
        if soma == 1:
            print(f"Perdeste o jogo, o computador ganhou.")
            break
else:
    comp = random.randint(1,4)
    soma -= comp
    print(f"O computador retirou {comp} fósforos, ainda restam {soma}")
    while soma>1:
        n = int(input("Quantos fósforos queres retirar?"))
        while n<1 or n>4 or n>soma:
            print("Número fora do intervalo de valores, escolhe um número entre 1 e 4 e menor ou igual aos restantes.")
            n = int(input("Quantos fósforos quer retirar?"))
        soma -= n
        if soma == 1:
            print("Ganhaste, o computados perdeu!")
            break
        if soma % 5 !=1:
            comp = (soma - 1) % 5
            if comp == 0:
                comp= random.randint(1,min(4,soma - 1))
        else:
            comp = random.randint(1,min(4,soma-1))
        soma -= comp
        print(f"O computador retirou {comp} fósforos. Faltam {soma} fósforos")
        if soma ==1:
            print("Perdeste o jogo, o computador ganhou!")
            break

