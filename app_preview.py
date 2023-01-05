import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

pares_df = pd.DataFrame([['Nodo 1', 'Nodo 2'], ['Nodo 2', 'Nodo 3'], ['Nodo 3', 'Nodo 1']], columns = ['col_a', 'col_b'])
G = nx.from_pandas_edgelist(pares_df, 'col_a', 'col_b')
pos = nx.spring_layout(G, k=my_k, iterations=n_iter)

plt.figure()
nx.draw_networkx_nodes(G, pos, node_size=sizes_btw, node_color='yellow')
nx.draw_networkx_edges(G, pos, edge_color='gray', width=5.0, alpha=0.3)
nx.draw_networkx_labels(G, pos, labels, font_size=12)

st.pyplot()
