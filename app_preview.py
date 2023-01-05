import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st

archivo = st.file_uploader('Cargar archivo de texto .txt')

if archivo is not None:
  texto = ''
  with open(archivo, encoding='iso-8859-1') as f:
    lines = f.readlines()
    for li in lines:
      texto += li

  st.text(lines)

  len_pal, my_k, ancho, n_iter, margen = 5, 0.1, 15, 500, 0.04

  pares_df = pd.DataFrame([['Nodo 1', 'Nodo 2'], ['Nodo 2', 'Nodo 3'], ['Nodo 3', 'Nodo 1']], columns = ['col_a', 'col_b'])
  G = nx.from_pandas_edgelist(pares_df, 'col_a', 'col_b')
  pos = nx.spring_layout(G, k=my_k, iterations=n_iter)

  fig, ax = plt.subplots()
  nx.draw_networkx_nodes(G, pos, node_color='yellow', ax=ax)
  nx.draw_networkx_edges(G, pos, edge_color='gray', width=5.0, alpha=0.3, ax=ax)

  st.pyplot(fig)
