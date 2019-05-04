import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("dataTheses.csv", header= 0,index_col= 0)
#print(df)

# plot type 1
my_doc = df.loc[df['document'] == 'en117661421.txt']
my_doc_chunk_m = df.loc[df['length_of_chunk'] == 200]
#print(my_doc_chunk_m)
#print(my_doc_chunk_m[:,1:]) geht nicht

boxplot = my_doc_chunk_m.boxplot(column='x')
#print(type(boxplot))
#my_doc_chunk_m.plot()
plt.show()