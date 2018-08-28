import praw
import time
import os
import requests
import json
import pandas as pd



def authenticate():
    print("Authenticating...")
    reddit = praw.Reddit('reddit bot', user_agent="")

    print("Authenticated as {}".format(reddit.user.me()))
    return reddit


def main():
    reddit = authenticate()

    d = get_saved_rankings()

    comments_replied_to = get_saved_comments()
    print(comments_replied_to)
    while True:
            run_bot(reddit, comments_replied_to, d)


def run_bot(reddit, comments_replied_to,d):
    print("Searching comments...")    
    searchWord="something"
    for comment in reddit.subreddit('all').comments(limit=None):
        if searchWord in comment.body.lower() and comment.id not in comments_replied_to:
            print(
                "Found " +
                searchWord + " " +
                comment.id + "made by {}".format(comment.author))
            print(comment.body)
            print("~~~~~~~~~~~~~~~~~~\n")
           

            with open ("comments_content.txt","a",encoding='utf-8') as g:
                g.write("{}\n".format(comment.author))
                g.write("{}\n".format(comment.body))  
                g.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")  

            name = comment.author
            if not str(name) in d:
                points = 1
            else:
                points = d[str(name)] + 1
            d[str(name)] = points

            with open ("ranking.txt","w", encoding='utf-8') as h:
                h.write(json.dumps(d))

            comments_replied_to.append(comment.id)

            with open("comments_replied_to.txt", "a") as f:
               f.write(comment.id + "\n")

    df = pd.DataFrame.from_dict(d, orient='index')
    df.reset_index(level=0, inplace=True)

    with open ("ranking_table.txt","w") as j:
        j.write(str(df))

    print(comments_replied_to)
    print("Sleeping for 5 seconds...")
    # sleep for 5 seconds...
    time.sleep(5)



def get_saved_rankings():
    if not os.path.isfile("ranking.txt"):
        d={}
    else:
        with open("ranking.txt","r", encoding='utf-8') as f:
            d = json.loads(f.read())
    return d

def get_saved_comments():
    if not os.path.isfile("comments_replied_to.txt"):
        comments_replied_to = []
    else:
        with open("comments_replied_to.txt", "r") as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
            comments_replied_to = list(filter(None, comments_replied_to))

    return comments_replied_to


if __name__ == "__main__":
    main()
