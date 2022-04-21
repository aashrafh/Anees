import xml.etree.ElementTree as ET
import preprocess
f = open('../Data/verbs.txt','r',encoding="utf-8")
data = f.read()
f.close()
data = ET.fromstring(data)
lst1 = data.findall('verb/unvocalized')
lst2 = data.findall('verb/root')
verbs = list()
for verb in lst1:
    verbs.append(preprocess.pre_process(verb.text))
for verb in lst2:
    verbs.append(preprocess.pre_process(verb.text))
file = open(r"../Data/verb_dictionary.txt","w+",encoding="utf-8")
file.write(" ".join(list(set(verbs))))
file.close()

