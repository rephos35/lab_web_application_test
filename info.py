# Pipfile
# isbntools = "*"
# isbnid = "*"

# from isbntools.app import isbn_from_words, clean, meta, registry
# from isbn.isbn import ISBN
from isbntools.app import clean

import json

from bs4 import BeautifulSoup
import requests
from time import sleep
from random import randint

import cv2
from pyzbar import pyzbar

from fake_useragent import UserAgent

crawler_book_url = "https://isbn.ncl.edu.tw/NEW_ISBNNet/main_DisplayResults.php?&Pact=DisplayAll"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "cookiesession1=678B28725C6B7608B71039EF33AA0795; PHPSESSID=hc72cuaru2s8brumt1jd8sdl67; __tad=1674394089.4503445; _ga=GA1.3.859905126.1674807491; _gid=GA1.3.1343276462.1675316261; _gat=1", #  __tad=1674248574.1688656 _git change ???
    # _ga=GA1.3.859905126.1674807491; _gid=GA1.3.1237244282.1674807491; _gat=1; 
    "Host": "isbn.ncl.edu.tw",
    "Referer": crawler_book_url, #"https://isbn.ncl.edu.tw/NEW_ISBNNet/H30_SearchBooks.php?&Pact=DisplayAll"
    "sec-ch-ua": "'Not_A Brand';v='99', 'Google Chrome';v='109', 'Chromium';v='109'",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": 'same-origin',
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    
}

def get_isbninfo(book_name, book_isbn):
    # isbn 
    book_isbn = clean(book_isbn)
    if book_name == "" and book_isbn == "":
        return []
    print("name: ",book_name, " isbn: ",book_isbn) 
    search_books = crawler(book_name, book_isbn)
    return search_books


def get_isbninfo_from_image(barcode_file):
    barcode_file.save(dst="./static/image/barcode.jpg")
    barcode_image = cv2.imread("./static/image/barcode.jpg")
    gray = cv2.cvtColor(barcode_image, cv2.COLOR_BGR2RGB)
    texts = pyzbar.decode(gray)
    for text in texts:
        book_isbn =text.data.decode("utf-8")
    return book_isbn
    







# def get_isbninfo(book_name, book_isbn):
#     # isbn 
#     book_isbn = clean(book_isbn)
#     if book_name == "" and book_isbn == "":
#         return None

#     print("name: ",book_name, " isbn: ",book_isbn) ###
#     if not ISBN.valid(book_isbn):
#         print("there") ###
#         book_isbn = isbn_from_words(book_name)
#         print(book_isbn)
#     # search
#     dict = meta(book_isbn)
#     print("dict", dict)
    
#     if not dict:
#         search_books = crawler(book_name, book_isbn)

#     isbn_info = json.loads(registry.bibformatters["json"](dict))
#     # {'type': 'book', 'title': '給習慣逃避的你 - 心理諮商師告訴你, 每個逃避行為的背後, 都有需要被關心的理由', 'author': [{'name': ''}], 'year': '2021', 'identifier': [{'type': 'ISBN', 'id': '9789865062088'}], 'publisher': ''}
#     print(isbn_info)
#     return isbn_info


def crawler(book_name, book_isbn):
    # get, post: server

    ## <div> class=title <a> <a href=>
    # sel = soup.select("div.title a")
    # for s in sel:
        # print(s["href"], s.text)
    payload = {
    "FO_SearchField0": "Title",
    "FO_SearchValue0": book_name,
    "FO_SchRe1ation1": "AND",
    "FO_SearchField1": "ISBN",
    "FO_SearchValue1": book_isbn,
    "FO_SchRe1ation2": "AND",
    "FO_SearchField2": "PublisherShortTitle",
    "FO_SearchValue2": "",

    "FB_clicked": "FB_開始查詢",        
    "FB_pageSID": "Simple",
    "FO_Match": "2",
    "FO_資料排序": "PubMonth_Pre DESC",
    "FO_每頁筆數": "10",
    "FO_目前頁數": "1",
    "FB_ListOri":""    
    }
    # random
    headers["User-Agent"] = UserAgent().random
    print(headers["User-Agent"])
    delay = randint(1,5)
    
    # r = requests.Session()
    response_post = requests.post(crawler_book_url, data=payload, headers=headers)
    sleep(delay)
    response_get = requests.get(crawler_book_url, headers=headers)
    soup = BeautifulSoup(response_get.text, "html.parser")

    datas = soup.find_all("tr", limit=5)
    search_books = []
    book_number = 0
    for data in datas[2:]:
        book_number += 1
        isbn = data.find(attrs={"aria-label":"封面圖"}).img["src"].split("/")
        author = data.find(attrs={"aria-label":"作者"}).string.split(";")

        search_book={
            "book_number": book_number,
            "book_name": data.find(attrs={"aria-label":"書名"}).string,
            "book_author": author[0],
            "book_publisher": data.find(attrs={"aria-label":"出版者"}).string,
            "book_isbn": isbn[5]
        }

        search_books.append(search_book)
    return search_books 
    # search_books[0]["book_name"]   

        