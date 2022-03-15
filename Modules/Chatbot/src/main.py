import nlu


file = open('../Data/test1.txt','r', encoding="utf8")
text = file.read()

nlu.understanding(text)


