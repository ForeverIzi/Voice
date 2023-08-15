from deepmultilingualpunctuation import PunctuationModel
model = PunctuationModel(model  = "kredor/punctuate-all")

import heapq
import re
import string
import nltk

nltk.download('punkt')
nltk.download("stopwords")

#Formatando o Texto

def formatar(txt):
    txt = re.sub(r'\s', ' ', txt)
    txt = txt.replace("\\n\\n", " ")
    txt = txt.lower()
    
    tokens = []
    vicios = ['né', 'Né', 'então', 'Então', 'gente']
    stopwords = nltk.corpus.stopwords.words("portuguese") + vicios
    
    for i in nltk.word_tokenize(txt):
        if i not in stopwords and i not in string.punctuation:
            tokens.append(i)
    texto_formatado = " ".join(elemento for elemento in tokens if not elemento.isdigit())
    return texto_formatado

#Quantidade de Sentenças

def quant_sent(text,num):
    num_sent = len(nltk.sent_tokenize(text))
    quant = (num_sent * num * 10 ) / 100
    return round (quant)

#Retorna a lista das sentenças

def sumarizar(txt, quant_sentencas):
  texto_format = formatar(txt)
  texto_pontuado = model.restore_punctuation(txt)
  freq_palavras = nltk.FreqDist(nltk.word_tokenize(texto_format))
  freq_max  = max(freq_palavras.values())
  for palavra in freq_palavras:
    freq_palavras[palavra] = freq_palavras[palavra]/freq_max

  sentencas_txt = nltk.sent_tokenize(txt)

  nota_sentenca = {}
  for sentenca in sentencas_txt:
    for palavra in nltk.word_tokenize(sentenca):
      if palavra in freq_palavras.keys():
        if sentenca not in nota_sentenca:
          nota_sentenca[sentenca] = freq_palavras[palavra]
        else:
          nota_sentenca[sentenca] += freq_palavras[palavra]

  melhores_sentencas = heapq.nlargest(quant_sentencas, nota_sentenca, key = nota_sentenca.get)
  resumo = ""
  for sentenca in sentencas_txt:
    if sentenca in melhores_sentencas:
      resumo += sentenca
  return resumo,sentencas_txt,melhores_sentencas



texto = input("Insira o texto para ser resumido: ")
num_sentencas = int(input("Insira a porcentagem de sentenças que deseja no resumo (em número inteiro): "))

resumo, sentencas, melhores_sentencas = sumarizar(texto, quant_sent(texto, num_sentencas))

print(f"\nTexto resumido com ({num_sentencas} das sentenças originais):\n{resumo}\n")

print("Todas as sentenças:")
for sentenca in sentencas:
    print(f"- {sentenca}")

print("\nMelhores sentenças:")
for sentenca in melhores_sentencas:
    print(f"- {sentenca}")
