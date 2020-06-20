import requests
import json
from bs4 import BeautifulSoup
import datetime


def get_book_names_from(url):
    resp = requests.get(url)
    result = BeautifulSoup(resp.content, 'html.parser')
    list_of_book_list = result.find_all('ul', class_="nav nav-tabs nav-stacked")   
    book_names = []
    for book_list in list_of_book_list:     
        books = book_list.find_all('a')
        for book in books:
            book_names.append(book.text)

    return book_names



###########################################################
# initialize variables here
book_no = 1
bible = []
start_time = datetime.datetime.now()
mal_book_names = get_book_names_from("http://www.wordproject.org/bibles/ml/")
eng_book_names = get_book_names_from("https://www.wordproject.org/bibles/kj/")

###########################################################
# start execution here

while(True):
    book_res = requests.get("http://www.wordproject.org/bibles/ml/{:02d}/1.htm".format(book_no))
    if(book_res.status_code != 200):
        print("Invalid Book")
        break
    # elif(book_no == 2):
        # break

    chapter_list = []
    chapter_no = 1
    
    while(True):
        chapter_res = requests.get("http://www.wordproject.org/bibles/ml/{:02d}/{}.htm".format(book_no, chapter_no))
        if(chapter_res.status_code != 200):
            print("Invalid Chapter")            
            break
        # elif(chapter_no == 2):
            # break

        print("http://www.wordproject.org/bibles/ml/{:02d}/{}.htm".format(book_no, chapter_no))
        chapter_soup = BeautifulSoup(chapter_res.content, 'html.parser')
        chapter_body = chapter_soup.find(id="textBody")        
        verses = chapter_body.find('p').text
        verse_list = verses.split('\n')
        new_verse_list = []   
        for verse in verse_list[1:]:
            verse = verse.split(' ')[1:]
            verse = ' '.join(verse)
            if verse.strip() != "":
                new_verse_list.append(verse.strip())
        chapter_list.append(new_verse_list)
        chapter_no = chapter_no + 1

    book = {'mal_name':mal_book_names[book_no-1], 'eng_name':eng_book_names[book_no-1], 'chapters':chapter_list}
    bible.append(book)
    book_no = book_no+1

with open('data.json', 'w', encoding='utf-8') as file:
    json.dump(bible, file, ensure_ascii=False) #indent=4)

print("Total time taken = " + str(datetime.datetime.now() - start_time))