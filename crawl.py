import praw
import json

# Helper Variables
postCount = 1
postLimit = 10

# Reddit developer account: 
ID          = "7UI5BZd_IpRM-Opi3WtSOA"
SECRET      = "mw-ViF2wBo6gEwE_PuB4kQHermrjjg"
AGENT       = "cs172"

# Json setup:
items = []
fields = ('permalink', 'id', 'title', 'url','selftext','score', 'upvote_ratio', 'created_utc', 'num_comments')
#           link                      image  text-body  upvotes                  time created
# import requests
# from bs4 import BeautifulSoup
# seed = "https://en.wikipedia.org/wiki/Randomness"

# page = requests.get(seed)
# soup = BeautifulSoup(page.content, "html.parser")

# for link in soup.find_all('a'):
#     # do whatever with links here
#     print("hi")


# Reddit read only mode
reddit = praw.Reddit(
    client_id=ID,
    client_secret=SECRET,
    user_agent=AGENT
)

for post in reddit.subreddit("Helldivers").new(limit=postLimit):
    # grab dictionary with attributes of object using vars()
    to_dict = vars(post)
    print(f"Parsing: ({post.title})[{postCount}:{postLimit}]")

    # grab specific attributes specified in fields, written above, for current post
    sub_dict = {field:to_dict[field] for field in fields}

    # grab all comments for the current post
    comments = []
    post.comments.replace_more(limit=None)
    # Helper counter for comments
    commentCount = 1
    print("Downloading Comments . . . ")
    for comment in post.comments.list():
        print(commentCount)
        comments.append(comment.body)
        commentCount += 1
    sub_dict['comments'] = comments

    # Create a new container that just has the field we want
    items.append(sub_dict)
    postCount += 1

for item in items:
    print(item)
# Dump into json format and write to crawl.json
# json_str = json.dumps(items)
# with open('crawl.json', 'w') as f:
#     json.dump(items, f)
