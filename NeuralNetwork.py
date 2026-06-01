import sys
import math
import random
import numpy as np

class Node:
    
    def __init__(self, name: str, izlaz: int, w0: int, tezine: list):
        self.name = name
        self.izlaz = izlaz
        self.w0 = w0
        self.tezine = tezine
    
    def __str__(self):
        return self.name    

def sigmoidFunction(net: list):
    y_evi = []
    for node in net:
        y_evi.append(1 / (1 + math.exp(-node)))
    return y_evi

def mean_square_function(network_test_and_real_values: list) -> float:
    error = 0.0
    for pair in network_test_and_real_values:
        error += (pair[0] - pair[1])**2
    return error / len(network_test_and_real_values)


def stvori_pocetnu_populaciju(arhitektura, imena):
    
    networkWeights = []
    selfWeights = []
    #print(imena)

    prviSloj = []
    #prviSelfSloj = []
    for x in range(0, len(imena) - 1): #len(imena) - 1
        mySloj = []
        for prviIzlazi in range(0, arhitektura[0]):
            mySloj.append(round(random.uniform(1.0, 2.0), 3))
        prviSloj.append(mySloj)
        #prviSelfSloj.append(round(random.uniform(1.0, 2.0), 3))
    #selfWeights.append(prviSelfSloj)
    networkWeights.append(prviSloj)


    for sloj in range(0, len(arhitektura) - 1): # sloj je broj nodova u tom sloju [5, 2, 3]...
        mySloj = []
        slojSelfTezina = []
        for brojIzlaza in range(1, arhitektura[sloj] + 1): # za svaki od nodova u tom sloju
            randomIzlaz = []
            for nodeIzlaz in range(0, arhitektura[sloj + 1]):    # pogledaj koliko ima nodova u sljedecem sloju
                randomIzlaz.append(round(random.uniform(1.0, 2.0), 3))

            slojSelfTezina.append(round(random.uniform(1.0, 2.0), 3))
            mySloj.append(randomIzlaz)

        selfWeights.append(slojSelfTezina)

        networkWeights.append(mySloj)

    zadnjiSloj = []
    zadnjiSelf = []
    for zadnjiNode in range(0, arhitektura[len(arhitektura) - 1]):
        zadnjiSloj.append([round(random.uniform(1.0, 2.0), 3)])
        zadnjiSelf.append(round(random.uniform(1.0, 2.0), 3))
    networkWeights.append(zadnjiSloj)
    selfWeights.append(zadnjiSelf)
    selfWeights.append([round(random.uniform(1.0, 2.0), 3)])

    #[ [ [1,2,3,4,5], [2,3,5,6,6], [2,3,5,6,6] , [2,3,5,6,6] ], [sloj2], [sloj3] ]
    #print("NETWORK WEIGHTS")
    #for l in networkWeights:
    #    for node in l:
    #        print(node)
    #    print()
    #print("---------------------------------------------------------------")

    #[ [1,2,4,53,2], [5,5,2,7,8,6], [12,5,6,7,77,6], [] ]
    #print("SELF WEIGHTS")
    #for col in selfWeights:
    #    print(col)
    #print()
    
    rezultat = test_network(networkWeights, selfWeights, inputsToTest, trueValues)
    dobrota = dobrota_funkcija(rezultat)
    
    return (networkWeights, selfWeights, dobrota)

# 8000 iter u 2 min

def test_network2(networkWeights, selfWeights, inputsToTest, trueValues):  
    network_predict_and_true_values = []

    for idxTrue, ulaz in enumerate(inputsToTest):
        x_evi = ulaz 

        for idx, column in enumerate(networkWeights):
            net = []

            num_outputs = len(column[0]) 
            num_inputs = len(column)     

            for output_idx in range(num_outputs):
                total = 0.0
                for input_idx in range(num_inputs):
                    total += column[input_idx][output_idx] * x_evi[input_idx]
                total += selfWeights[idx][output_idx]
                net.append(total)

            if idx == len(networkWeights) - 1:
                output_value = float(net[0]) if len(net) == 1 else net
                network_predict_and_true_values.append((output_value, trueValues[idxTrue]))
            else:
                x_evi = sigmoidFunction(net)

    return network_predict_and_true_values



def test_network(networkWeights, selfWeights, inputsToTest, trueValues):  
    #create neural network
    # posto svaka ide u svaku mozemo kao lista listi, umjesto node pa cuvat djecu
    # testiraj network za svaki ulaz
    net = 0.0
    #print("funnkcija:::")
    network_predict_and_true_values = []
    for idxTrue, ulaz in enumerate(inputsToTest):
        #print("ulaz:::", idxTrue)
        x_evi = [ulaz]
        for idx, column in enumerate(networkWeights):
           # print("stupac:::", idx)
            matrica = []
            #print("col", column[idx])
            for brojIzlazaIzTogCvora in range(0, len(column[idx])):
                matrica.append([polje[brojIzlazaIzTogCvora] for polje in column])
            matrica = np.array(matrica)

            net = np.dot(matrica, np.transpose(x_evi[idx])) + np.transpose(selfWeights[idx])

            if idx == len(networkWeights) - 1:
                network_predict_and_true_values.append((float(net[0]), trueValues[idxTrue]))
                break   # kod zadnjeg ne radimo net funkciju nego samo vracamo vrijednosti
            
            y_evi = sigmoidFunction(net)
            x_evi.append(y_evi)
            
    #network_true_values = trueValues
#
    #toReturn = []
    #for i in range(0, len(network_true_values)):
    #    toReturn.append((network_test_values[i], network_true_values[i]))
    ##print(dobrota_funkcija(toReturn))
    return network_predict_and_true_values

def dobrota_funkcija(jedinka: list):
    
    error = mean_square_function(jedinka)
    return 1 / error


def selectEliteJedinke(populacija: list, elitism: int, inputsToTest, trueValues):
    
    dobrota_jedinki = []
    
    for idx, jedinka in enumerate(populacija):
        #print("jedinka", populacija)
        #rezultat = test_network(jedinka[0], jedinka[1], inputsToTest, trueValues)
        dobrota_jedinki.append(jedinka[2])
    
    najbolje_jedinke_idx = sorted(range(len(dobrota_jedinki)), key=lambda i: dobrota_jedinki[i])[-elitism:]
    najbolje_jedinke = []
    for i in najbolje_jedinke_idx:
        najbolje_jedinke.append(populacija[i])

    return najbolje_jedinke #najbolje_jedinke_idx


def selectParents(populacija: list, inputsToTest, trueValues):
    #izaberi na temelju vjerojatnosi od pojedinace / ukupne dobrote
    ukupna_dobrota = 0.0
    dobrota_po_jedinki = []
    
    #random.shuffle(populacija)
    
    for jedinka in populacija:
        ukupna_dobrota += jedinka[2]
        dobrota_po_jedinki.append(jedinka[2])
        
    #for test in testovi:
    #    #print("pojedineee", dobrota_funkcija(test))
    #    dobrota = dobrota_funkcija(test)
    #    ukupna_dobrota += dobrota
    #    dobrota_po_jedinki.append(dobrota)
    
    #print("ukupno ", ukupna_dobrota)
    
    #for test in testovi:
    #    dobrota_po_jedinki.append(dobrota_funkcija(test) / ukupna_dobrota)
    #    print("pojedine", dobrota_funkcija(test) / ukupna_dobrota)
    
    roditelji = []
    for i in range(0, 2):
        random_num = random.uniform(0, ukupna_dobrota)
        perc = 0.0
        chosen = -1
        for idx, dobrota in enumerate(dobrota_po_jedinki):
           perc += dobrota
           if perc >= random_num and chosen != idx:
               #print(f"perc: {perc} || random: {random_num} || DOBROTA: {dobrota}")
               roditelji.append(populacija[idx])
               break
           #else:
               #print(f"perc- NEEE: {perc} || random- NEEE: {random_num} || DOBROTA: {dobrota}")
     
    return roditelji      


def krizanje_i_mutacija(rod1, rod2, p_mut, stddevGauss, inputsToTest, trueValues):
# [ [ [1,2,3,4,5], [2,3,5,6,6], [2,3,5,6,6] , [2,3,5,6,6] ],  [sloj2],  [sloj3] ]
    newWeights = []
    for sloj in range(0, len(rod1[0])):
        slojPuni = []
        for cvor in range(0, len(rod1[0][sloj])):
            izlazniCvor = []
            for izlaz in range(0, len(rod1[0][sloj][cvor])):
                novi = (rod1[0][sloj][cvor][izlaz] + rod2[0][sloj][cvor][izlaz]) / 2
                if random.uniform(0.0, 1.0) <= p_mut:
                    novi += random.normalvariate(0, stddevGauss)
                izlazniCvor.append(novi)
            slojPuni.append(izlazniCvor)   
        newWeights.append(slojPuni)
     
    #[ [1,2,4,53,2], [5,5,2,7,8,6], [12,5,6,7,77,6], [] ]   
    newSelfWeights = []
    for sloj in range(0, len(rod1[1])):
        slojPuni = []
        for nodes in range(0, len(rod1[1][sloj])):
            novi = (rod1[1][sloj][nodes] + rod2[1][sloj][nodes]) / 2  
            if random.uniform(0.0, 1.0) <= p_mut:
                novi += random.normalvariate(0, stddevGauss)
            slojPuni.append(novi)
        newSelfWeights.append(slojPuni)
        
    rezultat = test_network(newWeights, newSelfWeights, inputsToTest, trueValues)
    dobrota = dobrota_funkcija(rezultat)
    
    # 1000 puta brze
    #rezultat = test_network(newWeights, newSelfWeights, inputsToTest, trueValues)
    #dobrota = random.uniform(0,1)
        
    return (newWeights, newSelfWeights, dobrota)


def mutacija(dijete, p_mut, stddevGauss, inputsToTest, trueValues):
    newWeights = []
    for sloj in range(0, len(dijete[0])):
        slojPuni = []
        for cvor in range(0, len(dijete[0][sloj])):
            izlazniCvor = []
            for izlaz in range(0, len(dijete[0][sloj][cvor])):
                if random.uniform(0.0, 1.0) <= p_mut:
                    izlazniCvor.append((dijete[0][sloj][cvor][izlaz] + random.normalvariate(0, stddevGauss)))
                else:
                     izlazniCvor.append(dijete[0][sloj][cvor][izlaz])
            slojPuni.append(izlazniCvor)   
        newWeights.append(slojPuni)
     
    #[ [1,2,4,53,2], [5,5,2,7,8,6], [12,5,6,7,77,6], [] ]   
    newSelfWeights = []
    for sloj in range(0, len(dijete[1])):
        slojPuni = []
        for nodes in range(0, len(dijete[1][sloj])):
            if random.uniform(0.0, 1.0) <= p_mut:
                slojPuni.append(dijete[1][sloj][nodes] + random.normalvariate(0, stddevGauss))
            else:
                slojPuni.append(dijete[1][sloj][nodes])
        newSelfWeights.append(slojPuni)
        
    rezultat = test_network(newWeights, newSelfWeights, inputsToTest, trueValues)
    dobrota = dobrota_funkcija(rezultat)
        
    return (newWeights, newSelfWeights, dobrota)   

def printBestSqaureError(newPopulation, inputsToTest, trueValues, iteration):
    najbolja = selectEliteJedinke(newPopulation, 1, inputsToTest, trueValues)[0]
    #print("najbolja", najbolja)
    print(f"[Train error @{iteration}]: {1 / najbolja[2]}")
 
 
def test_model(populacija, inputsToTest_test, trueValues_test, inputsToTest, trueValues):
    
    najbolja = selectEliteJedinke(populacija, 1, inputsToTest, trueValues)[0]
    rez = test_network(najbolja[0], najbolja[1], inputsToTest_test, trueValues_test)
    return mean_square_function(rez)


train_name, test_name, arhitektura, popsize, elitism, p_mut, stddevGauss, iter = None, None, None, None, None, None, None, None
if "--train" in sys.argv:
    idx = sys.argv.index("--train") + 1
    train_name = sys.argv[idx]
if "--test" in sys.argv:
    idx = sys.argv.index("--test") + 1
    test_name = sys.argv[idx]
if "--nn" in sys.argv:
    idx = sys.argv.index("--nn") + 1
    arhitektura = sys.argv[idx]
if "--popsize" in sys.argv:
    idx = sys.argv.index("--popsize") + 1
    popsize = int(sys.argv[idx])
if "--elitism" in sys.argv:
    idx = sys.argv.index("--elitism") + 1
    elitism = int(sys.argv[idx])
if "--p" in sys.argv:
    idx = sys.argv.index("--p") + 1
    p_mut = float(sys.argv[idx])
if "--K" in sys.argv:
    idx = sys.argv.index("--K") + 1
    stddevGauss = float(sys.argv[idx])
if "--iter" in sys.argv:
    idx = sys.argv.index("--iter") + 1
    iter = int(sys.argv[idx])

#print(train_name, test_name)    
    
file_train = open(f".\\{train_name}", "r", encoding="utf-8")
file_test = open(f".\\{test_name}", "r", encoding="utf-8")

inputReadLines = file_train.readlines()
inputTest = file_test.readlines()

# ucitaj podatke
imena = None
dataset = []
inputsToTest = []
trueValues = []
inputsToTest_test = []
trueValues_test = []
for idx, line in enumerate(inputReadLines):
    if idx == 0:
        imena = line.strip().split(",")
    else:
        dataset.append([float(value) for value in line.strip().split(",")])
        inputsToTest.append(dataset[idx - 1][:-1])
        trueValues.append(dataset[idx - 1][-1])
#print(inputsToTest)
dataset = []
for idx, line in enumerate(inputTest):
    if idx == 0:
        imena = line.strip().split(",")
    else:
        dataset.append([float(value) for value in line.strip().split(",")])
        inputsToTest_test.append(dataset[idx - 1][:-1])
        trueValues_test.append(dataset[idx - 1][-1])
   
arhitektura = [int(razina) for razina in arhitektura[:-1].split("s")]
#print(imena)
#for k in dataset:
#    print(k)
   
networkWeights, selfWeights, dobrota = stvori_pocetnu_populaciju(arhitektura, imena)

#for k in test_network(networkWeights, selfWeights, inputsToTest, trueValues):
#    print(k)
#print("-------------------------------------")
#print("-------------------------------------")
#for k in test_network2(networkWeights, selfWeights, inputsToTest, trueValues):
#    print(k)

#print(dobrota)
#raceni_uzorci = test_network(networkWeights, selfWeights, inputsToTest, trueValues)
       
#for idx, ulaz in enumerate(vraceni_uzorci):
#    print(f"{idx}. {ulaz}")
    
#print(mean_square_function(vraceni_uzorci))

#networkWeights, selfWeights = stvori_pocetnu_populaciju(arhitektura, imena)

populacija = []
for pop in range(0, popsize):
    populacija.append(stvori_pocetnu_populaciju(arhitektura, imena))
    
    
#for p in populacija:
#    print(p, "\n\n")
#print(populacija[len(populacija) - 1][0])
#print("\n\n\n")
#print(populacija[len(populacija) - 1][1])

for idx in range(0, iter + 1):
    
    nova_populacija = []
    # elitizam, izaberi n-elitism najboljih jedinki po dobroti
    #nova_populacija.append(najbolja for najbolja in selectEliteJedinke(populacija, elitism, inputsToTest, trueValues)) 
    for najbolja in selectEliteJedinke(populacija, elitism, inputsToTest, trueValues):
        nova_populacija.append(najbolja)
    
    while(len(nova_populacija) < len(populacija)):
        
        rod1, rod2 = selectParents(populacija, inputsToTest, trueValues)
        dijete = krizanje_i_mutacija(rod1, rod2, p_mut, stddevGauss, inputsToTest, trueValues)
        #dijete = mutacija(rod1, p_mut, stddevGauss, inputsToTest, trueValues)
        nova_populacija.append(dijete)
        #print(f"Nova: {len(nova_populacija)} || Stara: {len(populacija)} || Iteracija: {idx}")
    #print(f"Iteracija: {idx}")
    populacija = nova_populacija
    
    if idx in (2000, 4000, 6000, 8000, 10000):
        printBestSqaureError(populacija, inputsToTest, trueValues, idx)
    

ss_err = test_model(populacija, inputsToTest_test, trueValues_test, inputsToTest, trueValues)
print(f"[Test error]: {ss_err}") 

        
