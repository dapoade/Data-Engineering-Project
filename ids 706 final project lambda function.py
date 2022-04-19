import boto3


def lambda_handler(event, context):
	# TODO implement
	df = webscraper()
	write_s3(df, bucket= "daposbucket")

def webscraper():
	from urllib.request import urlopen
	from bs4 import BeautifulSoup
	import pandas as pd
	import numpy as np

	stats_list = []


	year = 2017
	# NBA season we will be analyzing
	# URL page we will scraping (see image above)
	#url = "https://www.basketball-reference.com/leagues/NBA_{}_advanced.html".format(year)

	url = "https://www.basketball-reference.com/leagues/NBA_{}_totals.html".format(year)

	# this is the HTML from the given URL
	html = urlopen(url)
	soup = BeautifulSoup(html)

	# use findALL() to get the column headers
	soup.findAll('tr', limit=2)

	# use getText()to extract the text we need into a list
	headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]

	# exclude the first column as we will not need the ranking order from Basketball Reference for the analysis
	headers = headers[1:]

	# avoid the first header row
	rows = soup.findAll('tr')[1:]
	player_stats = [[td.getText() for td in rows[i].findAll('td')]
		for i in range(len(rows))]


	all_stats = pd.DataFrame(player_stats, columns = headers)
	stats = all_stats.copy()


	#Add the year of the stats being produced
	stats[["Year"]] = year
	#subset stats to relevant variables
	stats = stats[["Player", "PTS", "TOV", "BLK", "STL", "AST", "3P", "FG%", "FT%" , "TRB", "G", "Tm"]]





	#get duplicate values
	player_total = all_stats[all_stats["Tm"] == "TOT"]
	#add year to duplicates to make easier to concatenate
	### player_total[["Year"]] = year

	stats_without_duplicates = stats[~stats["Player"].isin(player_total["Player"])]

	final_stats = stats_without_duplicates.append(player_total) #stats_without_duplicates.append(player_total[["Player", "BPM", "Year"]])



	final_stats = final_stats[final_stats.Player.notnull()]

	final_stats[["PTS"]] = final_stats[["PTS"]].astype(int)
	final_stats[["BLK"]] = final_stats[["BLK"]].astype(int)
	final_stats[["STL"]] = final_stats[["STL"]].astype(int)
	final_stats[["AST"]] = final_stats[["AST"]].astype(int)
	final_stats[["TRB"]] = final_stats[["TRB"]].astype(int)
	final_stats[["G"]] = final_stats[["G"]].astype(float)


	final_stats[["PTS"]] = final_stats[["PTS"]].values / final_stats[["G"]].values
	final_stats[["BLK"]] = final_stats[["BLK"]].values / final_stats[["G"]].values
	final_stats[["STL"]] = final_stats[["STL"]].values / final_stats[["G"]].values
	final_stats[["AST"]] = final_stats[["AST"]].values / final_stats[["G"]].values
	final_stats[["TRB"]] = final_stats[["TRB"]].values / final_stats[["G"]].values

	final_stats = final_stats[["Player", "PTS", "TOV", "BLK", "STL", "AST", "3P", "FG%", "FT%" , "TRB", "G", "Tm"]]

	stats_list.append(final_stats)


	df123 = pd.concat(stats_list)

	return(df123)


def write_s3(df, bucket):

	from io import StringIO

	"""
	Write S3 Bucket
	"""
	csv_buffer = StringIO()
	df.to_csv(csv_buffer)
	s3_resource = boto3.resource('s3')
	response = s3_resource.Object(bucket, 'stats_list.csv').put(Body=csv_buffer.getvalue())
