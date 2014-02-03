'''
Created on Jan 28, 2014

@author: Eric
'''
import urllib
import re

def getHTML(url):
    site = urllib.urlopen(url)
    html = site.read()
    site.close()
    return html

if __name__ == '__main__':
    pass

print 'app name:', 
appname = raw_input()


appname = appname.replace(' ', '-').lower()


url = "http://slideme.org/application/" + appname
html = getHTML(url)
ratingExp = "average-rating\">Average: <span>(\d+)"
appRating = int(re.findall(ratingExp, html)[0])

numRatingsExp = "total-votes\">\(<span>(\d+)"
numRatings = int(re.findall(numRatingsExp, html)[0])

numDownloadsExp = "downloads\">(\d+)"
numDownloads = int(re.findall(numDownloadsExp, html)[0])

print appname
print 'Rating: ' + str(appRating)
print 'Num Ratings: ' + str(numRatings)
print 'Num Downloads: ' + str(numDownloads)