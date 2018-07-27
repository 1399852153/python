import urllib.request
import re
import urllib.parse as urlparse

default_user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/58.0.3029.96 Safari/537.36'


def download(url, user_agent=default_user_agent, retry_count=2):
    # 下载url对应的网页

    print('download: ' + url + 'retryCount=' + str(retry_count))
    try:
        header = {
            'User-Agent': user_agent
        }
        request = urllib.request.Request(url, headers=header)
        html = urllib.request.urlopen(request).read()
        return html
    except urllib.error.HTTPError as e:
        print(e.reason)

        if retry_count > 0:
            if (hasattr(e, "code")) and (500 <= e.code <= 599):
                print('retry download ===== code=' + str(e.code) + " retryCount=" + str(retry_count))
                return download(url, retry_count=retry_count-1)
            else:
                return None
        else:
            return None


def get_linked_url(html):
    # a标签正则
    web_page_rex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)

    return web_page_rex.findall(html)


def linked_download(seed_url, linked_rex):
    # 按照正则匹配规则,下载关联的所有网页

    print("linked_download start")

    url_list = [seed_url]

    while url_list:
        url = url_list.pop()
        html = download(url)

        linked_urls = get_linked_url(html.decode('utf-8'))
        print(linked_urls)

        # 将符合规则的a标签加入url列表,继续遍历
        for url_item in linked_urls:
            if re.match(linked_rex, url_item):
                url_item = urlparse.urljoin(seed_url,url_item)
                url_list.append(url_item)


