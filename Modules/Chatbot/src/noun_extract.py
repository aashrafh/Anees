import xml.etree.ElementTree as ET
import preprocess
f = open('../Data/jamid.txt','r',encoding="utf-8")
data = f.read()
f.close()
data = ET.fromstring(data)
lst1 = data.findall('noun/unvocalized')
nouns = list()
for noun in lst1:
    nouns.append(preprocess.pre_process(noun.text))

f = open('../Data/fa3il.txt','r',encoding="utf-8")
data = f.read()
f.close()
data = ET.fromstring(data)
lst1 = data.findall('noun/unvocalized')
for noun in lst1:
    nouns.append(preprocess.pre_process(noun.text))

f = open('../Data/maf3oul.txt','r',encoding="utf-8")
data = f.read()
f.close()
data = ET.fromstring(data)
lst1 = data.findall('noun/unvocalized')
for noun in lst1:
    nouns.append(preprocess.pre_process(noun.text))

f = open('../Data/mansoub.txt','r',encoding="utf-8")
data = f.read()
f.close()
data = ET.fromstring(data)
lst1 = data.findall('noun/unvocalized')
for noun in lst1:
    nouns.append(preprocess.pre_process(noun.text))

f = open('../Data/masdar.txt','r',encoding="utf-8")
data = f.read()
f.close()
data = ET.fromstring(data)
lst1 = data.findall('noun/unvocalized')
for noun in lst1:
    nouns.append(preprocess.pre_process(noun.text))

f = open('../Data/moubalagha.txt','r',encoding="utf-8")
data = f.read()
f.close()
data = ET.fromstring(data)
lst1 = data.findall('noun/unvocalized')
for noun in lst1:
    nouns.append(preprocess.pre_process(noun.text))

f = open('../Data/mouchabbaha.txt','r',encoding="utf-8")
data = f.read()
f.close()
data = ET.fromstring(data)
lst1 = data.findall('noun/unvocalized')
for noun in lst1:
    nouns.append(preprocess.pre_process(noun.text))

f = open('../Data/sifates.txt','r',encoding="utf-8")
data = f.read()
f.close()
data = ET.fromstring(data)
lst1 = data.findall('noun/unvocalized')
for noun in lst1:
    nouns.append(preprocess.pre_process(noun.text))

f = open('../Data/tafdil.txt','r',encoding="utf-8")
data = f.read()
f.close()
data = ET.fromstring(data)
lst1 = data.findall('noun/unvocalized')
for noun in lst1:
    nouns.append(preprocess.pre_process(noun.text))

file = open(r"../Data/noun_dictionary.txt","w+",encoding="utf-8")
file.write(" ".join(list(set(nouns))))
file.close()