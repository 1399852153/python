import util

html = util.download('http://httpstat.us/501')

if html:
	print(html.decode('utf-8'))


