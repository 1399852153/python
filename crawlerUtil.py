import urllib.request
import re
import urllib.parse as urlparse
import urllib.robotparser

robotFileParser = urllib.robotparser.RobotFileParser()


def download(url, user_agent, proxy=None, retry_count=2):
    # 下载url对应的网页

    print('download: ' + url + ' retryCount=' + str(retry_count))

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


def linked_download(seed_url, linked_rex=None, user_agent='wswp', proxy=None):
    # 按照正则匹配规则,下载关联的所有网页

    print("linked_download start")

    searched_urls = set()
    url_list = [seed_url]

    opener = urllib.request.build_opener(urllib.request.ProxyHandler(proxy))
    opener.addheaders = [
        ('User-agent', user_agent)
    ]

    rp = get_robots(seed_url)

    urllib.request.install_opener(opener)

    while url_list:
        url = url_list.pop()

        # robot.txt中当前代理是否允许爬取
        if rp.can_fetch(user_agent, url):

            html = download(url, user_agent, proxy)
            print('html: /n' + url)

            linked_urls = get_linked_url(html.decode('utf-8'))

            # 将符合规则的a标签加入url列表,继续遍历
            for url_item in linked_urls:
                # 是否符合规则
                if re.search(linked_rex, url_item):
                    # 是否还未被爬取过
                    if url_item not in searched_urls:
                        # 将已经爬取过的网页保存起来
                        searched_urls.add(url_item)

                        url_item = urlparse.urljoin(seed_url,url_item)
                        url_list.append(url_item)
        else:
            print('Blocked by robots.txt:' + url)


def get_robots(url):
    """Initialize robots parser for this domain
    """
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(urlparse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp
