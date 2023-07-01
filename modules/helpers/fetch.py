import requests
from modules.helpers.sanitize import *
from bs4 import BeautifulSoup

async def get_texts_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    text = ' '.join([p.get_text() for p in paragraphs])
    return text

async def get_html_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('body')
    text = ' '.join([p.get_text() for p in paragraphs])
    return text

async def read_file(path_to_file):
    file = open(path_to_file, "r")
    sanitized_file = sanitize_text(file.read())
    return sanitized_file
