import urllib.request



user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'

def download(url,user_agent=user_agent,retryCount=2):
	print('download: ' + url + 'retryCount=' + str(retryCount));
	try:
		header = {
			'User-Agent': user_agent
		}	
	
		request = urllib.request.Request(url,headers=header);
		html = urllib.request.urlopen(request).read();
		return html;
	except urllib.error.HTTPError as e:
		print(e.reason);
		
		if (retryCount > 0):
			if (hasattr(e,"code")) and (500<=e.code and e.code<=599):
				print('retry download ===== code=' + str(e.code) + " retryCount=" + str(retryCount));
				return download(url,retryCount=retryCount-1);
			else:
				return None;
		else:
			return None;
