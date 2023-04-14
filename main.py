import requests
import selectorlib
import time
from emailing import send_email
import sqlite3

URL = 'https://programmer100.pythonanywhere.com/tours/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
CONNECTION = sqlite3.connect('data.db')


def scrape(url):
    """Scrape the page Source from the url"""
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file('extract.yaml')
    value = extractor.extract(source)['tours']
    return value


def store(extracted):
    # with open('data.txt', 'a') as file:
    #     file.write(extracted + '\n')
    cursor = CONNECTION.cursor()
    band, city, date = extracted.split(',')
    cursor.execute('Insert INTO events values(?,?,?)', (band, city, date))
    CONNECTION.commit()
    cursor.close()


def read(extracted):
    # with open('data.txt', 'r') as file:
    #     return file.read()
    cursor = CONNECTION.cursor()
    band, city, date = extracted.split(',')
    cursor.execute('SELECT * FROM events WHERE band=? and city=? and date=?', (band, city, date))
    row = cursor.fetchall()
    cursor.close()
    return row


if __name__ == '__main__':
    while True:
        source = scrape(URL)
        extracted = extract(source)
        print(extracted)
        if extracted != 'No upcoming tours':
            row = read(extracted)
            if not row:
                store(extracted)
                send_email(extracted)
        time.sleep(2)
