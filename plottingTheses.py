import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



# BOXPLOT
# show all the boxplots of all documents' GFIs for chunk size m next to each other
def plot_boxplots():
    for m in [1000, 750, 500, 450, 400, 350, 300, 250, 200, 150, 100, 75, 50, 40, 30, 20, 10]:
        my_doc_chunk_m = df.loc[df['length_of_chunk'] == m]
        my_doc_chunk_m.boxplot(column='GFI', by='document', figsize=(14,7))
        plt.ylabel('GFI')
        plt.figtext(0.995, 0.01, 'the chunk size is ' + str(m), ha='right', va='bottom')
        plt.savefig('Plots/thesis/boxplot/' + str(m) + 'longChunksBoxplottedAllTheses.svg')


# BAR CHART
def plot_barcharts():
    for m in [100, 75, 50, 40, 30, 20, 10]:
        for thesis in all_theses:
            plt.close('all')
            this_doc_len_m = df.loc[df['document']==thesis].loc[df['length_of_chunk']==m]
            if this_doc_len_m.empty == True:
                continue
            ints = []
            for i in this_doc_len_m['number_of_chunk']:
                ints.append(int(i))
            plt.bar(ints,this_doc_len_m['GFI'])
            plt.gcf().set_size_inches(7, 3.5)
            plt.ylabel('GFI')
            plt.xlabel('number of chunk (from beginning to end)')
            plt.figtext(0.995, 0.01, 'the chunk size is ' + str(m), ha='right', va='bottom')
            plt.savefig('Plots/thesis/bar/' + str(m) + "_long_" + thesis + 'indicesOverNumberOfChunk.svg')


# SCATTER PLOT
def plot_scatterplot():
    for thesis in all_theses:
        plt.close('all')
        this_doc = df.loc[df['document'] == thesis]

        # scatter the GFIs depending on the chunk size
        plt.scatter(this_doc['length_of_chunk'], this_doc['GFI'])
        plt.gcf().set_size_inches(14, 7)

        # calculate the mean GFIs for each chunk size
        mean_GFIs = { 'len' : [],
                      'mean' : []}
        for l in sorted(set(this_doc['length_of_chunk'])):
            values = this_doc.loc[this_doc['length_of_chunk'] == l]['GFI']
            mean_GFIs['len'].append(l)
            mean_GFIs['mean'].append(np.mean(values))

        # insert the means into the plot
        plt.plot(mean_GFIs['len'], mean_GFIs['mean'], 'k-', color='r')
        plt.ylabel('GFI')
        plt.xlabel('length of chunk in sentences')
        plt.savefig('Plots/thesis/scatter/' + thesis + 'indicesOverChunkSize.svg')

# VARIANCES
# display variances of chunks
# read in the variances from the file
def plot_variances():
    plt.close('all')

    # get the chunk sizes and their mean variances
    chunk_sizes = list(sorted(set(df_variances['length_of_chunk'])))
    for i,c in enumerate(chunk_sizes):
        chunk_sizes[i] = int(c)
    mean_chunk_variances = []
    median_chunk_variances = []
    # calculate the mean variance for each chunk size
    for size in chunk_sizes:
        mean_chunk_variances.append(np.mean(df_variances.loc[df_variances['length_of_chunk'] == size]['variance']))
        median_chunk_variances.append(np.median(df_variances.loc[df_variances['length_of_chunk'] == size]['variance']))


    # scatter them nicely
    plt.scatter(chunk_sizes, mean_chunk_variances, label = 'mean values')
    plt.scatter(chunk_sizes, median_chunk_variances, label = 'median values')
    plt.legend()
    plt.gcf().set_size_inches(14, 7)
    plt.ylabel('mean variance of the GFI over all documents')
    plt.xlabel('length of chunk in sentences')
    plt.savefig('Plots/thesis/variancesOnChunkSize.svg')

# DEVIATIONS
# display standard deviations of chunks
# read in the deviations from the file
def plot_deviations():
    plt.close('all')
    df_deviations = df_variances

    # get the chunk sizes and their mean variances
    chunk_sizes = list(sorted(set(df_deviations['length_of_chunk'])))
    for i,c in enumerate(chunk_sizes):
        chunk_sizes[i] = int(c)
    mean_chunk_deviations = []
    median_chunk_deviations = []
    # calculate the mean variance for each chunk size
    for size in chunk_sizes:
        mean_chunk_deviations.append(np.mean(df_deviations.loc[df_deviations['length_of_chunk'] == size]['std']))
        median_chunk_deviations.append(np.median(df_deviations.loc[df_deviations['length_of_chunk'] == size]['std']))


    # scatter them nicely
    plt.scatter(chunk_sizes, mean_chunk_deviations, label = 'mean values')
    plt.scatter(chunk_sizes, median_chunk_deviations, label = 'median values')
    plt.legend()
    plt.gcf().set_size_inches(14, 7)
    plt.ylabel('standard deviation of the GFI over all documents')
    plt.xlabel('length of chunk in sentences')
    plt.savefig('Plots/thesis/deviationsOnChunkSize.svg')



df = pd.read_csv("Results/resultsTheses.csv", header=0, index_col=0)
df = df.loc[df["complexity"]==3]

df_variances = pd.read_csv("Results/variancesTheses.csv", header=0, index_col=0)
df_variances = df_variances.loc[df_variances["complexity"]==3]

all_theses = ['en114417450.txt', 'en119716549.txt', 'en119767323.txt', 'en122940506.txt', 'en116249615.txt',
              'en115002482.txt', 'en117652377.txt', 'en117661421.txt']

#plot_boxplots()
#plot_barcharts()
#plot_scatterplot()
#plot_variances()
plot_deviations()

plt.close('all')

