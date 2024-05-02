import praw
import json
import sys

# Helper Variables
postCount = 1
postLimit = 10

# Reddit developer account: 
ID          = "7UI5BZd_IpRM-Opi3WtSOA"
SECRET      = "mw-ViF2wBo6gEwE_PuB4kQHermrjjg"
AGENT       = "cs172"

# Json setup and data containers:
items = []
users = []
fields = ('permalink', 'id', 'title', 'url','selftext','score', 'upvote_ratio', 'created_utc', 'num_comments')
#           link                      image  text-body  upvotes                  time created

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

    # grab specific attributes specified in fields, written above, for current post. 
    sub_dict = {field:to_dict[field] for field in fields}

    # Prepare crawler for diving into users and add users to json
    sub_dict['author'] = post.author
    users.append(post.author)

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
print(sys.getsizeof(items))
# for item in items:
#     print(item)
# Dump into json format and write to crawl.json
json_str = json.dumps(items)
with open('crawl.json', 'w') as f:
    json.dump(items, f)
