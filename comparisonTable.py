import pandas as pd
import os
import numpy as np


# prepare English theses
df_theses_en = pd.read_csv("Results/English/resultsTheses.csv", header=0, index_col=0)
df_theses_en = df_theses_en.loc[df_theses_en["complexity"]==3]

variances_theses_en = pd.read_csv("Results/English/variancesTheses.csv", header=0, index_col=0)
variances_theses_en = variances_theses_en.loc[variances_theses_en["complexity"]==3]


# prepare German theses
df_theses_de = pd.read_csv("Results/German/resultsTheses.csv", header=0, index_col=0)
df_theses_de = df_theses_de.loc[df_theses_de["complexity"]==3]

variances_theses_de = pd.read_csv("Results/German/variancesTheses.csv", header=0, index_col=0)
variances_theses_de = variances_theses_de.loc[variances_theses_de["complexity"]==3]


# prepare English homework documents
df_0 = pd.read_csv("Results/English/results_0.csv", header=0, index_col=0)
df_1 = pd.read_csv("Results/English/results_1.csv", header=0, index_col=0)
df_2 = pd.read_csv("Results/English/results_2.csv", header=0, index_col=0)
df_3 = pd.read_csv("Results/English/results_3.csv", header=0, index_col=0)
# concatenate the results of the separate folders with documents
df_homeworks_en = pd.concat([df_0, df_1, df_2, df_3], ignore_index=True)
# look at the values of the definition with values of complexity 3 only
df_homeworks_en = df_homeworks_en.loc[df_homeworks_en['complexity'] == 3]
df_var_0 = pd.read_csv("Results/English/variancesHomework_0.csv", header=0, index_col=0)
df_var_1 = pd.read_csv("Results/English/variancesHomework_1.csv", header=0, index_col=0)
df_var_2 = pd.read_csv("Results/English/variancesHomework_2.csv", header=0, index_col=0)
df_var_3 = pd.read_csv("Results/English/variancesHomework_3.csv", header=0, index_col=0)
variances_homeworks_en = pd.concat([df_var_0, df_var_1, df_var_3], ignore_index=True)
# look at the values of the definition with values of complexity 3 only
variances_homeworks_en = variances_homeworks_en.loc[variances_homeworks_en['complexity']==3]


# prepare German assignments
essays_de = pd.read_csv("Results/German/resultsEssays.csv", header=0, index_col=0)
summaries_de = pd.read_csv("Results/German/resultsSummaries.csv", header=0, index_col=0)
df_homeworks_de = pd.concat([essays_de, summaries_de], ignore_index=True)
df_homeworks_de = df_homeworks_de.loc[df_homeworks_de['complexity'] == 3]

var_essays_de = pd.read_csv("Results/German/variancesEssays.csv", header=0, index_col=0)
var_summaries_de = pd.read_csv("Results/German/variancesSummaries.csv", header=0, index_col=0)
variances_homeworks_de = pd.concat([var_essays_de, var_summaries_de], ignore_index=True)
variances_homeworks_de = variances_homeworks_de.loc[variances_homeworks_de['complexity']==3]


statistics = {
    "type" : [],
    "number" : [],
    "chunk_size" : [],
    "mean_GFI" : [],
    "median_GFI" : [],
    "mean_std" : [],
    "max_len" : []
}

for m in [0, 100, 30, 10]:
    # zero means that all values are averaged independent of their chunk size
    if m == 0:
        # compute values for English theses
        statistics["chunk_size"].append(0)
        statistics["type"].append("English theses")
        statistics["number"].append(len(set(df_theses_en["document"])))
        statistics["mean_GFI"].append(np.mean(df_theses_en["GFI"]))
        statistics["median_GFI"].append(np.median(df_theses_en["GFI"]))
        statistics["mean_std"].append(np.mean(variances_theses_en["std"]))
        statistics["max_len"].append(np.max(df_theses_en["length_of_chunk"]))

        # compute values for German theses
        statistics["chunk_size"].append(0)
        statistics["type"].append("German theses")
        statistics["number"].append(len(set(df_theses_de["document"])))
        statistics["mean_GFI"].append(np.mean(df_theses_de["GFI"]))
        statistics["median_GFI"].append(np.median(df_theses_de["GFI"]))
        statistics["mean_std"].append(np.mean(variances_theses_de["std"]))
        statistics["max_len"].append(np.max(df_theses_de["length_of_chunk"]))

        # compute values for English homeworks
        statistics["chunk_size"].append(0)
        statistics["type"].append("English homeworks")
        statistics["number"].append(len(set(df_homeworks_en["document"])))
        statistics["mean_GFI"].append(np.mean(df_homeworks_en["GFI"]))
        statistics["median_GFI"].append(np.median(df_homeworks_en["GFI"]))
        statistics["mean_std"].append(np.mean(variances_homeworks_en["std"]))
        statistics["max_len"].append(np.max(df_homeworks_en["length_of_chunk"]))

        # compute values for German assignments
        statistics["chunk_size"].append(0)
        statistics["type"].append("German assignments")
        statistics["number"].append(len(set(df_homeworks_de["document"])))
        statistics["mean_GFI"].append(np.mean(df_homeworks_de["GFI"]))
        statistics["median_GFI"].append(np.median(df_homeworks_de["GFI"]))
        statistics["mean_std"].append(np.mean(variances_homeworks_de["std"]))
        statistics["max_len"].append(np.max(df_homeworks_de["length_of_chunk"]))

    # else m is the chunk size whose values are averaged
    else:
        # compute values for English theses
        statistics["chunk_size"].append(m)
        statistics["type"].append("English theses")
        statistics["number"].append(len(set(df_theses_en.loc[df_theses_en["length_of_chunk"]==m]["document"])))
        statistics["mean_GFI"].append(np.mean(df_theses_en.loc[df_theses_en["length_of_chunk"]==m]["GFI"]))
        statistics["median_GFI"].append(np.median(df_theses_en.loc[df_theses_en["length_of_chunk"]==m]["GFI"]))
        statistics["mean_std"].append(np.mean(variances_theses_en.loc[variances_theses_en["length_of_chunk"]==m]["std"]))
        statistics["max_len"].append(np.max(df_theses_en.loc[df_theses_en["length_of_chunk"]==m]["length_of_chunk"]))

        # compute values for German theses
        statistics["chunk_size"].append(m)
        statistics["type"].append("German theses")
        statistics["number"].append(len(set(df_theses_de.loc[df_theses_de["length_of_chunk"]==m]["document"])))
        statistics["mean_GFI"].append(np.mean(df_theses_de.loc[df_theses_de["length_of_chunk"]==m]["GFI"]))
        statistics["median_GFI"].append(np.median(df_theses_de.loc[df_theses_de["length_of_chunk"]==m]["GFI"]))
        statistics["mean_std"].append(np.mean(variances_theses_de.loc[variances_theses_de["length_of_chunk"]==m]["std"]))
        statistics["max_len"].append(np.max(df_theses_de.loc[df_theses_de["length_of_chunk"]==m]["length_of_chunk"]))

        # compute values for English homeworks
        statistics["chunk_size"].append(m)
        statistics["type"].append("English homeworks")
        statistics["number"].append(len(set(df_homeworks_en.loc[df_homeworks_en["length_of_chunk"]==m]["document"])))
        statistics["mean_GFI"].append(np.mean(df_homeworks_en.loc[df_homeworks_en["length_of_chunk"]==m]["GFI"]))
        statistics["median_GFI"].append(np.median(df_homeworks_en.loc[df_homeworks_en["length_of_chunk"]==m]["GFI"]))
        statistics["mean_std"].append(np.mean(variances_homeworks_en.loc[variances_homeworks_en["length_of_chunk"]==m]["std"]))
        statistics["max_len"].append(np.max(df_homeworks_en.loc[df_homeworks_en["length_of_chunk"]==m]["length_of_chunk"]))

        # compute values for German assignments
        statistics["chunk_size"].append(m)
        statistics["type"].append("German assignments")
        statistics["number"].append(len(set(df_homeworks_de.loc[df_homeworks_de["length_of_chunk"]==m]["document"])))
        statistics["mean_GFI"].append(np.mean(df_homeworks_de.loc[df_homeworks_de["length_of_chunk"]==m]["GFI"]))
        statistics["median_GFI"].append(np.median(df_homeworks_de.loc[df_homeworks_de["length_of_chunk"]==m]["GFI"]))
        statistics["mean_std"].append(np.mean(variances_homeworks_de.loc[variances_homeworks_de["length_of_chunk"]==m]["std"]))
        statistics["max_len"].append(np.max(df_homeworks_de.loc[df_homeworks_de["length_of_chunk"]==m]["length_of_chunk"]))

# convert the dictionary with the data to a dataframe
df_statistics = pd.DataFrame(data=statistics)
# write the collected data into a csv-file
data_out = open("Results/comparisonTable.csv", "w")
# convert the data to a csv and write it into the given file
data_out.write(df_statistics.to_csv())

df_10 = df_statistics.loc[df_statistics["chunk_size"]==10]
# write the collected data into a csv-file
data_out = open("Results/comparisonTable10.csv", "w")
# convert the data to a csv and write it into the given file
data_out.write(df_10.to_csv())

df_30 = df_statistics.loc[df_statistics["chunk_size"]==30]
# write the collected data into a csv-file
data_out = open("Results/comparisonTable30.csv", "w")
# convert the data to a csv and write it into the given file
data_out.write(df_30.to_csv())

df_100 = df_statistics.loc[df_statistics["chunk_size"]==100]
# write the collected data into a csv-file
data_out = open("Results/comparisonTable100.csv", "w")
# convert the data to a csv and write it into the given file
data_out.write(df_100.to_csv())

data_out.close()