import bs4 as bs
import urllib.request
from selenium import webdriver
import time
from random import randint
import csv
driver = webdriver.Chrome()
original_link ='http://www.indulekha.com/mathrubhumi?limit=100'
stack = [original_link]
writing_file = open('indulekha_bookstore_original.csv','a',encoding="utf-8",newline='')
kerala_test = csv.writer(writing_file,delimiter=',')
count = 0
page = 1
while stack:
    time.sleep(randint(1, 5))
    driver.get(stack.pop())

    source = driver.execute_script("return document.body.innerHTML")
    # first = urllib.request.urlopen('https://keralabookstore.com/language-to-english.do').read()
    # source = urllib.request.urlopen('https://keralabookstore.com/show-books-of-publisher.do?publisher=Mathrubhumi+Books').read()
    soup = bs.BeautifulSoup(source,'lxml')
    all_books = []
    for url in soup.find_all('div',{'class':'image'}):
        url_children = list(url.children)
        all_books.append(url_children[0].get("href"))

    print(all_books)
    for book in all_books:
        time.sleep(randint(1,5))
        driver.get(book)
        count += 1
        source = driver.execute_script("return document.body.innerHTML")
        new_soup = bs.BeautifulSoup(source,'lxml')
        title = ""
        author = ""
        pages = ""
        price = ""
        if new_soup.find('h1'):
            title = new_soup.find('h1').get_text()
        if new_soup.find('div',{ "id" : "authors"}):
            author = new_soup.find('div',{ "id" : "authors"}).get_text()
            author = author.strip().replace("By:",'').lstrip()
        for para in new_soup.find_all('p'):
            if 'Pages' in para.get_text():
                the_text = para.get_text()
                print(count,the_text)
                start_pos = the_text.index('Pages')
                pages = ""
                first_occured = False
                while the_text[start_pos] != "\n":
                    if the_text[start_pos].isdigit():
                        pages += the_text[start_pos]
                        first_occured = True
                    elif first_occured:
                        break
                    start_pos += 1

        if new_soup.find_all('h2'):
            prices = new_soup.find_all('h2')
            for new_price in prices:
                if 'Rs' in new_price.get_text():
                    price = new_price.get_text().replace('Rs','')
        final_text = [title,author,pages,price]
        print(count,final_text)
        kerala_test.writerow(final_text)
    page += 1
    stack.append(original_link + "&page=" + str(page))
    if page==12:
        break

writing_file.close()