import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.colors as colors
colors_list = list(colors._colors_full_map.values())


# BOXPLOT
# show all the boxplots of all documents' GFIs for chunk size m next to each other
def plot_boxplot(type):
    for m in [40, 35, 30, 28, 26, 24, 22, 20, 18, 16, 14, 12, 10]: # setting m to a high number doesn't make sense for boxplots
        my_doc_chunk_m = df.loc[df['length_of_chunk'] == m]
        if len(my_doc_chunk_m) > 5:
            my_doc_chunk_m.boxplot(column='GFI', by='document', figsize=(14,7), )
            plt.suptitle('GFI for chunks of size ' + str(m) + ' grouped by document', fontsize=14)
            plt.ylabel('GFI')
            plt.xticks(rotation=90)
            plt.savefig('Plots/German/assignments/' + type + '/' + str(m) + 'longChunksBoxplottedAllHomeworks.svg', bbox_inches='tight')



# BAR CHART
def plot_barchart(type):
    if type == "essays":
        documents = all_essays
    else:
        documents = all_summaries

    for homework in documents:
        for m in [20, 18, 16, 14, 12, 10]: # doesn't make sense with bigger m, since there is only one bar then
            plt.close('all')
            this_doc_len_m_ = df.loc[df['document'] == homework]
            this_doc_len_m = this_doc_len_m_.loc[df['length_of_chunk'] == m]
            if this_doc_len_m.empty == True:
                continue
            ints = []
            for i in this_doc_len_m['number_of_chunk']:
                ints.append(int(i))
            if len(ints) < 5:
                continue
            plt.bar(ints,this_doc_len_m['GFI'])
            plt.gcf().set_size_inches(7, 3.5)
            plt.ylabel('GFI')
            plt.xlabel('number of chunk (from beginning to end)')
            #plt.suptitle('GFI for the chunks of size ' + str(m) + ' of document ' + homework, fontsize=14)
            plt.savefig('Plots/German/assignments/' + type + '/' + str(m) + "_long_" + homework[-6:] + 'indicesOverNumberOfChunk.svg', bbox_inches='tight')

# STRUCTURE CHART
def plot_structure(type):
    for m in [100, 75, 50, 40, 30, 20, 10]:
        plt.close('all')
        rel_chunks = df.loc[df['length_of_chunk']==m]
        colors = []
        if type == "essays":
            all_docs = all_essays
        else:
            all_docs = all_summaries
        for c, thesis in enumerate(all_docs[0:13]):
            this_doc_len_m = rel_chunks.loc[rel_chunks['document']==thesis]
            if this_doc_len_m.empty == True:
                continue
            ints = []
            max_number_of_this_chunk = np.max(this_doc_len_m['number_of_chunk'])
            for i in this_doc_len_m['number_of_chunk']:
                # transform the chunk number into a percentage of how far in the document this chunk is
                ints.append(100 * int(i) / max_number_of_this_chunk)
            # have to apend color as well?!
            for i in range(len(ints)):
                colors.append(colors_list[c])
            plt.plot(ints, this_doc_len_m['GFI'], '-o', color = colors_list[c])

        # when the lines of all theses are there, we can combine them in one plot and store it
        plt.gcf().set_size_inches(14, 7)
        plt.ylabel('GFI')
        plt.xlabel("document's percentage of the chunk's end")
        #plt.suptitle('GFI for the chunks of size ' + str(m) + ' of document', fontsize=14)
        plt.savefig('Plots/German/assignments/' + type + '/structure/all' + str(m) + '_long_indicesOverNumberOfChunk.svg', bbox_inches='tight')


# SCATTER PLOT
def plot_scatterplot(type):
    if type == "essays":
        documents = all_essays
    else:
        documents = all_summaries

    for homework in documents:
        plt.close('all')
        this_doc = df.loc[df['document'] == homework]

        # not interesting to plot, since there are just too few values
        if len(this_doc['length_of_chunk']) < 20:
            continue

        # scatter the GFIs depending on the chunk size
        plt.scatter(this_doc['length_of_chunk'], this_doc['GFI'])
        plt.gcf().set_size_inches(14, 7)

        # calculate the mean GFIs for each chunk size
        mean_GFIs = {'len': [],
                     'mean': []}
        for l in sorted(set(this_doc['length_of_chunk'])):
            values = this_doc.loc[this_doc['length_of_chunk'] == l]['GFI']
            mean_GFIs['len'].append(l)
            mean_GFIs['mean'].append(np.mean(values))

        # insert the means into the plot
        plt.plot(mean_GFIs['len'], mean_GFIs['mean'], 'k-', color='r')
        plt.ylabel('GFI')
        plt.xlabel('length of chunk in sentences')
        #plt.suptitle('GFI values of the different chunk sizes of document ' + homework, fontsize=14)
        plt.savefig('Plots/German/assignments/' + type + '/' + homework[-11:-4] + 'indicesOverChunkSize.svg', bbox_inches='tight')


# DISTRIBUTION PLOT
def plot_distribution(type):
    for m in [100, 75, 50, 40, 30, 20, 10]:
        plt.close('all')
        df_of_len = df.loc[df['length_of_chunk']==m]
        if type == "essays":
            all_docs = all_essays
        else:
            all_docs = all_summaries

        for c, thesis in enumerate(all_docs[4:13]):
            this_doc_of_len = df_of_len.loc[df_of_len["document"]==thesis]
            plt.hist(this_doc_of_len['GFI'], density = True, bins = np.arange(5,20), color = colors_list[c+313], alpha=0.3, histtype="bar")
        plt.gcf().set_size_inches(14, 7)
        plt.ylabel('probability')
        plt.xlabel('GFI')
        #plt.suptitle('distribution of GFI values of size ' + str(m) + ' of all homeworks', fontsize=14)
        plt.savefig('Plots/German/assignments/' + type + '/distribution/' + str(m) + '.svg', bbox_inches='tight')




# VARIANCES
# display variances of chunks
# read in the variances from the file
def plot_variances(type):
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
    #plt.suptitle('Variances of GFI values of the different chunk sizes over all documents', fontsize=14)
    plt.savefig('Plots/German/assignments/' + type + '/variances.svg', bbox_inches='tight')



# DEVIATIONS
# display deviations of chunks
def plot_deviations(type):
    plt.close('all')

    df_deviations = df_variances

    # get the chunk sizes and their mean variances
    chunk_sizes = list(sorted(set(df_deviations['length_of_chunk'])))
    for i, c in enumerate(chunk_sizes):
        chunk_sizes[i] = int(c)
    mean_chunk_deviations = []
    median_chunk_deviations = []
    # calculate the mean deviation for each chunk size
    for size in chunk_sizes:
        mean_chunk_deviations.append(np.mean(df_deviations.loc[df_deviations['length_of_chunk'] == size]['std']))
        median_chunk_deviations.append(np.median(df_deviations.loc[df_deviations['length_of_chunk'] == size]['std']))

    # scatter them nicely
    plt.scatter(chunk_sizes, mean_chunk_deviations, label='mean values')
    plt.scatter(chunk_sizes, median_chunk_deviations, label='median values')
    plt.legend()
    plt.gcf().set_size_inches(14, 7)
    plt.ylabel('mean deviations of the GFI over all documents')
    plt.xlabel('length of chunk in sentences')
    #plt.suptitle('Deviations of GFI values of the different chunk sizes over all documents', fontsize=14)
    plt.savefig('Plots/German/assignments/' + type + '/deviations.svg', bbox_inches='tight')






# get the texts we want to analyze
all_essays = []
summaries_to_analyze = []
# executes for all files in one directory
for f in os.listdir("Data/German/essays/L1"):
    all_essays.append("L1/"+f)
df = pd.read_csv("Results/German/resultsEssays.csv", header=0, index_col=0)
# look at the values of the definition with values of complexity 3 only
df = df.loc[df['complexity'] == 3]
df_variances = pd.read_csv("Results/German/variancesEssays.csv", header=0, index_col=0)
# look at the values of the definition with values of complexity 3 only
df_variances = df_variances.loc[df_variances['complexity']==3]

print("start plotting essays")
#plot_boxplot("essays")
#plot_barchart("essays")
#plot_scatterplot("essays")
#plot_variances("essays")
#plot_deviations("essays")
#plot_structure("essays")
plot_distribution("essays")

plt.close('all')



all_summaries = []
for f in os.listdir("Data/German/essays/summaryL1"):
    all_summaries.append("summaryL1/"+f)
df = pd.read_csv("Results/German/resultsSummaries.csv", header=0, index_col=0)
# look at the values of the definition with values of complexity 3 only
df = df.loc[df['complexity'] == 3]
df_variances = pd.read_csv("Results/German/variancesSummaries.csv", header=0, index_col=0)
# look at the values of the definition with values of complexity 3 only
df_variances = df_variances.loc[df_variances['complexity']==3]

print("start plotting summaries")
#plot_boxplot("summaries")
#plot_barchart("summaries")
#plot_scatterplot("summaries")
#plot_variances("summaries")
#plot_deviations("summaries")
#plot_structure("summaries")
plot_distribution("summaries")

plt.close('all')