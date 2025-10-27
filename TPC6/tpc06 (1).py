
tabMeteo1 = [((2022,1,20), 2, 16, 0),((2022,1,21), 1, 13, 0.2), ((2022,1,22), 7, 17, 0.01)]

def medias(tabMeteo):
    res = []
    for dia in tabMeteo:
        tmax = dia[2]        
        tmin = dia [1]
        data = dia [0]
        media = (tmin + tmax)/2
        tuplo = (data,media)
        res.append(tuplo)
    return res 



def guardaTabMeteo(t, fnome): 
    file = open(fnome, "w")
    for data, tmin, tmax, prec in t:
        ano, mes, dia = data
        file.write(f"{ano}-{mes}-{dia}; {tmin}; {tmax};{prec}\n")
    
    file.close()
    return



def carregaTabMeteo(fnome):
    res = []
    file = open(fnome, "r")
    for line in file:
        line = line.strip()    
        campos = line.split(";")
        print(campos)
        data, tmin, tmax , prec =campos
        ano, mes, dia = data.split("-")
        tuplo = ((int(ano), int(mes), int(dia)), float(tmin), float(tmax) ,float(prec))
        res.append(tuplo)
    file.close()
    return res



def minMin(tabMeteo1):

    i = 0
    min_temp = tabMeteo1[0][1]

    while i < len(tabMeteo1):
        if tabMeteo1[i][1] < min_temp:
            min_temp = tabMeteo1[i][1]
        i += 1
    return min_temp




def amplTerm(tabMeteo):
    res = []
    for dia in tabMeteo:
        tmax = dia[2]        
        tmin = dia [1]
        data = dia [0]
        amplTerm = (tmax - tmin)
        list = [(data,amplTerm)]
        res.append(list)
    return res 



def maxChuva(tabMeteo):
    i = 0
    max_prec = tabMeteo[0][3]  
    max_data = tabMeteo[0][0]  
    while i < len(tabMeteo): 
        if tabMeteo[i][3] > max_prec:
            max_prec = tabMeteo[i][3]
            max_data = tabMeteo[i][0]
        i += 1

    return (max_data, max_prec)



def diasChuvosos(tabMeteo, p):
    res = []
    for registo in tabMeteo: 
        data = registo[0]
        precipitacao = registo[3]
        if precipitacao > p:
            res.append((data, precipitacao))
    return res
    

tabMeteo3 = [((2022,1,20), 2, 16, 0), ((2022,1,21), 1, 13, 0.2), ((2022,1,23), 6, 19, 0.6), ((2022,1,24), 3, 18, 0.8),((2022,2,20), 6, 19, 0.2), ((2022,2,24), 3, 18, 0.2), ((2022,2,28), 3, 18, 0.2)]




def maxPeriodoCalor(tabMeteo, p):
    maior = 0
    atual = 0
    for dia in tabMeteo:
        prec = dia[3]
        if prec < p:
            atual += 1
            if atual > maior:
                maior = atual
        else:
            atual = 0

    return maior

tabMeteo1 = [((2022,1,20), 2, 16, 0), ((2022,1,21), 1, 13, 0.2), ((2022,1,22), 7, 17, 0.01)]
           



from matplotlib import pyplot as plt

def grafTabMeteo(t):
    x= [f"{data[0]} - {data[1]} - {data[2]}"for data, tmin, tmax , prec in t]
    ytmin = [ tmin for data, tmin, tmax, prec in t]
    ytmax = [ tmax for data, tmin, tmax, prec in t]

    y_prec = [prec for *_ , prec in t]
    
    plt.plot(x,ytmin, label = "Temperatura mínima (ºC)", color="blue", marker ="o")
    plt.plot(x,ytmax, label = "Temperatura máxima (ºC)", color="red", marker = "o")
    plt.legend()
    plt.title("Tabela Metereológica")
    plt.grid()
    plt.xticks(rotation=45)
    plt.show()

    plt.bar(x, y_prec, label = "Pluvisiosidade (mm)", color="c")
    plt.legend()
    plt.grid()
    plt.xticks(rotation=45)
    plt.show()
    return



menu = -1
print("""Estas são as opções:
(1)- Calcula temp média de cada dia;
(2)- Função para guardar tabela metereológica num ficheiro de texto;
(3)- Função para carregar uma tabela meteorológica de um ficheiro de texto;
(4)- Calcula temp mínima mais baixa registada na tabela;
(5)- Calcula a amplitude térmica de cada dia;
(6)- Calcula o dia em que a precipitação registada teve o seu valor máximo;
(7)- Define uma função que recebe uma tabela meteorológica e um limite `p` e retorna uma lista de pares [(data, precipitação)] correspondente aos dias em que a precipitação foi superior a `p`;
(8)- Define uma função que recebe uma tabela meteorológica e um limite `p` e retorna o maior número consecutivo de dias com precipitação abaixo desse limite;
(9)- Define uma função que recebe uma tabela meteorológica e desenha os gráficos da temperatura mínima, máxima e de pluviosidade;
(0)- Sair da aplicação""")

while menu != 0:
    menu = int(input("Escolhe a tua opção: "))
    if menu == 0:
        print("Saíste da aplicação!!!")
    elif menu == 1:
        medias(tabMeteo1)
        print(medias(tabMeteo1))
    elif menu == 2:
        guardaTabMeteo(tabMeteo1, "meteorologia.txt")
        print("Arquivo guardado com sucesso!")
    elif menu == 3:
        print(carregaTabMeteo("meteorologia.txt"))
    elif menu== 4:
        minMin(tabMeteo1)
        print(minMin(tabMeteo1))
    elif menu==5:
        amplTerm(tabMeteo1)
        print(amplTerm(tabMeteo1))
    elif menu==6:
        maxChuva(tabMeteo1)
        print(maxChuva(tabMeteo1))
    elif menu==7:
        print(diasChuvosos(tabMeteo3, 0.5))
    elif menu==8:
        print(maxPeriodoCalor(tabMeteo1, 0.05))

    elif menu==9:
        grafTabMeteo(tabMeteo3)

    else:
        print("Tenta escolher um número do menu :)")

