import json

arr = []

with open("cenz.txt", 'r', encoding='utf-8') as txt:
    for line in txt:
        word = line.lower().strip().split('\n')[0]
        if word != '':
            arr.append(word)
with open("cenz.json", 'w', encoding='utf-8') as js:
    json.dump(arr, js)
