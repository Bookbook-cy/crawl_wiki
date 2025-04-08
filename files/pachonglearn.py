import urllib.request
url = 'http://www.baidu.com'
req = urllib.request.urlopen(url)

print(req.getheaders())
req.title()