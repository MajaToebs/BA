import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



# SCATTER PLOT
def plot_scatterplot():
    for thesis in all_theses:
        plt.close('all')
        this_doc = df.loc[df['document'] == thesis]

        # scatter the GFIs depending on the chunk size
        plt.scatter(this_doc['length_of_chunk'], this_doc['fog'], label = 'my Fog', color = 'red')
        plt.scatter(this_doc['length_of_chunk'], this_doc['GFI'], label = 'GFI', color = 'orange')
        #plt.scatter(this_doc['length_of_chunk'], this_doc['ARI'], label = 'ARI', color = 'green')
        #plt.scatter(this_doc['length_of_chunk'], this_doc['SMOG'], label = 'SMOG', color = 'green')
        #plt.scatter(this_doc['length_of_chunk'], this_doc['CLI'], label = 'CLI', color = 'green')
        #plt.scatter(this_doc['length_of_chunk'], this_doc['FKGL'], label = 'FKGL', color = 'green')
        plt.gcf().set_size_inches(14, 7)

        # calculate the mean GFIs for each chunk size
        mean_GFIs = { 'len' : [],
                      'mean' : []}
        for l in sorted(set(this_doc['length_of_chunk'])):
            values = this_doc.loc[this_doc['length_of_chunk'] == l]['GFI']
            mean_GFIs['len'].append(l)
            mean_GFIs['mean'].append(np.mean(values))

        mean_other = {'len': [],
                     'mean': []}
        for l in sorted(set(this_doc['length_of_chunk'])):
            values = this_doc.loc[this_doc['length_of_chunk'] == l]['fog']
            mean_other['len'].append(l)
            mean_other['mean'].append(np.mean(values))

        # insert the means into the plot
        plt.plot(mean_GFIs['len'], mean_GFIs['mean'], 'k-', label = 'mean GFIs of this chunk size', color='orange')
        # insert the means into the plot
        plt.plot(mean_other['len'], mean_other['mean'], 'k-', label = 'mean Fogs of this chunk size', color='red')
        plt.ylabel('grade level')
        plt.xlabel('length of chunk in sentences')
        plt.legend()
        plt.suptitle('Comparison of two readability indices for document ' + thesis, fontsize=14)
        plt.savefig('Plots/indices/thesis/scatter/' + thesis + 'indicesOverChunkSize.svg')




df = pd.read_csv("Results/English/resultsIndicesTheses.csv", header=0, index_col=0)
# to get only the values with complexity 3
df = df.loc[df["complexity"]==3]

all_theses = ['en114417450.txt', 'en119716549.txt', 'en119767323.txt', 'en116249615.txt',
              'en115002482.txt', 'en117652377.txt', 'en117661421.txt']

plot_scatterplot()

plt.close('all')