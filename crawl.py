import praw
import json
import sys
import queue

# Helper Variables
postLimit = 5
topPostTime = "year"

# Reddit developer account: 
ID          = "7UI5BZd_IpRM-Opi3WtSOA"
SECRET      = "mw-ViF2wBo6gEwE_PuB4kQHermrjjg"
AGENT       = "cs172"

# Json setup and data containers:
items = []
users = queue.Queue()
subReddit = queue.Queue()
fields = ('permalink', 'id', 'title', 'url','selftext','score', 'upvote_ratio', 'created_utc', 'num_comments')
#           link                      image  text-body  upvotes                  time created

# Reddit read only mode
reddit = praw.Reddit(
    client_id=ID,
    client_secret=SECRET,
    user_agent=AGENT
)

# Seed
seed = "Helldivers"

def crawlSubreddit(subreddit):
    postCount = 1
    for post in reddit.subreddit(subreddit).top(time_filter = topPostTime, limit = postLimit):
        # grab dictionary with attributes of object using vars()
        dict = vars(post)
        print(f"Parsing: ({post.title})[{postCount}:{postLimit}]")

        # grab specific attributes specified in fields, written above, for current post. 
        sub_dict = {field:dict[field] for field in fields}

        # Prepare crawler for diving into users and add users to json
        sub_dict['author'] = post.name
        users.put(post.author)

        # grab all comments for the current post
        comments = []
        post.comments.replace_more(limit=None)

        # Helper counter for comments
        commentCount = 1
        for comment in post.comments.list():
            print("\r", end='')
            print(f"Downloading Comments: {commentCount}", end='\r', flush = True)            comments.append(comment.body)
            commentCount += 1
        print("\n")
        sub_dict['comments'] = comments

        # Create a new container that just has the field we want
        items.append(sub_dict)
        postCount += 1

def crawlRedditor(redditor):
    # Grab new subreddits visited here as well as item essentials
    for post in reddit.redditor(redditor).submissions.top(timer_filter = topPostTime, limit = postLimit):
        # grab dictionary with attributes of object using vars()
        dict = vars(post)
        print(f"Parsing: ({post.title})[{postCount}:{postLimit}]\n")

        # grab specific attributes specified in fields, written above, for current post. 
        sub_dict = {field:dict[field] for field in fields}

        # Feed crawler users and add users to json
        sub_dict['author'] = post.name
        users.put(post.author)

        # grab all comments for the current post
        comments = []
        post.comments.replace_more(limit=None)

        # Helper counter for comments
        commentCount = 1
        for comment in post.comments.list():
            print("\r", end='')
            print(f"Downloading Comments: {commentCount}", end='\r', flush = True)       
            comments.append(comment.body)
            commentCount += 1
        sub_dict['comments'] = comments

        # Add post to items, which will be stored later in json
        items.append(sub_dict)

        # Feed crawler new subreddits
        subReddit.put(post.subreddit.name)
        postCount += 1

# print(sys.getsizeof(json_str))
def main():
    json_str = ""
    # Seed our crawl
    subReddit.put(seed)
    crawlSubreddit(subReddit.get())

    # While sys.getsizeof(json_str) < 100100000, add the extra 1000000 so that we go above 100mb
    # continue scraping through users and subreddits the user has posted in
    # while(sys.getsizeof(json_str) < 100100000):
    #     crawlSubreddit(subReddit.get())

    #     json_str = json.dumps(items, sort_keys=True, indent=4)

    # #write json_str to crawl.json
    # with open('crawl.json', 'w') as f:
    #     json.dump(items, f)

main()