import csv
with open('imdb_data.csv', 'rU') as inp, open('movies.csv', 'w') as out:
    writer = csv.writer(out)
    for row in csv.reader(inp):
        if row[1] == "movie":
            writer.writerow(row)