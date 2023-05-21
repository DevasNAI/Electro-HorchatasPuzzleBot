import csv
data = []
with open("lado.csv") as file:
    csv_reader = csv.reader(file, delimiter=' ')
    lineCount = 0

    for row in csv_reader:
        data.append(float(row[0]))
        lineCount += 1

print(data)
print(lineCount)