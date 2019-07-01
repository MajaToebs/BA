# BA
Python code of my bachelor thesis on readability measures (mostly the Gunning Fog Index) for intrinsic plagiarism analysis

The resulting figures and plots of them are available as well

## Required Packages
- Textstat
- NLTK
- Pyphen
- Numpy
- Matplotlib
- Pandas
- Sys
- OS
- RE

## Testing
To test the methods I used, just exchange the file names in my code with the data you have and execute the code.
The files starting with "preprocess" should be used to preprocess your data, the files starting with "fog" can be used to calculate the Gunning Fog Indices of your data, the files starting with "plot" can be used to plot the results of your tests and the files starting with "indices" or "comparison" are for comparison of different readability measures and document types. Finally, all files starting with "stability" were used to adapt the Gunning Fog Index for further stability of the obtained results.
