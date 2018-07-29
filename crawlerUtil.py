import urllib.request
import re
import urllib.parse as urlparse
import urllib.robotparser
import urllib.error
import Throttle

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


def linked_download(seed_url, linked_rex=None, user_agent='wswp', proxy=None, max_depth=2, delay=3):
    # 按照正则匹配规则,下载关联的所有网页

    print("linked_download start")

    # 设置延迟访问休眠对象
    throttle = Throttle.Throttle(delay)

    # 访问过的url字典缓存
    searched_urls = {}
    # 需要遍历的url列表
    url_list = [seed_url]

    # 设置user-agent和代理
    opener = urllib.request.build_opener(urllib.request.ProxyHandler(proxy))
    opener.addheaders = [
        ('User-agent', user_agent)
    ]
    urllib.request.install_opener(opener)

    # 读取robot.txt
    rp = get_robots(seed_url)

    # 遍历所有的url
    while url_list:
        # 弹出当前第一个url
        url = url_list.pop()

        # robot.txt中当前代理是否允许爬取
        if rp.can_fetch(user_agent, url):
            # 获得当前url访问过的次数(默认为0)
            depth = searched_urls.get(url, 0)

            # 如果url最大访问次数未达到次数
            if depth != max_depth:
                # 判断当前访问是否需要延迟
                throttle.wait(url)

                # 访问url,获得html数据
                html = download(url, user_agent, proxy)

                # 从html中获得所有的a标签链接
                linked_urls = get_linked_url(html.decode('utf-8'))

                # 将符合规则的a标签加入url列表
                for url_item in linked_urls:
                    # 是否符合传入的url规则
                    if re.search(linked_rex, url_item):
                        # 是否还未被爬取过
                        if url_item not in searched_urls:
                            # 将已经爬取过的网页保存起来,并且设置爬取的次数加1
                            searched_urls[url_item] = depth+1

                            # 将url拼接为绝对路径
                            url_item = urlparse.urljoin(seed_url, url_item)
                            # 加入当前url_list
                            url_list.append(url_item)
        else:
            # 被robot.txt 拒绝
            print('Blocked by robots.txt:' + url)


# 解析当前域名下的robot.txt
def get_robots(url):
    """Initialize robots parser for this domain"""

    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(urlparse.urljoin(url, '/robots.txt'))
    rp.read()

    return rp
