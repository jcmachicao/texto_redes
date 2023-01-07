import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st
import codecs
import spacy
import subprocess
import es_core_news_sm
nlp = es_core_news_sm.load()

len_pal, my_k, ancho, n_iter, margen = 5, 0.1, 10, 500, 0.04

#archivo = st.file_uploader('Cargar archivo de texto .txt')
archivo = st.text_input('Inserte texto aqui:', '')

if archivo is not None:
  
  st.write(archivo)
  
  oraciones = archivo.split('.')
  st.write('El número de oraciones de este texto es: ', len(oraciones)-1)
  
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
    
  pares_df = pd.DataFrame(pares, columns=['col_a', 'col_b'])
  st.dataframe(depur_tot)
  
  G = nx.from_pandas_edgelist(pares_df, 'col_a', 'col_b')
  pos = nx.spring_layout(G, k=my_k, iterations=n_iter)
  
  fig, ax = plt.subplots()
  nx.draw_networkx_nodes(G, pos, node_color='yellow')
  
  st.pyplot(fig)
  
  labels = {}
  for node in G.nodes():
    labels[node] = node
    
  d1 = nx.betweenness_centrality(G)
  d2 = nx.degree_centrality(G)
  nx.set_node_attributes(G, d1, 'size') 
  
  sizes_btw = []
  for g in G.nodes.values():
    sizes_btw.append(int(g['size']*3000))
  
  '''
  pares_df = pd.DataFrame([['Nodo 1', 'Nodo 2'], ['Nodo 2', 'Nodo 3'], ['Nodo 3', 'Nodo 1']], columns = ['col_a', 'col_b'])
  G = nx.from_pandas_edgelist(pares_df, 'col_a', 'col_b')
  pos = nx.spring_layout(G, k=my_k, iterations=n_iter)
  '''

  fig, ax = plt.subplots()
  #nx.draw_networkx_nodes(G, pos, node_size=sizes_btw, node_color='yellow')
  nx.draw_networkx_nodes(G, pos, node_color='yellow')
  nx.draw_networkx_edges(G, pos, edge_color='gray', width=5.0, alpha=0.3)
  #nx.draw_networkx_labels(G, pos, labels, font_size=12)  
  st.pyplot(fig)
