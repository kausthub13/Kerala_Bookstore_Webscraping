import bs4 as bs
import urllib.request
from selenium import webdriver
import time
from random import randint
import csv
driver = webdriver.Chrome()
driver.get('https://keralabookstore.com/language-to-english.do')
stack = ['https://keralabookstore.com/show-books-of-publisher.do?publisher=Mathrubhumi+Books']
writing_file = open('kerala_bookstore_original.csv','a',encoding="utf-8",newline='')
kerala_test = csv.writer(writing_file,delimiter=',')
count = 0
while stack:
    count += 1
    time.sleep(randint(1, 5))
    driver.get(stack.pop())

    source = driver.execute_script("return document.body.innerHTML")
    # first = urllib.request.urlopen('https://keralabookstore.com/language-to-english.do').read()
    # source = urllib.request.urlopen('https://keralabookstore.com/show-books-of-publisher.do?publisher=Mathrubhumi+Books').read()
    soup = bs.BeautifulSoup(source,'lxml')
    all_books = []
    for url in soup.find_all('a'):
        if '/book/' in url.get('href') and 'https://keralabookstore.com'+  url.get('href') not in all_books:
            all_books.append('https://keralabookstore.com'+ url.get('href'))
        if '/navigate-books.do' in url.get('href') and 'next' in url.get('href'):
            stack.append('https://keralabookstore.com'+ url.get('href'))
    for book in all_books:
        time.sleep(randint(1,5))
        driver.get(book)
        source = driver.execute_script("return document.body.innerHTML")
        new_soup = bs.BeautifulSoup(source,'lxml')
        title = ""
        author = ""
        isbn = ""
        pages = ""
        price = ""
        if new_soup.find('div',{ "class" : "panel-heading"}):
            title = new_soup.find('div',{ "class" : "panel-heading"}).get_text()
        if new_soup.find('span',{ "itemprop" : "name"}):
            author = new_soup.find('span',{ "itemprop" : "name"}).get_text()
        if new_soup.find('span',{ "itemprop" : "isbn"}):
            isbn = new_soup.find('span',{ "itemprop" : "isbn"}).get_text()
        if new_soup.find('span',{ "itemprop" : "numberOfPages"}):
            pages = new_soup.find('span',{ "itemprop" : "numberOfPages"}).get_text()
        if new_soup.find('span',{ "itemprop" : "price"}):
            price = new_soup.find('span',{ "itemprop" : "price"}).get_text()
            price = price.replace('Rs ','')
        final_text = [title,author,isbn,pages,price]
        print(count,final_text)
        kerala_test.writerow(final_text)

writing_file.close()