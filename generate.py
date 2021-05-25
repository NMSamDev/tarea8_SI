import csv
import string
import sys
import codecs
import random
import hashlib
import math

# Diccionarios para contar las palabras segun su clasificacion
countP = dict()     # Positivo
countN = dict()     # Negativo
count = dict()      # Todos

# 1 es positivo
# 0 es negativo

# Cuenta las palabras segun su clasificacion
def word_count(str, clase):
    words = []
    words = str.split()
    
    for word in words:
        # Todos
        if word in count:
            count[word] += 1
        else:
            count[word] = 1
        # Positivos
        if(clase == 1):
            if word in countP:
                countP[word] += 1
            else:
                countP[word] = 1
        # Negativos
        else:
            if word in countN:
                countN[word] += 1
            else:
                countN[word] = 1

# Lectura de los datos
with open('./sentiment_labelled/amazon_cells_labelled.txt', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = '\t')

    entrada = dict()  # Diccionario para asignar id con su respectiva palabra
    saveIn = [] # Guarda diccionario entrada en una lista
    
    w = []
    temp = ""
    posW = []
    negW = []
    pos = 0
    neg = 0

    randomizer = list(range(1,100))

    for line in csv_reader:
        random.shuffle(randomizer)
        w = ''.join([i for i in line[0] if i not in string.punctuation]).lower()
        # entrada["id"] = hashlib.md5((w + str(randomizer[0])).encode()).hexdigest() # alternativa para añadir mayor aleartorierdad
        entrada["id"] = hashlib.md5(w.encode()).hexdigest()
        entrada["word"] = w
        entrada["clase"] = int(line[1])
        saveIn.append(dict(entrada))

    # Ordenamos por el id descendente para que nuestra eleccion tenga aleartoriedad
    saveIn = sorted(saveIn, key=lambda k: k['id']) 
    
    test = [] # Test
    training = [] # Training
    for i in range(0, 1000):
        if(i < 100):
            test.append(saveIn[i])
        else:
            training.append(saveIn[i])
    
    # Imprime la lista Training
    # for x in training:
    #     print(x['id'], x['clase'])
    
    # Guarda y cuenta las palabras segun su clase
    for line in training:
        w = line['word']
        word_count(w, line["clase"])
        if(line["clase"] == 1):
            posW.append(w)
            pos+=1
        else:
            negW.append(w)
            neg+=1
    
    # Parte de la formula
    v = len(count.keys()) # Vocabulario
    p0 = math.log(neg/len(training))  # log P(POS)
    p1 = math.log(pos/len(training))  # log P(NEG)
    newData = []

    # Completado llaves faltantes
    for word in count.keys():
        if not (word in countN):
            countN[word] = 0
        if not (word in countP):
            countP[word] = 0
        newData.append({
            "Palabra": word,
            "FrecPos": countP[word],
            "FrecNeg": countN[word],
            "LogPos": math.log((countP[word] + 1)/ (pos + v)),
            "LogNeg": math.log((countN[word] + 1)/ (neg + v)),
            "LogP(POS)": p0,
            "LogP(NEG)": p1
        })

    with open('modelo.csv', 'w') as new_file:
        headers = ['Palabra', 'FrecPos', 'FrecNeg', 'LogPos', 'LogNeg', 'LogP(POS)', 'LogP(NEG)']
        csv_writer = csv.DictWriter(new_file, fieldnames=headers)
        csv_writer.writeheader()

        for line in newData:
            csv_writer.writerow(line)
    
    with open('test_cases.csv', 'w') as test_cases:
        headers = ['id', 'word', 'clase']
        csv_writer = csv.DictWriter(test_cases, fieldnames=headers)
        csv_writer.writeheader()

        for line in test:
            csv_writer.writerow(line)
    
    with open('all_cases.csv', 'w') as all_cases:
        headers = ['id', 'word', 'clase']
        csv_writer = csv.DictWriter(all_cases, fieldnames=headers)
        csv_writer.writeheader()
        for line in test + training:
            csv_writer.writerow(line)
