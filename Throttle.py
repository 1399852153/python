from urllib.parse import urlparse
import datetime
import time


class Throttle:
    """ add a delay between downloads to the same domain"""

    def __init__(self, delay):
        self.delay = delay
        self.domains = {}

    def wait(self, url):
        # 解析出域名
        domain = urlparse(url).netloc

        # 获得上一次访问的时间戳
        last_accessed = self.domains.get(domain)

        # 如果需要延迟访问,而且上一次访问时间存在
        if self.delay > 0 and last_accessed is not None:
            # 需要休眠的时间 = 延迟时间 - 当前时间和最后一次访问时间之差
            sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
            # 如果结果大于零
            if sleep_secs > 0:
                print('need delay: sleep_secs=%s' % sleep_secs)

                # 休眠对应的时间(单位:秒)
                time.sleep(sleep_secs)

        # 设置当前域名 最近一次访问时间
        self.domains[domain] = datetime.datetime.now()
