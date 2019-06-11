import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



# BOXPLOT
# show all the boxplots of all documents' GFIs for chunk size m next to each other
def plot_boxplots():
    for m in [1000, 750, 500, 450, 400, 350, 300, 250, 200, 150, 100, 75, 50, 40, 30, 20, 10]:
        my_doc_chunk_m = df.loc[df['length_of_chunk'] == m]
        my_doc_chunk_m.boxplot(column='GFI', by='document', figsize=(14,7))
        plt.suptitle('GFI for chunks of size ' + str(m) + ' grouped by document', fontsize=14)
        plt.ylabel('GFI')
        plt.xticks(rotation=90)
        plt.savefig('Plots/German/theses/box/' + str(m) + 'longChunksBoxplottedAllTheses.svg')


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
            plt.suptitle('GFI for the chunks of size ' + str(m) + ' of document ' + thesis, fontsize=14)
            plt.savefig('Plots/German/theses/bar/' + str(m) + "_long_" + thesis + 'indicesOverNumberOfChunk.svg')


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
        plt.suptitle('GFI values of the different chunk sizes of document ' + thesis, fontsize=14)
        plt.savefig('Plots/German/theses/scatter/' + thesis + 'indicesOverChunkSize.svg')



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
    plt.suptitle('Variances of GFI values of the different chunk sizes over all documents', fontsize=14)
    plt.savefig('Plots/German/theses/variancesOnChunkSize.svg')



# DEVIATIONS
# display standard deviations of chunks
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
    plt.suptitle('Deviations of GFI values of the different chunk sizes over all documents', fontsize=14)
    plt.savefig('Plots/German/theses/deviationsOnChunkSize.svg')



df = pd.read_csv("Results/German/resultsTheses.csv", header=0, index_col=0)
df = df.loc[df["complexity"]==3]

df_variances = pd.read_csv("Results/German/variancesTheses.csv", header=0, index_col=0)
df_variances = df_variances.loc[df_variances["complexity"]==3]

all_theses = ['de122603393.txt', 'de123666862.txt', 'de118124834.txt', 'de116971348.txt', 'de113804971.txt',
              'de115685280.txt', 'de118611757.txt', 'de120662601.txt', 'de118628474.txt', 'de117909802.txt',
              'de118653524.txt', 'de124313811.txt', 'de122223299.txt', 'de11157308.txt', 'de11006290.txt',
              'de117710690.txt', 'de11109527.txt', 'de120500224.txt', 'de115078652.txt', 'de124051169.txt',
              'de115639573.txt', 'de115101969.txt', 'de119427502.txt', 'de118043324.txt', 'de120960357.txt',
              'de118627493.txt', 'de122449695.txt', 'de123748878.txt', 'de118577040.txt', 'de123255864.txt']

plot_boxplots()
plot_barcharts()
plot_scatterplot()
plot_variances()
plot_deviations()

plt.close('all')

