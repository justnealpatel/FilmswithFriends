import pandas

file1 = 'title.basics.tsv'
file2 = 'title.ratings.tsv'

titles = pandas.read_table(file1)
ratings = pandas.read_table(file2)
merged = titles.merge(ratings, on='tconst')
merged.to_csv("imdb_data.csv", index=False)