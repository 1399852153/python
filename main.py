import util

html = util.download('http://httpstat.us/501');

if html != None:
	print(html.decode('utf-8'));


