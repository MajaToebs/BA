import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



# SCATTER PLOT
def plot_scatterplot():
    for thesis in all_theses:
        plt.close('all')
        this_doc = df.loc[df['document'] == thesis]
        this_doc_shortened = df_shortened.loc[df_shortened['document'] == thesis]

        # scatter the GFIs depending on the chunk size
        plt.scatter(this_doc['length_of_chunk'], this_doc['GFI'], color = 'orange', label = 'with all sentences')
        plt.scatter(this_doc_shortened['length_of_chunk'], this_doc_shortened['GFI'], color = 'red', label = 'without outlier sentences')
        plt.gcf().set_size_inches(14, 7)
        plt.legend()

        # calculate the mean GFIs for each chunk size
        mean_GFIs = { 'len' : [],
                      'mean' : []}
        for l in sorted(set(this_doc['length_of_chunk'])):
            values = this_doc.loc[this_doc['length_of_chunk'] == l]['GFI']
            mean_GFIs['len'].append(l)
            mean_GFIs['mean'].append(np.mean(values))

        # calculate the mean GFIs for each chunk size for shortened sentences
        mean_GFIs_shortened = { 'len' : [],
                                'mean' : []}
        for l in sorted(set(this_doc_shortened['length_of_chunk'])):
            values = this_doc_shortened.loc[this_doc_shortened['length_of_chunk'] == l]['GFI']
            mean_GFIs_shortened['len'].append(l)
            mean_GFIs_shortened['mean'].append(np.mean(values))

        # insert the means into the plot
        plt.plot(mean_GFIs['len'], mean_GFIs['mean'], 'k-', color='orange')
        plt.plot(mean_GFIs_shortened['len'], mean_GFIs_shortened['mean'], 'k-', color='red')
        plt.ylabel('GFI')
        plt.xlabel('length of chunk in sentences')
        #plt.suptitle('Comparison of GFI values of the different chunk sizes of document ' + thesis, fontsize=14)
        plt.savefig('Plots/English/outliers/' + thesis + 'indicesOverChunkSizeShortenedSentences.svg', bbox_inches='tight')




# DEVIATIONS
# display standard deviations of chunks
def plot_deviations():
    plt.close('all')
    df_deviations = df_variances
    df_deviations_shortened = df_variances_shortened

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

    # get the chunk sizes and their mean variances for the manipulated data
    chunk_sizes_shortened = list(sorted(set(df_deviations_shortened['length_of_chunk'])))
    for i,c in enumerate(chunk_sizes_shortened):
        chunk_sizes_shortened[i] = int(c)
    mean_chunk_deviations_shortened = []
    median_chunk_deviations_shortened = []
    # calculate the mean variance for each chunk size
    for size in chunk_sizes_shortened:
        mean_chunk_deviations_shortened.append(np.mean(df_deviations_shortened.loc[df_deviations_shortened['length_of_chunk'] == size]['std']))
        median_chunk_deviations_shortened.append(np.median(df_deviations_shortened.loc[df_deviations_shortened['length_of_chunk'] == size]['std']))

    # scatter the medians nicely

    x_s_1 = chunk_sizes + chunk_sizes_shortened
    y_s_1 = median_chunk_deviations + median_chunk_deviations_shortened
    colors = []
    for i in range(len(chunk_sizes)):
        colors.append("orange")
    for i in range(len(chunk_sizes)):
        colors.append("red")
    plt.scatter(x_s_1, y_s_1, color = colors)

    #plt.legend()
    plt.gcf().set_size_inches(14, 7)
    plt.ylabel('standard deviation of the GFI over all documents')
    plt.xlabel('length of chunk in sentences')
    #plt.suptitle('Comparison of how the definition of the end of a sentence influences\n'
    #             'the standard deviations of GFI values of the different chunk sizes over all documents', fontsize=14)
    plt.savefig('Plots/English/outliers/deviationsOnChunkSizeShortenedSentences.svg', bbox_inches='tight')



df = pd.read_csv("Results/English/resultsTheses.csv", header=0, index_col=0)
df = df.loc[df["complexity"]==3]

# the theses where ";" and ":" have been replaced by "."
df_shortened = pd.read_csv("Results/English/resultsThesesOutliers.csv", header=0, index_col=0)
df_shortened = df_shortened.loc[df_shortened["complexity"]==3]

df_variances = pd.read_csv("Results/English/variancesTheses.csv", header=0, index_col=0)
df_variances = df_variances.loc[df_variances["complexity"]==3]

# the theses where ";" and ":" have been replaced by "."
df_variances_shortened = pd.read_csv("Results/English/variancesThesesOutliers.csv", header=0, index_col=0)
df_variances_shortened = df_variances_shortened.loc[df_variances_shortened["complexity"]==3]

all_theses = ['en114417450.txt', 'en119716549.txt', 'en119767323.txt', 'en116249615.txt',
              'en115002482.txt', 'en117652377.txt', 'en117661421.txt']


plot_scatterplot()
plot_deviations()

plt.close('all')

