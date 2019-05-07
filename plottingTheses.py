import pandas as pd
import matplotlib.pyplot as plt

#my_doc_chunk_m = df.loc[df['document'].isin(['en117661421.txt', 'en119716549.txt', 'en114417450.txt'])].loc[df['length_of_chunk'] == 100]
#print(df.loc[:,['document', 'length_of_chunk', 'GFI']]) choosing columns to be displayed


df = pd.read_csv("resultsTheses.csv", header=0,index_col=0)
all_theses = ['en114417450.txt', 'en119716549.txt', 'en119767323.txt', 'en122940506.txt', 'en116249615.txt', 'en115002482.txt', 'en117652377.txt', 'en117661421.txt']

# BOXPLOT
# show all the boxplots of all documents' GFIs for chunk size m next to each other

for m in [400, 300, 200, 100, 50, 40, 30, 20, 10]:
    my_doc_chunk_m = df.loc[df['length_of_chunk'] == m]
    #print(my_doc_chunk_m.describe()) gives one the most common statistics
    my_doc_chunk_m.boxplot(column='GFI', by='document', figsize=(14,7))
    plt.title = "length" + str(m)
    plt.figtext(0.995, 0.01, 'the chunk size is ' + str(m), ha='right', va='bottom')
    # before saving, I should adjust the size, since the x-labels won't be readable otherwise
    plt.savefig('/Plots/' + str(m) + 'longChunksBoxplottedAllTheses.svg')




'''
# Plot Type: Bar Chart
for m in [100, 50, 40, 30, 20, 10]:
    for thesis in all_theses:
        this_doc_len_m = df.loc[df['document']==thesis].loc[df['length_of_chunk']==m]
        ints = []
        for i in this_doc_len_m['number_of_chunk']:
            ints.append(int(i))
        plt.bar(ints,this_doc_len_m['GFI'])
        plt.gcf().set_size_inches(7, 3.5)
        plt.title("Thesis " + thesis)
        plt.ylabel('GFI')
        plt.xlabel('number of chunk (from beginning to end)')
        plt.figtext(0.995, 0.01, 'the chunk size is ' + str(m), ha='right', va='bottom')
        plt.savefig('/Plots/' + thesis + 'indicesOverNumberOfChunk.svg')
    #plt.show()


# Plot Type: Scatter Plot
for thesis in all_theses:
    this_doc = df.loc[df['document']==thesis]
    plt.scatter(this_doc['length_of_chunk'], this_doc['GFI'])
    plt.gcf().set_size_inches(14, 7)
    plt.title("Thesis " + thesis)
    plt.ylabel('GFI')
    plt.xlabel('length of chunk in sentences')
    #plt.savefig('/Plots/' + thesis + 'indicesOverChunkSize.svg')
'''

plt.show()