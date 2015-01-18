from bs4 import BeautifulSoup
import urllib2
import unicodedata
from flask import Flask, request
from flask.ext import restful
from flask.ext.restful import Resource, Api
import json

app = Flask(__name__)
api = restful.Api(app)

class SearchResults(Resource):
    def get(self,query):
        url="https://www.google.com/search?q="+query+"+site:www.theguardian.com"
        print url
        request = urllib2.Request(url)
        request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0')
        opener = urllib2.build_opener()
        page=opener.open(request)
        soup=BeautifulSoup(page.read())

        links = []
        titles = []
        descriptions = []
        timestamps = []

        results = soup.findAll('li',{'class':'g'})
        print len(results)
        for result in results:
            soup1 = BeautifulSoup(str(result))
            statement = ""

            try:
                titles.append(unicodedata.normalize('NFKD', soup1.findAll('h3',{'class':'r'})[0].get_text()).encode('ascii','ignore'))
            except:
                titles.append('')
            try:
                links.append(unicodedata.normalize('NFKD', soup1.find('h3',{'class':'r'}).findChildren()[0]['href']).encode('ascii','ignore'))
            except:
                links.append('')
            statement = soup1.find('span',{'class','st'})
            soup2 = BeautifulSoup(str(statement))
            try:
                timestamps.append(unicodedata.normalize('NFKD', soup2.find('span',{'class':'f'}).text).encode('ascii','ignore'))
            except:
                timestamps.append('')
            try:
                descriptions.append(unicodedata.normalize('NFKD', statement.get_text()).encode('ascii','ignore'))
            except:
                descriptions.append('')

        value=[]
        print len(titles)
        for i in range(0,len(titles)):
            value.append({"title":titles[i],"description":descriptions[i],"url":links[i],"timestamp":timestamps[i]})

        return json.dumps(value)

class GetCategories(Resource):
        def get(self):
            url="http://www.theguardian.com/us"
            page=urllib2.urlopen(url)
            soup = BeautifulSoup(page.read())
            categories = []
            add = soup.findAll('div',{'class':'fc-container__header__title'})
            for i in range(0, len(add)):
                    categories.append({'category':''+add[i].findChildren()[0].text.strip()})
            returnvalue= json.dumps({'test':'test','list':categories})
            print type(returnvalue)
            return returnvalue


class GetNews2(Resource):
        def get(self, category):
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

            time1=[]
            time2=[]

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

            soup2 = BeautifulSoup(str(entireText))

            entireText = soup2.findAll('div',{'data-title':category})


            for text in entireText:
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
                            cat2.append(unicodedata.normalize('NFKD', category).encode('ascii','ignore'))
                            url = link2[i]
                            page = urllib2.urlopen(url)
                            soup = BeautifulSoup(page.read())
                            description2=soup.find('meta',{'itemprop':'description'})
                            timestamp=soup.find('time',{'itemprop':'datePublished'})
                            try:
                                    time2.append(unicodedata.normalize('NFKD', timestamp.text.strip("\n")).encode('ascii','ignore'))
                                    desc2.append(unicodedata.normalize('NFKD', description2['content']).encode('ascii','ignore'))
                                    #print unicodedata.normalize('NFKD', description2['content']).encode('ascii','ignore')
                            except:
                                    time2.append("No Time Specified")
                                    desc2.append("No Description...")
                                    #print "No Description..."

                    for i in range(0, len(link1)):
                            link1.append(link1[i])
                            cat1.append(unicodedata.normalize('NFKD', category).encode('ascii','ignore'))
                            url = link1[i]
                            page = urllib2.urlopen(url)
                            soup = BeautifulSoup(page.read())
                            description1=soup.find('meta',{'itemprop':'description'})
                            timestamp=soup.find('time',{'itemprop':'datePublished'})
                            try:
                                    time1.append(unicodedata.normalize('NFKD', timestamp.text.strip("\n")).encode('ascii','ignore'))
                                    desc1.append(unicodedata.normalize('NFKD', description1['content']).encode('ascii','ignore'))
                                    #print unicodedata.normalize('NFKD', description1['content']).encode('ascii','ignore')
                            except:
                                    time1.append("No Time Specified")
                                    desc1.append("No Description...")
                                    #print "No Description..."

            value=[]
            cnt=0
            for i in range(0, len(links1)):
                    #if cat1[i]==category:
                    value.append({"title":headlines1[i],"description":desc1[i],"url":links1[i],"time":time1[i]})
            for i in range(0, len(links2)):
                    #if cat2[i]==category:
                    value.append({"title":headlines2[i],"description":desc2[i],"url":links2[i],"time":time2[i]})

            return json.dumps(value)

class GetNews(Resource):
        def get(self, category):
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

            time1=[]
            time2=[]

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

            soup2 = BeautifulSoup(str(entireText))

            entireText = soup2.findAll('div',{'data-title':category})

            for text in entireText:
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
                            cat2.append(unicodedata.normalize('NFKD', category).encode('ascii','ignore'))
                            url = link2[i]
                            page = urllib2.urlopen(url)
                            soup = BeautifulSoup(page.read())
                            description2=soup.find('meta',{'itemprop':'description'})
                            timestamp=soup.find('time',{'itemprop':'datePublished'})
                            try:
                                    time2.append(unicodedata.normalize('NFKD', timestamp.text.strip("\n")).encode('ascii','ignore'))
                                    desc2.append(unicodedata.normalize('NFKD', description2['content']).encode('ascii','ignore'))
                                    #print unicodedata.normalize('NFKD', description2['content']).encode('ascii','ignore')
                            except:
                                    time2.append("No Time Specified")
                                    desc2.append("No Description...")
                                    #print "No Description..."

                    for i in range(0, len(link1)):
                            link1.append(link1[i])
                            cat1.append(unicodedata.normalize('NFKD', category).encode('ascii','ignore'))
                            url = link1[i]
                            page = urllib2.urlopen(url)
                            soup = BeautifulSoup(page.read())
                            description1=soup.find('meta',{'itemprop':'description'})
                            timestamp=soup.find('time',{'itemprop':'datePublished'})
                            try:
                                    time1.append(unicodedata.normalize('NFKD', timestamp.text.strip("\n")).encode('ascii','ignore'))
                                    desc1.append(unicodedata.normalize('NFKD', description1['content']).encode('ascii','ignore'))
                                    #print unicodedata.normalize('NFKD', description1['content']).encode('ascii','ignore')
                            except:
                                    time1.append("No Time Specified")
                                    desc1.append("No Description...")
                                    #print "No Description..."

            value=[]
            cnt=0
            for i in range(0, len(links1)):
                    if cat1[i]==category:
                        value.append({"title":headlines1[i],"description":desc1[i],"url":links1[i],"time":time1[i]})
            for i in range(0, len(links2)):
                    if cat2[i]==category:
                        value.append({"title":headlines2[i],"description":desc2[i],"url":links2[i],"time":time2[i]})

            return json.dumps(value)


api.add_resource(GetNews2,'/category/<string:category>')
api.add_resource(SearchResults,'/search/<string:query>')
api.add_resource(GetCategories, '/getcategories')

if __name__ == '__main__':
        app.run(debug=True,threaded=True)
