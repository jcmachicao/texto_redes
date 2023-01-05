import pandas as pd
import spacy
import es_core_news_sm
nlp = es_core_news_sm.load()
from spacy.lang.es.stop_words import STOP_WORDS
import networkx as nx
import matplotlib.pyplot as plt

texto = ''
#with open(ruta + archivo, encoding='iso-8859-1') as f:
with open(ruta + archivo) as f:
  lines = f.readlines()
  for li in lines:
    texto += li

len_pal, my_k, ancho, n_iter, margen = 5, 0.1, 15, 500, 0.04

depur_tot = pd.DataFrame()
pares = []
for ora in oraciones:
  depur = []
  doc = nlp(ora.lower())
  for t in doc:
    if len(t.text) > len_pal:
      if t.pos_ in ['NOUN', 'VERB']:
        depur.append([t.lemma_, t.pos_])
  depur_df = pd.DataFrame(depur, columns=['pal', 'gram'])
  pals = list(depur_df.pal)
  for j in range(len(pals)-1):
    pares.append([pals[j], pals[j+1]])
  depur_tot = pd.concat([depur_tot, depur_df], axis=0)
  
pares_df = pd.DataFrame(pares, columns=['col_a', 'col_b'])
  
G = nx.from_pandas_edgelist(pares_df, 'col_a', 'col_b')
pos = nx.spring_layout(G, k=my_k, iterations=n_iter)

labels = {}
for node in G.nodes():
  labels[node] = node

d1 = nx.betweenness_centrality(G)
d2 = nx.degree_centrality(G)

nx.set_node_attributes(G, d1, 'size')

sizes_btw = []
for g in G.nodes.values():
  sizes_btw.append(int(g['size']*3000))

plt.figure(figsize=(ancho*2, ancho*2), facecolor='lightgray')
nx.draw_networkx_nodes(G, pos, node_size=sizes_btw, node_color='yellow')
nx.draw_networkx_edges(G, pos, edge_color='gray', width=5.0, alpha=0.3)
nx.draw_networkx_labels(G, pos, labels, font_size=12)
plt.show()






