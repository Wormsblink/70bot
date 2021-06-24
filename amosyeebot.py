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
                        user_agent = "Worms amos yee bot v0.7")
        print("Log in successful!")
        print(datetime.now().strftime('%d %b %y %H:%M:%S'))
        return r

def run_bot(r, replied_comments_id):
        print("Retrieving last 50 comments")
        for comment in r.subreddit('singapore').comments(limit = 50):
                if (("amos yee" in comment.body or "Amos yee" in comment.body or "Amos Yee" in comment.body or "amosyee" in comment.body) and comment.id not in replied_comments_id and not comment.author == r.user.me() and not "bot" in comment.author.name):
                        print("found matching text")

                        if (len(replied_comments_id)<2):
                                comment.reply("First mention of Amos Yee!")
                                print("First mention")
                        else:
                                #print("Not first mention")
                                text_reply = prepare_reply(r)
                                print("reply prepared")
                                comment.reply(text_reply)

                        print("Replied to comment " + comment.id + " by " + comment.author.name)
                        replied_comments_id.append(comment.id)
                        with open ("replied_comments.txt", "a") as f:
                                f.write(comment.id + "\n")
                                print("Recorded reply to comment id " + comment.id)

        #print ("Sleeping for 10 seconds")
        time.sleep(10)

def prepare_reply(r):
        #print("DEBUG: function prepare_reply")

        #print("trying to retrive last mention")
        time_since_last_mention = get_time_since_last_mention(r)
        #print("time since last mention: " + time_since_last_mention)

        last_mention_author = get_last_mention(r).author.name
        #print("last mention author: " + last_mention_author)

        last_mention_date = datetime.utcfromtimestamp(get_last_mention(r).created_utc).strftime('%d %b %y')
        #print("last mention date: " + last_mention_date)

        last_mention_title = get_last_mention(r).submission.title
        #print("last mention title: " + last_mention_title)

        last_mention_link = get_last_mention(r).permalink
        #print("last mention link: " + last_mention_link)

        #print("attempting to string s")

        s = str("🎉 **RESET THE COUNTER!!!** 🎉\n\n" +
        "It has been *" + get_prefix() + "* **" + time_since_last_mention + "** since we've had an intellectual discussion about Amos Yee! \n\n" +
        "Last mentioned by " + last_mention_author + " on **" + last_mention_date + "**: " +
        "[" + last_mention_title + "](" + last_mention_link + ")" + "\n\n" +
        "***\n\n" +
        "[v0.7](" + "https://github.com/Wormsblink/amos_yee_bot" + ") by Worms_sg and running on Raspberry Pi400 | PM AmosYee_bot if bot is down")

        #print("s concatenated")

        return s

def get_replied_comments():
        #print("DEBUG: function get_replied_comments")
        if not os.path.isfile("replied_comments.txt"):
                replied_comments_id = []
        else:
                with open("replied_comments.txt", "r") as f:
                        replied_comments_id = f.read()
                        replied_comments_id = replied_comments_id.split("\n")

        return replied_comments_id

def get_prefix():
		print("DEBUG: function get_prefix")
		with open("prefix.txt") as f2:
				prefixes = f2.read()
				prefixes = prefixes.split("\n")
		print("prefixes split")
		chosen_prefix = random.choice(prefixes)
		print("chosen prefix")
		return chosen_prefix


def get_last_mention(r):
        #print("DEBUG: function get_last_mention")
        return r.comment(get_replied_comments()[-2])

def get_time_since_last_mention(r):
        print("DEBUG: function get_time_since_last_mention")
        last_comment_time = int(get_last_mention(r).created_utc)
        current_time = int(time.time())
        time_difference = current_time - last_comment_time
        # print("time calculation complete " + str(time_difference))
        if (time_difference > 24*3600*2):
                return (str(int(time_difference/24/3600)) + " days")

        elif(time_difference > 3600*2):
                return(str(int(time_difference/3600)) + " hours")

        elif(time_difference>60*2):
                return(str(int(time_difference/60)) + " minutes")
        else:
        		return (str(time_difference) + " seconds")

def remove_deleted_comments(r):
        #print("DEBUG: remove_deleted_comments")

        list = get_replied_comments()

        try:

                while (r.comment(list[-2]).author==None):
                        print("deleting comment id " + list[-2])
                        list = list[:-2]

                        with open("replied_comments.txt", "w") as f:
                                for item in list:
                                         f.write(item + "\n")

        except:
                print("error deleting comment")


r = bot_login()
print("clearing old comments")
remove_deleted_comments(r)

while True:
        try:
                run_bot(r, get_replied_comments())
        except:
                print("unkown error 1 occured")

                try:
                        r = bot_login()
                        run_bot(r, get_replied_comments())

                except:
                        print ("unkown error 2 occured")
                        #remove_deleted_comments(r)
