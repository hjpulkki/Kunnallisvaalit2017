from BeautifulSoup import BeautifulSoup, Comment
import urllib
import re
import csv

KUNTA = "helsinki"

def get_candidate(id):
        url = "http://www.vaalikone.fi/kunta2017/" + str(id)
        f = urllib.urlopen(url)
        full_page = f.read()
        bs = BeautifulSoup(full_page)
	return bs


# Create file
csvfile = open(KUNTA + '.csv', 'wb')
writer = csv.writer(csvfile, delimiter=';')

# Get questions from one candidate page
questions = []
bs = get_candidate("espoo/ehdokkaat/3891")
for question in bs.findAll('div', { "class" : "question" }):
	question_text = str(question.find('h4').contents[0])
	questions.append(question_text)
writer.writerow(['Ehdokkaan nimi', 'Puolue'] + questions)

# Get the list of candinates
url = "http://www.vaalikone.fi/kunta2017/" + KUNTA + "/puolueet"
f = urllib.urlopen(url)
full_page = f.read()
bs_cand = BeautifulSoup(full_page)
for cand in bs_cand.findAll('td', {"class": "candidates_column_candidate"}):
	id = cand.find('a')['href']

	# Get the candidate page
	bs = get_candidate(id)
	name = bs.find('div', {"class" : "name"})
	if name:
		# The candidate exists. Add name and party
		party = bs.find('div', {"class" : "party"})
		result_row = [str(name.contents[0]), str(party.contents[0])]

		# Loop over divisions with questions
		for question in bs.findAll('div', { "class" : "question" }):
			for answer in question.findAll('li', { "class" : "selected" }):
				for span in answer.findAll('span'):
					data_class = span['data-ng-class']
					result_row.append(int(re.findall(r"[\w']+", data_class)[2]))

		print(result_row)
		writer.writerow(result_row)
