import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
colors_list = list(colors._colors_full_map.values())

# BOXPLOT
# show all the boxplots of all documents' GFIs for chunk size m next to each other
def plot_boxplots():
    for m in [50, 40, 30, 20, 10]:
        #fig, ax = plt.subplots()

        df_m = df.loc[df_theses_en['length_of_chunk'] == m]
        df_m.boxplot(column='GFI', by='document', figsize=(14,7), vert = False)

        #thesis_de = df_theses_de.loc[df_theses_de['length_of_chunk'] == m].loc[df_theses_de["document"]=='de124313811.txt']
        #thesis_de.boxplot(column='GFI', by='document', figsize=(14,7), ax = ax, vert = False)

        #mission_en = df_missions_en.loc[df_missions_en['length_of_chunk'] == m].loc[df_missions_en["document"]=='mission-command/9461991.txt']
        #mission_en.boxplot(column='GFI', by='document', figsize=(14,7), ax = ax, vert = False)

        #essay_de = df_essays_de.loc[df_essays_de['length_of_chunk'] == m].loc[df_essays_de["document"]=='L1/dew15_2007_09.txt']
        #essay_de.boxplot(column='GFI', by='document', figsize=(14,7), ax = ax, vert = False)

        plt.suptitle('GFI for chunks of size ' + str(m) + ' grouped by document', fontsize=14)
        plt.ylabel('GFI')
        plt.xticks(rotation=90)
        plt.savefig('Plots/comparison/boxplot/' + str(m) + 'longChunks.svg')

# prepare English theses
df_theses_en = pd.read_csv("Results/English/resultsTheses.csv", header=0, index_col=0)
df_theses_en = df_theses_en.loc[df_theses_en["complexity"]==3]

variances_theses_en = pd.read_csv("Results/English/variancesTheses.csv", header=0, index_col=0)
variances_theses_en = variances_theses_en.loc[variances_theses_en["complexity"]==3]

all_theses_en = ['en114417450.txt', 'en119716549.txt', 'en119767323.txt', 'en116249615.txt',
              'en115002482.txt', 'en117652377.txt', 'en117661421.txt']

# prepare German theses
df_theses_de = pd.read_csv("Results/German/resultsTheses.csv", header=0, index_col=0)
df_theses_de = df_theses_de.loc[df_theses_de["complexity"]==3]

variances_theses_de = pd.read_csv("Results/German/variancesTheses.csv", header=0, index_col=0)
variances_theses_de = variances_theses_de.loc[variances_theses_de["complexity"]==3]

all_theses_de = ['de122603393.txt', 'de123666862.txt', 'de116971348.txt', 'de113804971.txt',
              'de115685280.txt', 'de118611757.txt', 'de120662601.txt', 'de118628474.txt', 'de117909802.txt',
              'de118653524.txt', 'de124313811.txt', 'de122223299.txt', 'de11006290.txt',
              'de117710690.txt', 'de120500224.txt', 'de115078652.txt', 'de124051169.txt',
              'de115639573.txt', 'de115101969.txt', 'de119427502.txt', 'de118043324.txt', 'de120960357.txt',
              'de118627493.txt', 'de122449695.txt', 'de123748878.txt', 'de118577040.txt', 'de123255864.txt']

# prepare English mission documents
df_missions_en = pd.read_csv("Results/English/results_3.csv", header=0, index_col=0)
df_missions_en = df_missions_en.loc[df_missions_en["complexity"]==3]

variances_missions_en = pd.read_csv("Results/English/variancesHomework_3.csv", header=0, index_col=0)
variances_missions_en = variances_missions_en.loc[variances_missions_en["complexity"]==3]

all_missions = ['mission-command/9465835.txt', 'mission-command/9489831.txt', 'mission-command/9462586.txt',
                 'mission-command/9489875.txt', 'mission-command/9481043.txt', 'mission-command/9462411.txt',
                 'mission-command/9461712.txt', 'mission-command/9490023.txt', 'mission-command/9462406.txt',
                 'mission-command/9474049.txt', 'mission-command/9489856.txt', 'mission-command/9478109.txt',
                 'mission-command/9487780.txt', 'mission-command/9487828.txt', 'mission-command/9462342.txt',
                 'mission-command/9466829.txt', 'mission-command/9489859.txt', 'mission-command/9481116.txt',
                 'mission-command/9489866.txt', 'mission-command/9463242.txt', 'mission-command/9489815.txt',
                 'mission-command/9487536.txt', 'mission-command/10145044.txt', 'mission-command/9461991.txt',
                 'mission-command/9489819.txt', 'mission-command/9461911.txt', 'mission-command/9489857.txt',
                 'mission-command/9490214.txt', 'mission-command/9489842.txt', 'mission-command/9487595.txt']

# prepare German essays
df_essays_de = pd.read_csv("Results/German/resultsEssays.csv", header=0, index_col=0)
df_essays_de = df_essays_de.loc[df_essays_de['complexity'] == 3]

variances_essays_de = pd.read_csv("Results/German/variancesEssays.csv", header=0, index_col=0)
variances_essays_de = variances_essays_de.loc[variances_essays_de['complexity']==3]

all_essays = []
for f in os.listdir("Data/German/essays/L1"):
    all_essays.append("L1/"+f)



# put some suitable ones together
max_name = df_theses_en[df_theses_en['length_of_chunk']==df_theses_en['length_of_chunk'].max()]['document']

#maximum = df_theses_en.loc[df_theses_en["length_of_chunk"].idxmax()]
#print(maximum)
#maximum_name = df_theses_en[maximum]["document"]
print(max_name)
df_0 = df_theses_en.loc[df_theses_en["document"] == max_name[1]]
print(df_0)


maximum_name = df_theses_de["length_of_chunk"]==np.max(df_theses_de["length_of_chunk"])["document"]
df_1 = df_theses_de.loc[df_theses_de["document"] == maximum_name]

maximum_name = df_missions_en["length_of_chunk"]==np.max(df_missions_en["length_of_chunk"])["document"]
df_2 = df_missions_en.loc[df_missions_en["document"] == maximum_name]

maximum_name = df_essays_de["length_of_chunk"]==np.max(df_essays_de["length_of_chunk"])["document"]
df_3 = df_essays_de.loc[df_essays_de["document"] == maximum_name]

df = pd.concat([df_0, df_1, df_2, df_3], ignore_index=True)

plot_boxplots()

plt.close("all")