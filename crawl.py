# from html.parser import HTMLParser
#
#TODO:
# Figure out how differentiate normal links versus relative links
# Figure out how to differentiate http vs https
# Storing all outter links like pictures, other websites, but only adding
from bs4 import BeautifulSoup
import urllib
import urllib.parse
import urllib.request
from pprint import pprint
starting_url = "http://wiprodigital.com"


class Crawler:

    def __init__(self):
        self.starting_url = starting_url
        self.to_visit = set()
        self.visited = {}
        self.base_netloc = urllib.parse.urlparse(self.starting_url).netloc

        self.to_visit.add(self.starting_url)

    def crawl(self):
        while self.to_visit:
            url=self.to_visit.pop()
            print(url)
            self.visited[url]=[]
            try:
                page = urllib.request.urlopen(url)
                soup = BeautifulSoup(page, 'html.parser')

                for link in soup.find_all('a', href=True):
                    link = link['href']
                    link=urllib.parse.urljoin(starting_url, link)
                    link_netloc=urllib.parse.urlparse(link).netloc
                    # is the page in the same domain?
                    if link_netloc == self.base_netloc and link not in self.visited.keys():
                        self.to_visit.add(link)
                    self.visited[url].append(link)

                # copy static links
                # images
                for link in soup.find_all("img", src=True):
                    link = link['src']
                    link=urllib.parse.urljoin(url, link)
                    self.visited[url].append(link)
                # scripts
                for link in soup.find_all("script", src=True):
                    link = link['src']
                    link = urllib.parse.urljoin(url, link)
                    self.visited[url].append(link)
            except urllib.error.HTTPError as e:
                self.handle_error(e)

    def handle_error(self,e):
        pass


c = Crawler()
c.crawl()
pprint(c.visited)
    # print(to_visit)
    # print(other_links)
    # for l in soup.find_all("img", src=True):
    #     print(l['src'])

    # for l in soup.find_all("script", src=True):
    #     print(l['src'])
