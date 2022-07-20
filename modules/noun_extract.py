import xml.etree.ElementTree as ET
import preprocess

files = ['./data/jamid.txt', './data/fa3il.txt', './data/maf3oul.txt', './data/mansoub.txt', './data/masdar.txt',
         './data/moubalagha.txt', './data/mouchabbaha.txt', './data/sifates.txt', './data/tafdil.txt']

nouns = []
for file in files:
    with open(file, 'r', encoding="utf-8") as f:
        data = f.read()
        data = ET.fromstring(data)
        res = data.findall('noun/unvocalized')
        nouns.extend([preprocess.pre_process(noun.text) for noun in res])

file = open(r"./data/noun_dictionary.txt", "w+", encoding="utf-8")
file.write(" ".join(list(set(nouns))))
file.close()
