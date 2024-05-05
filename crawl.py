import praw
import json
import sys
import queue
import time

# Helper Variables
postLimit = 5
commentThreshold = 2
commentLimit = 5
sleepTime = 2
numPostsPerSleep = 5
targetFileSize = 100100000
topPostTime = "year"

# Reddit developer account: 
ID          = "7UI5BZd_IpRM-Opi3WtSOA"
SECRET      = "mw-ViF2wBo6gEwE_PuB4kQHermrjjg"
AGENT       = "crimp go"

# Json setup and data containers:
items = []
crawledUsers = set()
crawledPosts = set()
crawledSubreddit = set({"AskComputerScience", "funny", "memes", "AskReddit", "sports", "soccer", "baseball", "science", 
                        "askscience", "explainlikeimfive", "Food", "Futurology", "NBA", "Technology", "vidoes", "StardewValley", "history", 
                        "AskHistorians", "WritingPrompts", "leagueoflegends", "news", "worldnews", "books", "gaming", "dataisbeautiful", 
                        "MachineLearning", "UCDavis", "UCI", "stanford", "USC"})
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
    if(subreddit in crawledSubreddit):
        print("Dupe subreddit: ")
        return
    
    print(f"-----------------------------------------------\nCrawling {subreddit}\n")
    postCount = 1
    for post in reddit.subreddit(subreddit).top(time_filter = topPostTime, limit = postLimit):
        # try to avoid error 429
        if(postCount % numPostsPerSleep == 0):
            time.sleep(sleepTime)

        # ignore posts we already crawled
        if(post.title in crawledPosts or post is None):
            print("Dupe post or none existent: ")
            postCount += 1
            continue

        if(postCount > postLimit):
            print(f"Skipping {subreddit}, reached search limit.\n")
            return

        # Add post to dupe check
        crawledPosts.add(post.title)

        # grab dictionary with attributes of object using vars()
        dict = vars(post)
        print(f"Parsing: ({post.title})[{postCount}:{postLimit}]")

        # grab specific attributes specified in fields, written above, for current post. 
        sub_dict = {field:dict[field] for field in fields}

        # Feed crawler users, add users to json, add user to dupe check
        if(post.author is not None):
            if(post.author.name not in crawledUsers):
                sub_dict['author'] = post.author.name
                users.put(post.author.name)

        # grab all comments for the current post
        comments = []
        post.comments.replace_more(limit=commentLimit, threshold=commentThreshold)

        # Helper counter for comments
        commentCount = 1
        for comment in post.comments.list():
            print("\r", end='')
            print(f"Downloading Comments: {commentCount}", end='', flush=True)
            sys.stdout.flush()          
            comments.append(comment.body)
            commentCount += 1
        print("\n")
        sub_dict['comments'] = comments

        # Create a new container that just has the field we want
        items.append(sub_dict)
        postCount += 1

    # add subreddit to crawled subreddits
    crawledSubreddit.add(subreddit)

def crawlRedditor(redditor):
    if(redditor in crawledUsers):
        print("Dupe redditor: ")
        return
    
    postCount = 1
    print(f"-----------------------------------------------\nCrawling {redditor}\n")
    # Grab new subreddits visited here as well as item essentials
    for post in reddit.redditor(redditor).submissions.top(limit = postLimit):
        # try to avoid error 429
        if(postCount % numPostsPerSleep == 0):
            time.sleep(sleepTime)
        print("Working1")
        # ignore posts we already crawled
        if(post.title in crawledPosts or post is None):
            print("Dupe post or none existent: ")
            postCount += 1
            continue

        if(postCount > postLimit):
            print(f"Skipping {redditor}, reached search limit.\n")
            return
        print("Working2")
        # Add post to dupe check
        crawledPosts.add(post.title)

        # grab dictionary with attributes of object using vars()
        dict = vars(post)
        print(f"Parsing: ({post.title})[{postCount}:{postLimit}]\n")

        # grab specific attributes specified in fields, written above, for current post. 
        sub_dict = {field:dict[field] for field in fields}

        # Feed crawler subreddits, 
        if(post.subreddit.name not in crawledSubreddit):
            subReddit.put(post.subreddit.name)

        # grab all comments for the current post
        comments = []
        post.comments.replace_more(limit=commentLimit, threshold=commentThreshold)

        # Helper counter for comments
        commentCount = 1
        for comment in post.comments.list():
            print("\r", end='')
            print(f"Downloading Comments: {commentCount}", end='', flush = True)     
            sys.stdout.flush()  
            comments.append(comment.body)
            commentCount += 1
        sub_dict['comments'] = comments

        # Add post to items, which will be stored later in json
        items.append(sub_dict)
        postCount += 1

    # add redditor to crawled redditors
    crawledUsers.add(redditor)

# print(sys.getsizeof(json_str))
def main():
    json_str = ""
    # Seed our crawl
    subReddit.put(seed)

    # While sys.getsizeof(json_str) < 100100000, add the extra 1000000 so that we go above 100mb
    # continue scraping through users and subreddits the user has posted in
    while((sys.getsizeof(json_str) < targetFileSize)):
        if(subReddit.empty() and users.empty()):
            print("------------------------------------------------------------------------\nCould not finish, unable to find unique users and subreddits\n")
            break
        crawlSubreddit(subReddit.get())
        crawlRedditor(users.get())

        json_str = json.dumps(items, sort_keys=True, indent=4)

    #write json_str to crawl.json
    with open('crawl.json', 'w') as f:
        json.dump(items, f)
    
    # Output Subreddits for double checking dupes
    print(crawledSubreddit)


main()