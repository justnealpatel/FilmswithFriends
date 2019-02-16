title_file = "title.basics.tsv"
rating_file = "title.ratings.tsv"
movie_file = "imdb_data.csv"

titles = open(title_file, "r")
ratings = open(rating_file, "r")
movies = open(movie_file, "r")
title_lines = 0
rating_lines = 0
movie_lines = 0

for line in titles.readlines():
	title_lines = title_lines+1
titles.close()
for line in ratings.readlines():
	rating_lines = rating_lines+1
ratings.close()
for line in movies.readlines():
	movie_lines = movie_lines+1
movies.close()

print "Number of lines in " + title_file, title_lines
print "Number of lines in " + rating_file, rating_lines
print "Number of lines in " + movie_file, movie_lines