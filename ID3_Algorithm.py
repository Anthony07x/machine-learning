import sys
import math

class Node:
    
    def __init__(self, label: str, value: str, djeca: dict):
        self.label = label
        self.value = value
        self.djeca = djeca
        
    def __str__(self):
        return(f"Node: {self.label} ||| Value: {self.value}")
    
def possible_values_of_x(dataset: list, x: str):
    stupac = -1
    for idx, label in enumerate(dataset[0]):
        if label == x:
            stupac = idx
            break
        
    values = set()
    for idx, line in enumerate(dataset):
        if idx != 0:
            values.add(line[stupac])
        
    return [x, values]  # IME STUPCA(feature) i moguce vrijednosti za njega
        

def filterFunction(dataset: list, stupac: str, value: str) -> list:
    
    pozicija = -1
    for idx, label in enumerate(dataset[0]):
        if label == stupac:
            pozicija = idx
            break
    
    filteredDataset = []
    for idx, line in enumerate(dataset):
        if line[pozicija] == value or idx == 0:
            filteredDataset.append(line)
            
    return filteredDataset

# gets total occurence of values left in filtered (or starting) dataset
def getOccurenceOfValues(dataset: list) -> dict:
    values = dict()
    for idx, line in enumerate(dataset):
        if idx != 0:
            vrijednost = line[len(line) - 1]
            if vrijednost in values.keys():
                values[vrijednost] += 1
            else:
                values[vrijednost] = 1
    return values

# used for IG to calculate entropy of each possible Node expansion, 
# needs to be filtered before with "filterFunction" if further in expansion
def getOccurenceOfValues_by_X(dataset: list, x: str) -> float:
    
    trazeni_x = -1
    for idx, feature in enumerate(dataset[0]):
        if feature == x:
            trazeni_x = idx
            break
       
    value_of_feature = dict()
    
    for idx, line in enumerate(dataset):
        
        if idx != 0:
            if line[trazeni_x] in value_of_feature.keys():
               if line[len(line) - 1] in value_of_feature[line[trazeni_x]].keys():
                   value_of_feature[line[trazeni_x]][line[len(line) - 1]] += 1
               else:
                   value_of_feature[line[trazeni_x]][line[len(line) - 1]] = 1
                
            else:
                value_of_feature[line[trazeni_x]] = {line[len(line) - 1] : 1}
                
    return value_of_feature

        
# calculate weighted entropy for each feature thats left (must be filtered with getOccurenceOfValues_by_X before)  
def calculateWeightedEntropy(freq: dict) -> float:
    suma = 0.0
    ukupno_za_sve = 0
    
    for key, yes_no_occurs in freq.items():
        ukupno_za_sve += sum(yes_no_occurs.values())
    
    for key, yes_no_occurs in freq.items():
        ukupno_za_taj = sum(yes_no_occurs.values())
        for yes_no, num_of_occurs in yes_no_occurs.items():
            suma -= (ukupno_za_taj / ukupno_za_sve) * ((num_of_occurs/ukupno_za_taj) * math.log2(num_of_occurs/ukupno_za_taj))
    
    return round(suma, 6)       
 
 
# dataset must be filtered with "filterFunction" before calling this function       
def mostCommonValueForD(dataset: list) -> str:
    
    freq = getOccurenceOfValues(dataset)
    #print(freq)
    key_for_mostCommon_value = max(freq, key=freq.get)
    
    #provjeri jel postoji jos takvih max kljuceva(sa istim vrijednostima), ali da su abecedno prije
    for k,v in freq.items():
        if freq[k] == freq[key_for_mostCommon_value] and k < key_for_mostCommon_value:
            key_for_mostCommon_value = k

    return key_for_mostCommon_value

# dataset must be filtered with "filterFunction" before calling this function       
def entropyFunction(dataset: list) -> float: #, label: str
    
    freq = getOccurenceOfValues(dataset)
    
    entropija = 0.0
    ukupno = sum(freq.values())
    
    for k, v in freq.items():
        entropija -= (v/ukupno) * math.log2(v/ukupno)
    
    return round(entropija, 6)


def calculate_IG_function(X: list, parentEntropy: float, filteredDataset: list):
    
    #maxIG = max(X, 
    #    key=lambda x: parentEntropy - calculateWeightedEntropy(getOccurenceOfValues_by_X(filteredDataset, x)))
    
    maxIG = (0.0, "")
    for x in X:
        maxIG2 = (parentEntropy - calculateWeightedEntropy(getOccurenceOfValues_by_X(filteredDataset, x)), x)
        print(f"IG({maxIG2[1]})={maxIG2[0]:.4f}", end=" ")
        if maxIG2[0] > maxIG[0]:
            maxIG = (maxIG2[0], maxIG2[1])
        elif maxIG2[0] == maxIG[0]:
            maxIG = (maxIG[0], min(maxIG[1], maxIG2[1]))
    print()
    
    return maxIG[1]


def id3_algo_function(filteredDataset, parentDataset, X, myValue, treeDepth, maxDepth):
    if treeDepth == maxDepth:
        if len(filteredDataset) > 1:
            return Node(mostCommonValueForD(filteredDataset), myValue, None)
        else:
            return Node(mostCommonValueForD(parentDataset), myValue, None)
    
    if len(filteredDataset) <= 1:
        #print(filteredDataset, "filtt" )
        v = mostCommonValueForD(parentDataset) 
        return Node(v, myValue, None)
    
    v = mostCommonValueForD(filteredDataset)
    
    if len(X) == 0 or entropyFunction(filteredDataset) == 0.0:
        return Node(v, myValue, None)
    
    x = calculate_IG_function(X, entropyFunction(parentDataset), filteredDataset)
    sub_trees = dict()
    
    stupac, values = possible_values_of_x(parentDataset, x)
    
    for value in values:
        node = id3_algo_function(filterFunction(filteredDataset, stupac, value), filteredDataset, [removeX for removeX in X if removeX != x], value, treeDepth + 1, maxDepth)
        sub_trees[value] = node  # t je Node, a value je vrijednost of feature za koju je dosao tu
    return Node(x, myValue, sub_trees)

def constructTree(node: Node, depth: int = 1, path=None):
    if path is None:
        path = []
        
    # ak je korijen ujedno i list (jedini cvor)
    if node.value is None and node.djeca is None:   
        print(node.label)
        return

    # korijen ---> nema valuea do njega
    if node.value is None and node.djeca is not None:
        path.append(f"{depth}:{node.label}")
        
    # unutra, obicni node
    elif node.djeca is not None:
        path.append(f"={node.value} {depth}:{node.label}")
        
    # list 
    else:
        path.append(f"={node.value} {node.label}")

    # ako nema djece ---> dosa je do kraja, onda isprintaj taj put
    if not node.djeca:
        print("".join(path))
        return

    # ----> nastavi dalje za svu njegovu djecu ----> djeca su mape sa nodovima, a kljuc je value
    # provjeri kasnije jos jel ovo radi dobro na dummy primjeru
    for val, dijete in node.djeca.items():
        constructTree(dijete, depth + 1, path[:])

def predict(MasterNode: Node, predictDataset: list) -> list:
    predicitions = []
    for idx, line in enumerate(predictDataset):
        if idx != 0:
            #print("dasdsa", predictDataset[0] , line)
            predicitions.append(predict_from_node(predictDataset[0] , line, MasterNode))
 
    return predicitions
 
def predict_from_node(names: list, line:list, MasterNode: Node) -> tuple:
    
    if MasterNode.djeca == None:
        return (MasterNode.label, line[len(line) - 1]) # prva je predvidena, a druga je stvarna (iz test primjera)

    stupac = -1
    for idx, name in enumerate(names):
        if name == MasterNode.label:
            stupac = idx
            break
    #print("sadasd", MasterNode.djeca[line[stupac]]) 
    
    if line[stupac] not in MasterNode.djeca.keys():
        return ("maybe", line[len(line) - 1])
        
    newMasterNode = MasterNode.djeca[line[stupac]]
    return predict_from_node(names, line, newMasterNode) 
  
  
def accuracy_function(predicitons: list) -> float:
  accuracy, total = 0.0, 0
  for prediciton in predicitons:
      total += 1
      if prediciton[0] == prediciton[1]:
          accuracy += 1
          
  return round(accuracy/total, 5)  
              
def confusion_matrix(predicitons: list, possibleValues: list) -> list:
    matrix = dict()
    for prediction in predicitons:
        #if prediction[0] != prediction[1]:
        if f"P:{prediction[0]} | S:{prediction[1]}" not in matrix.keys():
            matrix[f"P:{prediction[0]} | S:{prediction[1]}"] = 1
        else:
            matrix[f"P:{prediction[0]} | S:{prediction[1]}"] += 1
    
    for possibleValue1 in possibleValues:
        for possibleValue2 in possibleValues:
            if f"P:{possibleValue1} | S:{possibleValue2}" not in matrix.keys():
                matrix[f"P:{possibleValue1} | S:{possibleValue2}"] = 0
         
    
    return matrix       

def print_confusion_matrix(confusionMatrix: dict):
    matrix_order = []
    for k,v in confusionMatrix.items():
        matrix_order.append((k,v))
        
    matrix_order = sorted(matrix_order, key=lambda x: x[0]) 
    step = int(math.sqrt(len(matrix_order)))
    for i in range(0, step):
        for j in range(0, step):
            print(matrix_order[j * step + i][1], end=" ")
        print()          
              
              
              
    
train_name = sys.argv[1]
test_name = sys.argv[2]

tree_depth = 100000

if len(sys.argv) > 3:
    tree_depth = int(sys.argv[3])
    #print("treeee", tree_depth)

file_train = open(f".\\{train_name}", "r", encoding="utf-8")
file_test = open(f".\\{test_name}", "r", encoding="utf-8")

linije_train = file_train.readlines()
linije_test = file_test.readlines()

dataset = []
possible_ends = []
for line in linije_train:
    dataset.append(list(line.strip().split(",")))
    possible_ends.append(line.strip().split(",")[-1])
# izbaci zadnji stupac koji je vrijednosti
dataset[0].pop()
X = dataset[0]

possible_ends = set(possible_ends[1:])
#print("poss", list(possible_ends))

dataset_test = []
for line in linije_test:
    dataset_test.append(list(line.strip().split(",")))

#for l in dataset_test:
#    print(l)
    
#k = filterFunction(dataset, "temperature", "cold")
#for i in k:
#    print(i)
#    
#print(mostCommonValueForD(filterFunction(dataset, "temperature", "cold")))
#print(entropyFunction(filterFunction(dataset, "temperature", "cold")))
#ss = getOccurenceOfValues_by_X(dataset, "temperature")
#print(ss)
#print(calculateWeightedEntropy(ss))
#print(calculate_IG_function(X, entropyFunction(dataset), filterFunction(dataset, "temperature", "cold")))
#print("sdsd", possible_values_of_x(dataset, "temperature"))

masterNode = id3_algo_function(dataset, dataset , X, None, 0, tree_depth)
print("[BRANCHES]:")
constructTree(masterNode, depth = 1)

predictions = predict(masterNode, dataset_test)

toPrint = []
for pred in predictions:
    toPrint.append(pred[0])
predict_print = " ".join(toPrint)

accuracy = accuracy_function(predictions)
#print(f"[ACCURACY]: {accuracy:.5f}")

matrix = confusion_matrix(predictions , sorted(list(possible_ends)))
#print(matrix)
   
#print("[CONFUSION_MATRIX]:")          

toPrint = f"[PREDICTIONS]: {predict_print}\n[ACCURACY]: {accuracy:.5f}\n[CONFUSION_MATRIX]:"
print(toPrint)
print_confusion_matrix(matrix)
