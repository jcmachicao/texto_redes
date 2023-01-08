import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st
import codecs
import spacy
import subprocess
import es_core_news_sm
nlp = es_core_news_sm.load()

len_pal, my_k, ancho, n_iter, margen = 5, 0.1, 12, 500, 0.04

st.title('Organizador de verbos y sujetos en un texto complejo')
#archivo = st.file_uploader('Cargar archivo de texto .txt')
archivo = st.text_area('Inserte texto aqui:', '')

if archivo is not None:
  
  #st.write(archivo)
  st.write('Si no tienes textos disponibles, puedes probar alguno de este documento:
           ['Ejemplos'](https://docs.google.com/document/d/1vsRH42QTyh6l34_Hh5_nDMj-xclZdOc98ih4vJ23nxU/edit?usp=sharing)')
  
  oraciones = archivo.split('.')
  st.write('El número de oraciones de este texto es: ', len(oraciones)-1)
  
  depur_tot = pd.DataFrame()
  pares = []
  for ora in oraciones:
    #st.write(ora)
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
  #st.dataframe(depur_tot.head())
  
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
  
  fig, ax = plt.subplots(figsize=(ancho, ancho))
  nx.draw_networkx_nodes(G, pos, node_size=sizes_btw, node_color='yellow')
  nx.draw_networkx_edges(G, pos, edge_color='gray', width=5.0, alpha=0.3)
  for node, label in nx.draw_networkx_labels(G, pos, labels, font_size=9).items():
    label.set_rotation(45)
  st.pyplot(fig)
