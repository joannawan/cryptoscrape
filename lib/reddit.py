import links
import source
import json, requests, praw
import time

INCLUDED_PATH_REDDIT = "sources/reddit/include.txt"
LAST_RUN_PATH_REDDIT = "sources/reddit/.lastrun"
CRYPTOS_PATH_REDDIT = "sources/reddit/cryptos.txt"

class Reddit(source.Source):
    subreddits = set()
    instance = praw.Reddit("crypto-scrape")
    srMentions = dict()

    def __init__(self):
        source.Source.__init__(self, INCLUDED_PATH_REDDIT, LAST_RUN_PATH_REDDIT, CRYPTOS_PATH_REDDIT)
        for sr in self.included:
            self.subreddits.add(self.instance.subreddit(sr))
            self.srMentions[sr] = 0

    def collectMentions(self, lim=0):
        for sub in self.subreddits:
            for post in sub.new():
                postTime = int(post.created)

                if (postTime > self.lastRun):
                    post.comments.replace_more(limit = lim)
                    for crypto in self.cryptos:
                        self.srMentions[sub.display_name] += post.selftext.lower().count(crypto)
                        self.srMentions[sub.display_name] += post.url.lower().count(crypto)
                        for comment in post.comments.list():
                            self.srMentions[sub.display_name] += comment.body.lower().count(crypto)

        self.updateRun(time.time())
