import praw
import config
import time
import os
import time
import random
from datetime import datetime

def bot_login():
        print ("Logging in...")
        r = praw.Reddit(username = config.username,
                        password = config.password,
                        client_id = config.client_id,
                        client_secret = config.client_secret,
                        user_agent = "Worms amos yee bot v0.3")
        print("Log in successful!")
        return r

def run_bot(r, replied_comments_id):
        print("Retrieving last 25 comments")
        for comment in r.subreddit('test').comments(limit = 10):
                if (("amos yee" in comment.body or "Amos yee" in comment.body or "Amos Yee" in comment.body) and comment.id not in replied_comments_id and not comment.author == r.user.me() and not "bot" in comment.author.name):
                        print("found text")

                        if (len(get_replied_comments())<2):
                                comment.reply("First mention of Amos Yee!")
                                print("First mention")
                        else:
                                comment.reply(prepare_reply(r))

                        print("Replied to comment " + comment.id + " by " + comment.author.name)
                        replied_comments_id.append(comment.id)
                        with open ("replied_comments.txt", "a") as f:
                                f.write(comment.id + "\n")
                                print("Recorded reply to comment id " + comment.id)

        print ("Sleeping for 10 seconds")
        time.sleep(10)

def prepare_reply(r):
        s = str("🎉 **RESET THE COUNTER!!!** 🎉\n\n" +
        "It has been *" + get_prefix() + "* **" + get_time_since_last_mention(r) + "** since we've had an intellectual discussion about Amos Yee! \n\n" +
        "Last mentioned by " + get_last_mention(r).author.name + " on **" + datetime.utcfromtimestamp(get_last_mention(r).created_utc).strftime('%d %b %y') + "**: " +
        "[" + get_last_mention(r).submission.title + "](" + get_last_mention(r).permalink + ")" + "\n\n" +
        "***\n\n" +
        "[v0.3](" + "https://github.com/Wormsblink/amos_yee_bot" + ") by Worms_sg | PM AmosYee_bot if bot is down")

        return s

def get_replied_comments():
        if not os.path.isfile("replied_comments.txt"):
                replied_comments_id = []
        else:
                with open("replied_comments.txt", "r") as f:
                        replied_comments_id = f.read()
                        replied_comments_id = replied_comments_id.split("\n")

        return replied_comments_id

def get_prefix():
		with open("prefix.txt") as f:
				prefixes = f.read()
				prefixes = prefixes.split("\n")
		return random.choice(prefixes)


def get_last_mention(r):
        return r.comment(get_replied_comments()[-2])

def get_time_since_last_mention(r):
        last_comment_time = int(get_last_mention(r).created_utc)
        current_time = int(time.time())
        time_difference = current_time - last_comment_time
        if (time_difference > 24*3600*2):
                return (str(int(time_difference/24/3600)) + " days")

        elif(time_difference > 3600*2):
                return(str(int(time_difference/3600)) + " hours")
            
        elif(time_difference>60*2):
                return(str(int(time_difference/60)) + " minutes")
        else:
        		return (str(time_difference) + " seconds")

r = bot_login()
while True:
        run_bot(r, get_replied_comments())


