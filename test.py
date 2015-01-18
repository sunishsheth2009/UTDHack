from bs4 import BeautifulSoup
import urllib2
import unicodedata


url="http://www.theguardian.com/us"
page=urllib2.urlopen(url)
soup = BeautifulSoup(page.read())
#print type(soup)
links1 = [] 
links2 = []

link1 = []
link2 = []

headlines1 = []
headlines2 = []
desc1 = []
desc2 = []

categories = []
cat1 = []
cat2 = []

day = soup.find('span',{'class':'fc-today__dayofweek js-dayofweek'})
day_of_month = soup.find('span',{'class':'fc-today__dayofmonth js-dayofmonth'})
month = soup.find('span',{'class':'fc-today__month'})
year = soup.find('span',{'class':'fc-today__year'})
add = soup.findAll('div',{'class':'fc-container__header__title'})
for i in range(0, len(add)):
	categories.append(add[i].findChildren()[0].text)

print day.text,day_of_month.text,month.text,year.text

entireText = soup.findAll('div',{'class':'fc-container__inner'})

j = -1 

for text in entireText:
	if(j < len(categories)-1):
		j = j + 1
	else:
		break
	print j
	new1 = text.findAll('h1',{'class':'fc-item__title'})
	new2 = text.findAll('h2',{'class':'fc-item__title'})
	link1 = []
	link2 = []

	for i in range(0, len(new1)):
		link1.append(new1[i].contents[0]['href'])
		#print new1[i].contents[0]['href']
		headlines1.append(unicodedata.normalize('NFKD', new1[i].contents[0].text).encode('ascii','ignore'))
		#print unicodedata.normalize('NFKD', new1[i].contents[0].text).encode('ascii','ignore')


	for i in range(0, len(new2)):
		link2.append(new2[i].contents[0]['href'])
		#print new2[i].contents[0]['href']
		headlines2.append(unicodedata.normalize('NFKD', new2[i].contents[0].text).encode('ascii','ignore'))
		#print unicodedata.normalize('NFKD', new2[i].contents[0].text).encode('ascii','ignore')

	for i in range(0, len(link2)):
		links2.append(link2[i])
		cat2.append(unicodedata.normalize('NFKD', categories[j].strip('\n')).encode('ascii','ignore'))
		url = link2[i]
		page = urllib2.urlopen(url)
		soup = BeautifulSoup(page.read())
		description2=soup.find('meta',{'itemprop':'description'})
		try:
			desc2.append(unicodedata.normalize('NFKD', description2['content']).encode('ascii','ignore'))
			#print unicodedata.normalize('NFKD', description2['content']).encode('ascii','ignore')
		except:
			desc2.append("No Description...")
			#print "No Description..."

	for i in range(0, len(link1)):
		link1.append(link1[i])
		cat1.append(unicodedata.normalize('NFKD', categories[j].strip('\n')).encode('ascii','ignore'))
		url = link1[i]
		page = urllib2.urlopen(url)
		soup = BeautifulSoup(page.read())
		description1=soup.find('meta',{'itemprop':'description'})
		try:
			desc1.append(unicodedata.normalize('NFKD', description1['content']).encode('ascii','ignore'))
			#print unicodedata.normalize('NFKD', description1['content']).encode('ascii','ignore')
		except:
			desc1.append("No Description...")
			#print "No Description..."


for i in range(0, len(links1)):
	print "Categories --> " + cat1[i]
	print "HeadLines --> "+headlines1[i]
	print "Description --> "+desc1[i]
	print "Link --> "+links1[i]

for i in range(0, len(links2)):
	print "Categories --> " + cat2[i]
	print "HeadLines --> "+headlines2[i]
	print "Description --> "+desc2[i]
	print "Link --> "+links2[i]

