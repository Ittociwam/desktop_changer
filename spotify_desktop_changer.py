import urllib2
import simplejson
import cStringIO

fetcher = urllib2.build_opener()
searchTerm = 'parrot'
searchUrl = "http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + searchTerm + "&start=0"
f = fetcher.open(searchUrl)
deserialized_output = simplejson.load(f)


print(deserialized_output)# ['results'][0]['unescapedUrl']
