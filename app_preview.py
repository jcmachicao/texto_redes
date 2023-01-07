import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st
import codecs
import spacy
import subprocess

subprocess.run(['pip', 'install', 'es_core_news_md'])

#archivo = st.file_uploader('Cargar archivo de texto .txt')
archivo = st.text_input('Inserte texto aqui:', 'texto')

if archivo is not None:
  
  st.write(archivo)
  
  oraciones = archivo.split('.')
  st.write('El número de oraciones de este texto es: ', len(oraciones))
  
  depur_tot = pd.DataFrame()
  pares = []
  for ora in oraciones:
    st.write(ora)
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
  
  st.dataframe(depur_tot)
  
  len_pal, my_k, ancho, n_iter, margen = 5, 0.1, 15, 500, 0.04

  pares_df = pd.DataFrame([['Nodo 1', 'Nodo 2'], ['Nodo 2', 'Nodo 3'], ['Nodo 3', 'Nodo 1']], columns = ['col_a', 'col_b'])
  G = nx.from_pandas_edgelist(pares_df, 'col_a', 'col_b')
  pos = nx.spring_layout(G, k=my_k, iterations=n_iter)

  fig, ax = plt.subplots()
  nx.draw_networkx_nodes(G, pos, node_color='yellow', ax=ax)
  nx.draw_networkx_edges(G, pos, edge_color='gray', width=5.0, alpha=0.3, ax=ax)

  st.pyplot(fig)
