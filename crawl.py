import praw
# import requests
# from bs4 import BeautifulSoup
# seed = "https://en.wikipedia.org/wiki/Randomness"

# page = requests.get(seed)
# soup = BeautifulSoup(page.content, "html.parser")

# for link in soup.find_all('a'):
#     # do whatever with links here
#     print("hi")

ID          = "7UI5BZd_IpRM-Opi3WtSOA"
SECRET      = "mw-ViF2wBo6gEwE_PuB4kQHermrjjg"
AGENT       = "cs172"

reddit = praw.Reddit(
    client_id=ID,
    client_secret=SECRET,
    user_agent=AGENT
)

