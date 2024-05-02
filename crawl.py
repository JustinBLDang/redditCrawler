import requests
import praw
from bs4 import BeautifulSoup
seed = "https://en.wikipedia.org/wiki/Randomness"

page = requests.get(seed)
soup = BeautifulSoup(page.content, "html.parser")

for link in soup.find_all('a'):
    # do whatever with links here
    print("hi")