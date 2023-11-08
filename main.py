import requests
import os
import re
import urllib.request
from bs4 import BeautifulSoup


def download_file(response, filename=''):
    try:
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    file.write(chunk)
        return 0
    except Exception as ex:
        return 1


def url_constructor(curr):
    return "http://vestnik.spbu.ru" + curr


def main():
    year_list = ['2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006']
    if not os.path.isdir('result'):
        os.mkdir('result')
        os.chdir('result')
    else:
        os.chdir('result')
    curr_url = "http://vestnik.spbu.ru/ENG/s10.html"
    soup = BeautifulSoup(urllib.request.urlopen(curr_url), 'lxml')
    linkList = []
    for tr in soup.findAll('table')[1].findAll('tr'):
        for td in tr.findAll('td'):
            for el in td.findAll('a'):
                el_curr = str(el)
                if el_curr.find(".pdf") != -1:
                    el_curr = (re.findall(r'"(.+?)"', el_curr))[0]
                    el_curr = el_curr.replace("..", "")
                    linkList.append(el_curr)
    print(linkList)
    for el in linkList:
        yearPos = el.find("pdf")
        year = "20" + el[yearPos+3:yearPos+5]
        if not os.path.isdir(year):
            os.mkdir(year)
            os.chdir(year)
        else:
            os.chdir(year)
        response = requests.get(url_constructor(el))
        issuePos = el.find("v")
        issue = el[issuePos+1:issuePos+2]
        filename = "vestnik_spbu10_" + year + "_" + issue + ".pdf"
        download_file(response, filename)
        os.chdir('..')


if __name__ == '__main__':
    main()
