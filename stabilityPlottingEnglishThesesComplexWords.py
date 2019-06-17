import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



# SCATTER PLOT
def plot_scatterplot():
    for thesis in all_theses:
        plt.close('all')
        this_doc_3 = df.loc[df['document'] == thesis].loc[df["complexity"]==3]
        this_doc_4 = df.loc[df['document'] == thesis].loc[df["complexity"]==4]
        this_doc_5 = df.loc[df['document'] == thesis].loc[df["complexity"]==5]

        # scatter the GFIs depending on the chunk size
        plt.scatter(this_doc_3['length_of_chunk'], this_doc_3['GFI'], color = 'orange', label = 'words with >3 syllables are complex')
        plt.scatter(this_doc_4['length_of_chunk'], this_doc_4['GFI'], color = 'red', label = 'words with >4 syllables are complex')
        plt.scatter(this_doc_5['length_of_chunk'], this_doc_5['GFI'], color = 'green', label = 'words with >5 syllables are complex')
        plt.gcf().set_size_inches(14, 7)
        plt.legend()

        # calculate the mean GFIs for each chunk size
        mean_GFIs_3 = { 'len' : [],
                      'mean' : []}
        for l in sorted(set(this_doc_3['length_of_chunk'])):
            values = this_doc_3.loc[this_doc_3['length_of_chunk'] == l]['GFI']
            mean_GFIs_3['len'].append(l)
            mean_GFIs_3['mean'].append(np.mean(values))

        mean_GFIs_4 = { 'len' : [],
                      'mean' : []}
        for l in sorted(set(this_doc_4['length_of_chunk'])):
            values = this_doc_4.loc[this_doc_4['length_of_chunk'] == l]['GFI']
            mean_GFIs_4['len'].append(l)
            mean_GFIs_4['mean'].append(np.mean(values))

        mean_GFIs_5 = { 'len' : [],
                      'mean' : []}
        for l in sorted(set(this_doc_5['length_of_chunk'])):
            values = this_doc_5.loc[this_doc_5['length_of_chunk'] == l]['GFI']
            mean_GFIs_5['len'].append(l)
            mean_GFIs_5['mean'].append(np.mean(values))



        # insert the means into the plot
        plt.plot(mean_GFIs_3['len'], mean_GFIs_3['mean'], 'k-', color='orange')
        plt.plot(mean_GFIs_4['len'], mean_GFIs_4['mean'], 'k-', color='red')
        plt.plot(mean_GFIs_5['len'], mean_GFIs_5['mean'], 'k-', color='green')
        plt.ylabel('GFI')
        plt.xlabel('length of chunk in sentences')
        plt.suptitle('Comparison of GFI values of the different chunk sizes of document ' + thesis, fontsize=14)
        plt.savefig('Plots/English/complex/' + thesis + 'indicesOverChunkSizeShortenedSentences.svg')




# DEVIATIONS
# display standard deviations of chunks
def plot_deviations():
    plt.close('all')
    df_deviations_3 = df_variances.loc[df_variances['complexity']==3]
    df_deviations_4 = df_variances.loc[df_variances['complexity']==4]
    df_deviations_5 = df_variances.loc[df_variances['complexity']==5]

    # get the chunk sizes and their mean deviations
    chunk_sizes = list(sorted(set(df_deviations_3['length_of_chunk'])))
    for i,c in enumerate(chunk_sizes):
        chunk_sizes[i] = int(c)
    mean_chunk_deviations_3 = []
    median_chunk_deviations_3 = []
    # calculate the mean variance for each chunk size
    for size in chunk_sizes:
        mean_chunk_deviations_3.append(np.mean(df_deviations_3.loc[df_deviations_3['length_of_chunk'] == size]['std']))
        median_chunk_deviations_3.append(np.median(df_deviations_3.loc[df_deviations_3['length_of_chunk'] == size]['std']))

    # get the chunk sizes and their mean deviations
    chunk_sizes = list(sorted(set(df_deviations_4['length_of_chunk'])))
    for i,c in enumerate(chunk_sizes):
        chunk_sizes[i] = int(c)
    mean_chunk_deviations_4 = []
    median_chunk_deviations_4 = []
    # calculate the mean variance for each chunk size
    for size in chunk_sizes:
        mean_chunk_deviations_4.append(np.mean(df_deviations_4.loc[df_deviations_4['length_of_chunk'] == size]['std']))
        median_chunk_deviations_4.append(np.median(df_deviations_4.loc[df_deviations_4['length_of_chunk'] == size]['std']))



    # get the chunk sizes and their mean deviations
    chunk_sizes = list(sorted(set(df_deviations_5['length_of_chunk'])))
    for i,c in enumerate(chunk_sizes):
        chunk_sizes[i] = int(c)
    mean_chunk_deviations_5 = []
    median_chunk_deviations_5 = []
    # calculate the mean variance for each chunk size
    for size in chunk_sizes:
        mean_chunk_deviations_5.append(np.mean(df_deviations_5.loc[df_deviations_5['length_of_chunk'] == size]['std']))
        median_chunk_deviations_5.append(np.median(df_deviations_5.loc[df_deviations_5['length_of_chunk'] == size]['std']))



    # scatter the medians nicely

    x_s_1 = np.concatenate((chunk_sizes, chunk_sizes, chunk_sizes))
    y_s_1 = np.concatenate((median_chunk_deviations_3, median_chunk_deviations_4, median_chunk_deviations_5))
    colors = []
    for i in range(len(chunk_sizes)):
        colors.append("orange")
    for i in range(len(chunk_sizes)):
        colors.append("red")
    for i in range(len(chunk_sizes)):
        colors.append("green")
    plt.scatter(x_s_1, y_s_1, color = colors)

    #plt.legend()
    plt.gcf().set_size_inches(14, 7)
    plt.ylabel('standard deviation of the GFI over all documents')
    plt.xlabel('length of chunk in sentences')
    plt.suptitle('Comparison of how the definition of complex words influences\n'
                 'the standard deviations of GFI values of the different chunk sizes over all documents', fontsize=14)
    plt.savefig('Plots/English/complex/deviationsOnChunkSizeShortenedSentences.svg')



df = pd.read_csv("Results/English/resultsTheses.csv", header=0, index_col=0)
#df = df.loc[df["complexity"]==3]

df_variances = pd.read_csv("Results/English/variancesTheses.csv", header=0, index_col=0)
#df_variances = df_variances.loc[df_variances["complexity"]==3]


all_theses = ['en114417450.txt', 'en119716549.txt', 'en119767323.txt', 'en116249615.txt',
              'en115002482.txt', 'en117652377.txt', 'en117661421.txt']


#plot_scatterplot()
plot_deviations()

plt.close('all')

