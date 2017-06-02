import urllib
url = 'http://export.arxiv.org/api/query?search_query=all:a + OR + all:t + OR + all:f&start=0&max_results=1'
data = urllib.urlopen(url).read()
print data