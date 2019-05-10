import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df_0 = pd.read_csv("results_0.csv", header=0, index_col=0)
df_1 = pd.read_csv("results_1.csv", header=0, index_col=0)
df_2 = pd.read_csv("results_2.csv", header=0, index_col=0)
df_3 = pd.read_csv("results_3.csv", header=0, index_col=0)

# concatenate the results of the separate folders with documents
df = pd.concat([df_0, df_1, df_2, df_3], ignore_index=True)


# BOXPLOT
# show all the boxplots of all documents' GFIs for chunk size m next to each other
for m in [40, 35, 30, 28, 26, 24, 22, 20, 18, 16, 14, 12, 10]: # setting m to a high number doesn't make sense for boxplots
    my_doc_chunk_m = df.loc[df['length_of_chunk'] == m]
    my_doc_chunk_m.boxplot(column='GFI', by='document', figsize=(14,7))
    plt.ylabel('GFI')
    plt.figtext(0.995, 0.01, 'the chunk size is ' + str(m), ha='right', va='bottom')
    plt.savefig('Plots/homework/boxplot/' + str(m) + 'longChunksBoxplottedAllHomeworks.svg')


all_homeworks = ['aff-case/9536669.txt', 'aff-case/9514020.txt', 'aff-case/9534163.txt', 'aff-case/9534039.txt',
                 'aff-case/9535872.txt', 'aff-case/9536689.txt', 'aff-case/9533580.txt', 'aff-case/9535758.txt',
                 'aff-case/9536557.txt', 'aff-case/9534905.txt', 'aff-case/9534539.txt', 'aff-case/9534582.txt',
                 'aff-case/9565310.txt', 'aff-case/9535669.txt', 'aff-case/9536591.txt', 'aff-case/9535696.txt',
                 'aff-case/9531446.txt', 'aff-case/9535056.txt', 'aff-case/9526629.txt', 'aff-case/9532292.txt',
                 'aff-case/9537480.txt', 'aff-case/9539821.txt', 'aff-case/9535252.txt', 'aff-case/9536298.txt',
                 'aff-case/9540664.txt', 'aff-case/9534864.txt', 'aff-case/9526685.txt', 'aff-case/9535288.txt',
                 'osmosis/124007948.txt', 'osmosis/124006337.txt', 'osmosis/124007677.txt', 'osmosis/124006584.txt',
                 'osmosis/124009624.txt', 'osmosis/124007246.txt', 'osmosis/124006947.txt', 'osmosis/124009829.txt',
                 'osmosis/124009088.txt', 'osmosis/123995860.txt', 'osmosis/124009461.txt', 'osmosis/124009486.txt',
                 'osmosis/124007471.txt', 'osmosis/124006331.txt', 'osmosis/124007131.txt', 'osmosis/124012040.txt',
                 'osmosis/124008444.txt', 'essays/122565974.txt', 'essays/122557523.txt', 'essays/122753914.txt',
                 'essays/122543380.txt', 'essays/121118264.txt', 'essays/122543254.txt', 'essays/121118263.txt',
                 'essays/122752875.txt', 'essays/122566014.txt', 'essays/122557146.txt', 'essays/122566103.txt',
                 'essays/122566028.txt', 'essays/122544324.txt', 'essays/121155857.txt', 'essays/122569027.txt',
                 'essays/122546705.txt', 'essays/122752406.txt', 'essays/122557093.txt', 'essays/122753520.txt',
                 'essays/122543389.txt', 'essays/122546708.txt', 'essays/122577664.txt', 'essays/122568959.txt',
                 'essays/121117570.txt', 'essays/121118273.txt', 'essays/122543379.txt', 'essays/122556190.txt',
                 'essays/122556296.txt', 'essays/122753349.txt', 'mission-command/9465835.txt',
                 'mission-command/9487595.txt', 'mission-command/9489831.txt', 'mission-command/9462586.txt',
                 'mission-command/9489875.txt', 'mission-command/9481043.txt', 'mission-command/9462411.txt',
                 'mission-command/9461712.txt', 'mission-command/9490023.txt', 'mission-command/9462406.txt',
                 'mission-command/9474049.txt', 'mission-command/9489856.txt', 'mission-command/9478109.txt',
                 'mission-command/9487780.txt', 'mission-command/9487828.txt', 'mission-command/9462342.txt',
                 'mission-command/9466829.txt', 'mission-command/9489859.txt', 'mission-command/9481116.txt',
                 'mission-command/9489866.txt', 'mission-command/9463242.txt', 'mission-command/9489815.txt',
                 'mission-command/9487536.txt', 'mission-command/10145044.txt', 'mission-command/9461991.txt',
                 'mission-command/9489819.txt', 'mission-command/9461911.txt', 'mission-command/9489857.txt',
                 'mission-command/9490214.txt', 'mission-command/9489842.txt']



# BAR CHART
for homework in all_homeworks:
    for m in [20, 18, 16, 14, 12, 10]: # doesn't make sense with bigger m, since there is only one bar then
        plt.close('all')
        this_doc_len_m_ = df.loc[df['document'] == homework]
        this_doc_len_m = this_doc_len_m_.loc[df['length_of_chunk'] == m]
        if this_doc_len_m.empty == True:
            continue
        ints = []
        for i in this_doc_len_m['number_of_chunk']:
            ints.append(int(i))
        if len(ints) < 6:
            continue
        plt.bar(ints,this_doc_len_m['GFI'])
        plt.gcf().set_size_inches(7, 3.5)
        plt.ylabel('GFI')
        plt.xlabel('number of chunk (from beginning to end)')
        plt.figtext(0.995, 0.01, 'the chunk size is ' + str(m), ha='right', va='bottom')
        plt.savefig('Plots/homework/bar/' + str(m) + "_long_" + homework[-6:] + 'indicesOverNumberOfChunk.svg')


# SCATTER PLOT
for homework in all_homeworks:
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
    plt.savefig('Plots/homework/scatter/' + homework[-11:-4] + 'indicesOverChunkSize.svg')

plt.close('all')
# VARIANCES
# display variances of chunks
# read in the variances from the file
df_var_0 = pd.read_csv("variancesHomework_0.csv", header=0, index_col=0)
df_var_1 = pd.read_csv("variancesHomework_1.csv", header=0, index_col=0)
#df_var_2 = pd.read_csv("variancesHomework_2.csv", header=0, index_col=0) OSMOSIS
df_var_3 = pd.read_csv("variancesHomework_3.csv", header=0, index_col=0)

df_variances = pd.concat([df_var_0, df_var_1, df_var_3], ignore_index=True)

# get the chunk sizes and their mean variances
chunk_sizes = list(set(df_variances['length_of_chunk']))
for i,c in enumerate(chunk_sizes):
    chunk_sizes[i] = int(c)
mean_chunk_variances = []
# calculate the mean variance for each chunk size
for size in chunk_sizes:
    mean_chunk_variances.append(np.mean(df_variances.loc[df_variances['length_of_chunk'] == size]['variance']))

# scatter them nicely
plt.scatter(chunk_sizes, mean_chunk_variances)
plt.gcf().set_size_inches(14, 7)
plt.ylabel('mean variance of the GFI over all documents')
plt.xlabel('length of chunk in sentences')
plt.savefig('Plots/homework/variances.svg')
