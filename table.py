import lxml.html
import urllib2
import urlparse
import sys

def textIsUrl(text):
	parts = urlparse.urlsplit(text)
	return (parts.scheme and parts.netloc)

def textIsIp(text):
	pieces = text.split('.')
	if(len(pieces) != 4):
		return False
	for p in pieces:
		if(not p.isdigit() or not 0 <= int(p) <= 255):
			return False
	return True

def getStatusArrayFromUrl(url):
	html = lxml.html.fromstring(urllib2.urlopen(url).read())
	statusarray = []
	rows = html.cssselect("tr")
	for row in rows:
		statusarray.append({'url':False, 'ip':False})
		for td in row.cssselect("td"):
			text = td.text_content().strip().encode('ascii','ignore')
			if(textIsUrl(text)):
				statusarray[-1]['url'] = True
			elif(textIsIp(text)):
				statusarray[-1]['ip'] = True
	return statusarray
statuses = getStatusArrayFromUrl(sys.argv[1])
if(statuses == []):
	print('No tables found in the url') 
for i in xrange(len(statuses)):
	print 'row', i , '\t=>\turl:', statuses[i]['url'], '\tip:', statuses[i]['ip']