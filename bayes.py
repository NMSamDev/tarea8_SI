import csv
import string

dataTest = []
dataClass = []
final = []

# Lectura de los datos
with open('./test_cases.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    next(csv_reader)

    for line in csv_reader:
        # next(csv_reader)
        dataTest.append({
            "id": line[0],
            "frase": line[1],
            "clase": line[2]
            })
LogPOS = 0
LogNEG = 0
with open('./modelo.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    next(csv_reader)

    for line in csv_reader:
        dataClass.append({
            "Palabra": line[0],
            "FrecPos": float(line[1]),
            "FrecNeg": float(line[2]),
            "LogPos": float(line[3]),
            "LogNeg": float(line[4]),
            "LogP(POS)": float(line[5]),
            "LogP(NEG)": float(line[6])
        })
LogPOS = dataClass[0].get("LogP(POS)")
LogNEG = dataClass[0].get("LogP(NEG)")

clasificacion = []
for line in dataTest:
    tempPos = 0.0
    tempNeg = 0.0
    frase = line["frase"].split()
    tempPos += LogPOS
    tempNeg += LogNEG
    for word in frase:
        for dc in dataClass:
            if(dc.get("Palabra") == word):
                tempPos += dc.get("LogPos")
                tempNeg += dc.get("LogNeg")
    if(tempPos > tempNeg):
        clasificacion.append({
            "id": line["id"],
            "LogPos": tempPos,
            "LogNeg": tempNeg,
            "Clase": 1,
            "Clase Real": line["clase"]
        })
    else:
        clasificacion.append({
            "id": line["id"],
            "LogPos": tempPos,
            "LogNeg": tempNeg,
            "Clase": 0,
            "Clase Real": line["clase"]
        })

with open('clasificacion.csv', 'w') as clasificacion_file:
    headers = ['id', 'LogPos', 'LogNeg', 'Clase', 'Clase Real']
    csv_writer = csv.DictWriter(clasificacion_file, fieldnames=headers)
    csv_writer.writeheader()
    for line in clasificacion:
        csv_writer.writerow(line)