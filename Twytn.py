from twython import Twython
from twython import TwythonStreamer
import pandas as pd 
import json, tweepy, time
from dateutil import parser
from datetime import datetime, date
from PIL import Image
from io import StringIO


class TwitterAuto:
    """This is a program that helps to automate lots of processes on twitter like analysing accounts,
    checking out for bots, post status, decide who to follow and follow, destro follow, etc."""

    with open(r'C:\Users\richa\Secrets\Twi_API.json') as f:
        creds = json.load(f)  #This file contains my twitter API keys. #Available with a gun to my head and £100million. Lol
    
    def __init__(self, client):
        self.client = client

    def limit_handled(cursor):
        
        while True:
            try:
                yield cursor.next()
            except tweepy.RateLimitError:
                time.sleep(15 * 60)
       

    def test_rate_limit(api, wait=True, buffer=.1):
        
        """Tests whether the rate limit of the last request has been reached.
        :param api: The `tweepy` api instance.
        :param wait: A flag indicating whether to wait for the rate limit reset
                    if the rate limit has been reached.
        :param buffer: A buffer time in seconds that is added on to the waiting
                    time as an extra safety margin.
        :return: True if it is ok to proceed with the next request. False otherwise.
        """
        #Get the number of remaining requests
        remaining = int(api.last_response.headers['x-rate-limit-remaining'])
        #Check if we have reached the limit
        if remaining == 0:
            limit = int(api.last_response.headers['x-rate-limit-limit'])
            reset = int(api.last_response.headers['x-rate-limit-reset'])
            #Parse the UTC time
            reset = datetime.fromtimestamp(reset)
            #Let the user know we have reached the rate limit
            print("0 of {} requests remaining until {}.".format(limit, reset))

            if wait:
                #Determine the delay and sleep
                delay = abs(reset - datetime.now()).total_seconds() + buffer
                print("Sleeping for {}s...".format(delay))
                sleep(delay)
                #We have waited for the rate limit reset. OK to proceed.
                return True
            else:
                #We have reached the rate limit. The user needs to handle the rate limit manually.
                return False 

        #We have not reached the rate limit
        return True


    def Twitter_info(self, user_name):
        self.client = client
        result = client.show_user(screen_name=user_name, tweet_mode='extended') #This part used twython
        time_created = result['created_at']
        time_created_timestamp = parser.parse(time_created).timestamp()
        date_created = date.fromtimestamp(time_created_timestamp) #Removing min, sec and microsec from time_created
        today_date = datetime.now()
        account_age_seconds = today_date.timestamp() - time_created_timestamp
        account_age_weeks = round((account_age_seconds / 606877), 2)
        account_age_months = round((account_age_seconds / 2629800), 2)
        account_age_years = round((account_age_seconds / 31557600), 2) #I used 365.25 days for a year

        if account_age_years >= 1:
            account_age = str(account_age_years) + ' year' 
        elif account_age_years < 1 and account_age_months >= 1:
            account_age = str(account_age_months) + ' month'
        elif account_age_years and account_age_months < 1:
            account_age = str(account_age_weeks) + ' week'
        elif account_age_weeks < 1:
            account_age = "less than a week"
        total_follower = result['followers_count']
        total_following = result['friends_count']
        print(f'\n{user_name} account was created on {date_created} and it is {account_age} old today.')

        try:
            if total_follower and total_following:
                folow_to_folower_ratio = round((total_follower / total_following), 3)
            elif total_following and not total_follower:
                folow_to_folower_ratio = 0
            elif total_follower and not total_following:
                folow_to_folower_ratio = 0
            elif not total_follower and not total_following:
                folow_to_folower_ratio = 0
        except ZeroDivisionError:
            pass
        else:
            print(f'\n{user_name} total follower is {total_follower}, total following is {total_following} and follower-to-following ratio is {folow_to_folower_ratio}.')
            if folow_to_folower_ratio >= 0.3:
                s_global_ff_rat.append(folow_to_folower_ratio)
                return s_global_ff_rat
            else:
                pass

        total_tweet = result['statuses_count']
        total_like = result['favourites_count']                                                                                                                                           
        try:
            if total_tweet and total_like:
                tweet_to_like_ratio = round((total_tweet / total_like), 3)
            elif total_tweet and not total_like:
                tweet_to_like_ratio = 0
            elif total_like and not total_tweet:
                tweet_to_like_ratio = 0
            elif not total_like and not total_tweet:
                tweet_to_like_ratio = 0
        except ZeroDivisionError:
            pass
        else:
            print(f'\n{user_name} total tweet is {total_tweet}, total like is {total_like} and tweet-to-like-ratio is {tweet_to_like_ratio}.')
        
        try:
            last_status_id = result['status']['id']
        except KeyError:
            last_status_idd = 'None'
            last_status_text = 'None'
            user_replied_to = 'None'
            user_replied_to_screenName = 'None'
            print(f'\n{user_name} has not replied to any tweet.')
            #print(f'\n{user_name} last reply was: {last_status_text} in reply to: {user_replied_to_screenName} on their tweet with tweetid: {last_status_idd}')
        else:
            last_status_idd = last_status_id
            last_status_text = result['status']['full_text']
            user_replied_to = result['status']['entities']['user_mentions']
            user_replied_to_screenName = [element['screen_name'] for element in user_replied_to]
            print(f'\n{user_name} last reply was: {last_status_text} in reply to: {" ".join(map(str, user_replied_to_screenName))} on their tweet with tweetid: {last_status_idd}.')

    def User_timeline(self, user_name):
        self.client = client
        tweet_list = client.cursor(client.get_user_timeline, id=user_name)
        print(tweet_list)
        for i in tweet_list:
            b = [c for c in i['text'].split()]
            a = [elem['screen_name'] for elem in i['entities']['user_mentions']]
            for d in a:
                print(" ".join(map(str, b))+ ' : ' +d)

    def client_timeline(self):
        self.client = client
        tweet_list = limit_handled(client.Cursor(client.get_home_timeline).items(200)
        for i in tweet_list:
            b = [c for c in i['text'].split()]
            a = [elem['screen_name'] for elem in i['entities']['user_mentions']]
            for d in a:
                #s_global_sc_name.append(d)
                print(d+ ' : ' +" ".join(map(str, b)))
    
    def like_tweet(self, tweetid):
        self.client = client
        try: client.create_favorite(id=tweetid)
        except Exception as e:
            print(e)

    def post_status(self, message='Hi'):
        self.client = client
        post = client.update_status(status=message) 

    def post_image(filename, status_message):
        with open(filename, 'rb') as f_photo:
            response = twitter.upload_media(media=f_photo)
            twitter.update_status(status=status_message, media_ids=[response['media_id']])

    def post_edit_image(filename, status_message):
         with open(filename) as photo_edited:
            basewidth = 320
            wpercent = (basewidth / float(photo_edited.size[0]))
            height = int((float(photo_edited.size[1]) * float(wpercent)))
            photo_edited = photo_edited.resize((basewidth, height), Image.ANTIALIAS)
            image_io = StringIO.StringIO()
            photo_edited.save(image_io, format='JPEG')
            image_io.seek(0)
            response = twitter.upload_media(media=f_photo_edited)
            twitter.update_status(status=status_message, media_ids=[response['media_id']])

    def post_video(filename, status_message):
        with open(filename, 'rb') as f_video:
            response = twitter.upload_video(media=f_video, media_type='video/mp4')
            twitter.update_status(status=status_message, media_ids=[response['media_id']])

    def reply_status(self, message, author_name, tweet_id):
        self.client = client
        reply = f'{message} @{author_name}'
        post = client.update_status(status=reply, in_reply_to_status_id=tweet_id)


    def users_friends(self, filename, screen_name):
        """This function takes a user screen name, get a list of 100 friends and 100 followers each at a time.
        The friends and followers screen names are then saved in a csv file."""
        self.filename = filename
        s = [] # They are empty lists to which we will append unique friends and followers. A follower may appear in a friend list
        t = [] # but each element of the individual lists will be unique. This is because I'll save them as a roll of 2 elements
        for friends in tweepy.Cursor(api.friends, user_name=username).items(100):
            try:
                if friends in s:
                    continue
                else:
                    s.append(friends.screen_name)
            except Exception as ex:
                print(ex)
                continue

        for follower in tweepy.Cursor(api.followers, user_name=username).items(100):
            try:
                if follower in t:
                    continue
                else:
                    t.append(follower.screen_name)
            except Exception as ex:
                print(ex)
                continue
        with open(filename, 'w') as file: #I want to always overwrite the file with each run so that it doesn't turn
            header = 'friend, follower\n' #unneccessarily big. If I must put this program on a server, then I wll change to append.
            file.write(header)            #I could also store them in different files and perform set operations on them. 
            for friend, follower in zip(s, t):
                file.write(friend + ',' + follower + '\n')


    def who_to_follow(self, filename1, filename2):
        """This function iterate over the following and follower list saved in a csv file (filename1) described above,
        does some maths calculation to filter who to follow. The new list is saved in a text file(filename2)"""
        self.filename1 = filename1
        self.filename2 = filename2
        with open(filename1, newline='') as csvfile: 
            a = []
            b = []
            filereader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            filereader.__next__()
            for row in spamreader:
                x = (', '.join(row))
                i = x.split(',')
                friend_name = i[0].strip()
                follower_name = i[1].strip()
                user1 = api.get_user(friend_name)
                user1_friend_count = user1.friends_count
                user1_follower_count = user1.followers_count
                user2 = api.get_user(follower_name)
                user2_friend_count = user2.friends_count
                user2_follower_count = user2.followers_count
                """Let's get a list of uers who have at least 300 followers (to exclude obvious bots) and who follow at least 30% users...
                to exclude those users that feel like they're influencers and don't follow back. I intend to add more statistical
                analysis here in the future to improve the rate of follow back. I hope analysis like account creation date, last status
                update, activities on TL can reduce number of bots folowed and improve rate of follow back. """
                if user1_friend_count/user1_follower_count >= 0.3 and user1_follower_count > 300: #I intend to follow users who follow at least 30%
                    if friend_name in a:                                                          #back to exclude those users who don't followback
                        continue                                                                   
                    else:
                        a.append(friend_name)   
                else:
                    pass
                if user2_friend_count/user2_follower_count >= 0.3 and user2_follower_count > 300:
                    if follower_name in b:
                        continue
                    else:
                        b.append(follower_name)   
                else:
                    pass
                with open (filename2, 'w') as f_frnds:
                    for r, v in zip(a,b):
                        print(r, v, file=f_frnds)

    def frndship(self, filename):
        """This function takes the screen_name of each user(friend & follower) from the text file described above,
        iterate over the list and follow them"""
        self.filename = filename
        with open(filename) as f_list:
            for i in f_list.readlines():
                friends = i.split()[0].strip()
                followers = i.split()[1].strip()
                try:
                    a = api.create_friendship(friends) # It doesn't raise an exception if a user is already followed and no real need for that 
                except Exception as ex:                # Maybe we can get list of users successfully followed in a separate file. Can manipulate this for influencing
                    print(ex)                          # I will place a log file decorator on this function to enable me get specific
                    pass                               #moment a friendship is initIated.
                try:
                    b = api.create_friendship(followers)
                except Exception as ex:
                    print(ex)
                    pass    
        return True

    def destroy_frndship(self, client, filename):
        """"This function takes the screen_name of each user(friend & follower) from the text file whom we follow above,
        iterate over the list and unfollow them. Unfollowing users from the list will ensure we don't unfollow
        genuine members. I intend to wait for 5 days after following them before unfollowing (great, right?)"""
        self.filename = filename
        self.client = client
        with open(filename) as f_list:
            for i in f_list.readlines():
                friends = i.split()[0].strip()
                followers = i.split()[1].strip()
                try:
                    a = client.destroy_friendship(friends) # We can use api.show_friendship method on our account check the objects returned
                except Exception as ex:                 # and destroy frienships with those that don't roll with us.        
                    print(ex)
                    pass           
                try:
                    b = client.destroy_friendship(followers)
                except Exception as ex:
                    print(ex)
                    pass    
        return True 

a = TwitterAuto.creds
try:
    client = Twython(a["consumer_key"], a["app_secret"], a["oauth_token"], a["oauth_token_secret"])
except Exception:
    auth = tweepy.OAuthHandler(a["consumer_key"], a["app_secret"]) # I started with twython but later learned that tweepy is better for some parts \
    auth.set_access_token(a["oauth_token"], a["oauth_token_secret"]) # and I'm too lazy to write the program all over with tweepy. so, yes...
    client = tweepy.API(auth)

if __name__ == "__main":
    result = TwitterAuto(client)
    result.client_timeline()
    result.destroy_frndship('247purchase', 'frnds.txt')
    
"""There is yet another file that calls some methods here to consume large volume of targetted data in use for data analysis"""
"""Currently using the whole results to implement NLP, which opens a new dimension for business"""