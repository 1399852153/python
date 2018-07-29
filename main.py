import crawlerUtil

good_user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) ' \
                  'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                  'Chrome/62.0.3202.89 Safari/537.36'

bad_user_agent = 'BadCrawler'



crawlerUtil.linked_download(
    'http://example.webscraping.com',
    '/(index|view)/', good_user_agent, max_depth=1)



