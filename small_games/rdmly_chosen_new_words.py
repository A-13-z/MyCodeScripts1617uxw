import requests
import bs4
#from docx import Document
#from docx.shared import Inches
import random

pg = requests.get('https://www.vocabulary.com/lists/52473')

cd = bs4.BeautifulSoup(pg.text, features='html.parser')

ele = cd.select('ol#wordlist.wordlist.notesView li.entry.learnable a.word.dynamictext')
ele2 = cd.select('ol#wordlist.wordlist.notesView li.entry.learnable div.definition')

f1 = [i.getText() for i in ele]
f2 = [j.getText() for j in ele2]

dc = {a: b for a, b in zip(f1, f2)}

lt = [i for i in dc.items()]

print(random.choices(lt, k = 5))


#just a small tip
#if interested, you can save this as a word document using python docx module as shown above
