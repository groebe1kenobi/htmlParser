
from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.parse import urljoin, urlparse


class Crawler(object):
    def __init__(self):
        self.visited = set()

    def reset(self):
        self.visited = set()


    def crawl(self, url, depth):
        links = self.analyze(url)
        self.visited.add(url)
        while depth > 1:
            for link in links:
                try:
                    if link not in self.visited:
                        self.visited += self.crawl(link)
                    else:
                        return self.crawl(link)
                except:
                    pass

    def analyze(self, url):
        print("Visiting ", url)
        content = urlopen(url).read().decode()
        collector = Collector(url)
        collector.feed(content)
        urls = collector.getLinks()
        return urls


class Collector(HTMLParser):
    def __init__(self, url):
        HTMLParser.__init__(self)
        self.url = url
        self.urllist = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for t in attrs:
                if t[0] == 'href' and 'mailto' not in t[1]:
                    self.urllist.append(urljoin(self.url, t[1]))

    def getLinks(self):
        return self.urllist
