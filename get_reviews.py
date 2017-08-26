# Script to get all customer reviews about The Roger hotel in NYC from TripAdvisor

# imports
import bs4
import re
#import selenium
import numpy as np
import matplotlib.pyplot as plt
import json
import nltk
nltk.download('stopwords')

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from collections import Counter
#from selenium import webdriver
from nltk.corpus import stopwords


base_url = 'https://www.tripadvisor.com/Hotel_Review-g60763-d80110-Reviews-'
end_url = 'The_Roger-New_York_City_New_York.html'
index = 0
pagination = ''

#my_url = 'https://www.tripadvisor.com/Hotel_Review-g60763-d80110-Reviews-The_Roger-New_York_City_New_York.html'
nav_next_enabled = True

'''
browser = webdriver.Chrome()
browser.get(my_url)  
next_btn = browser.find_element_by_xpath("//span[.='Next']")
next_btn.click()
html_source = browser.page_source  
browser.quit()
'''

# Grab all of the review divs from each page
review_ps = []
while nav_next_enabled:
	review_divs = []

	# Build the url that we're using to grab the html content
	if index == 0:
		my_url = base_url + end_url
	else:
		my_url = base_url + 'or' + str(index) + '-' + end_url

	# opening connection and grabbing page
	uClient = uReq(my_url)
	page_html = uClient.read()

	# close client
	uClient.close()
	
	# html parsing
	page_soup = soup(page_html, "html.parser")
	
	review_divs = page_soup.findAll("div", { "class" : "review" })

	# Specifically get the review contents
	for review_content in review_divs:
		review_ps.append(review_content.p)

	# Check to see if you're on the last reviews page (the Next button will be disabled)
	if page_soup.find("span", { "class": "nav next disabled" }) or index == 10:
		nav_next_enabled = False
	else:
		# Each page has 5 reviews, so increment to the next 5
		print('hit next, reviews length: ' + str(len(review_ps)))
		index += 5

# Get each paragraph from the reviews
print('getting each paragraph from reviews...')
paragraphs = []
for p in review_ps:
	contents = []
	contents = p.contents
	if len(contents) == 2:
		paragraphs.append(contents[0])

words = []
for p in paragraphs:
	words += p.split()

# Clean up words by removing special characters
print('removing special characters from words...')
scrubbed_words = []
for word in words:
	new_word = re.sub('[$!.?()-]', '', word)
	if len(new_word) > 1:
		scrubbed_words.append(new_word)

# Removing stopwords and undescriptive words
undescriptive_words = [
	'room',
	'rooms',
	'hotel',
	'roger',
	'stayed',
	'would',
	'place',
	'us',
	'also',
	'really',
	'made',
	'next',
	'could',
	'desk',
	'get'
]
print('removing stop words...')
filtered_words = [word for word in scrubbed_words if word.lower() not in stopwords.words('english') and word.lower() not in undescriptive_words]

# Count occurrences of each word
print('counting frequency of each word...')
counts = Counter(filtered_words)

top_10_words = counts.most_common(20)

# Now just get the top 10 words
counts_dict = {}
for key, value in top_10_words:
	counts_dict[key] = value

print(type(counts_dict))
print(counts_dict)
counts_dict = json.dumps(counts_dict)
print(type(counts_dict))
print(counts_dict)
#loaded_counts_dict = json.loads(counts_dict)
#print(loaded_counts_dict)

'''
# Plots the findings
plt.bar(range(len(counts_dict)), counts_dict.values(), align='center')
plt.xticks(range(len(counts_dict)), counts_dict.keys(), rotation=25)
plt.show()
print('created plot...')
'''

