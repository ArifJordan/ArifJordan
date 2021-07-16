import requests
import tweepy
import time
import json

consumer_key = '1234'
consumer_secret = '1234'

access_token = "1234"
access_token_secret = "1234"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# api.update_status(
# 'Hello World, I am a bot, programmed by @TheArifJordan using the Python programming language.')


FILE_NAME = 'last_seen.txt'

goodBotCounter = 'good_bot_counter.txt'


def readCount(FILE):
    file_read = open(FILE, 'r')
    goodBotCount = int(file_read.read().strip())
    file_read.close()
    return goodBotCount


def updateCount(FILE, last_count):
    file_write = open(FILE, 'w')
    file_write.write(str(last_count))
    file_write.close()
    return


def read_last_seen(FILE_NAME):
    file_read = open(FILE_NAME, 'r')
    last_seen_id = int(file_read.read().strip())
    file_read.close()
    return last_seen_id


def store_last_seen(FILE_NAME, last_seen_id):
    file_write = open(FILE_NAME, 'w')
    file_write.write(str(last_seen_id))
    file_write.close()

    return


def inspire(tweet):

    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    try:

        api.update_status('@' + tweet.user.screen_name + " " + quote, tweet.id)
        print('Successfully tweeted random quote to ' + tweet.user.screen_name)
        store_last_seen(FILE_NAME, tweet.id)
        print('storing tweet id ')

    except tweepy.TweepError as e:
        print(e.reason)

        api.update_status('@TheArifJordan can you help out -> ' +
                          '@' + tweet.user.screen_name + " ?")


def returnMedia(tweet):

    # Returns photo, video, or gif to a user after inspecting the tweet they replied to #

    if (tweet.in_reply_to_status_id_str != ""):
        originalTweet = api.get_status(tweet.in_reply_to_status_id)

    else:
        originalTweet = tweet
        store_last_seen(FILE_NAME, tweet.id)
        api.update_status('@' + tweet.user.screen_name +
                          " You must reply -> !Steal <- to the original tweet with the image you want to steal. Or tag my dad 'TheArifJordan' to this tweet.", tweet.id)

    if (originalTweet.entities['media'][0]['type'] == 'photo'):
        try:
            image = originalTweet.extended_entities['media'][0].get(
                'media_url_https')
            api.update_status('@' + tweet.user.screen_name +
                              " Here you go :) " + image, tweet.id)
            store_last_seen(FILE_NAME, tweet.id)
        except tweepy.TweepError as e:
            print(e.reason)
            store_last_seen(FILE_NAME, tweet.id)
            api.update_status(
                '@TheArifJordan Dad can you help out -> ' + '@' + tweet.user.screen_name + " ?", tweet.id)

    elif (originalTweet.extended_entities['media'][0]['type'] == 'video'):
        try:
            video = originalTweet.extended_entities['media'][0]['video_info']['variants'][0]['url']
            api.update_status('@' + tweet.user.screen_name +
                              " Here you go :) " + video, tweet.id)
            store_last_seen(FILE_NAME, tweet.id)

        except tweepy.TweepError as e:
            print(e.reason)
            store_last_seen(FILE_NAME, tweet.id)
            api.update_status(
                '@TheArifJordan Dad can you help out -> ' + '@' + tweet.user.screen_name + " ?", tweet.id)
    elif (originalTweet.extended_entities['media'][0]['type'] == 'animated_gif'):
        try:
            gif = originalTweet.extended_entities['media'][0]['video_info']['variants'][0]['url']
            api.update_status('@' + tweet.user.screen_name +
                              " Here you go :) " + gif, tweet.id)
            store_last_seen(FILE_NAME, tweet.id)
        except tweepy.TweepError as e:
            print(e.reason)
            store_last_seen(FILE_NAME, tweet.id)
            api.update_status(
                '@TheArifJordan Dad can you help out -> ' + '@' + tweet.user.screen_name + " ?", tweet.id)
    else:
        store_last_seen(FILE_NAME, tweet.id)
        api.update_status(
            'Make sure you are tagging "!Steal" as a reply to the tweet that has the content you want to steal. Tag "TheArifJordan" if you still need help', tweet.id)


def replyToGoodBot(tweet):

    try:
        count = readCount(goodBotCounter) + 1
        api.update_status('@' + tweet.user.screen_name + " Thanks, I've been told that: " +
                          str(count) + " time(s)", tweet.id)
        api.create_favorite(tweet.id)
        updateCount(goodBotCounter, count)
        store_last_seen(FILE_NAME, tweet.id)
    except tweepy.TweepError as e:
        print(e.reason)
        store_last_seen(FILE_NAME, tweet.id)


def replyToBadBot(tweet):
    try:
        api.update_status('@' + tweet.user.screen_name +
                          " take it easy there playa. I'm still learning.", tweet.id)
        store_last_seen(FILE_NAME, tweet.id)
    except tweepy.TweepError as e:
        print(e.reason)
        store_last_seen(FILE_NAME, tweet.id)


def replyToQuestion(tweet):
    try:
        store_last_seen(FILE_NAME, tweet.id)
        api.update_status('@' + tweet.user.screen_name +
                          " @TheArifJordan did. You can learn about him here -> https://arifjordan.com", tweet.id)

    except tweepy.TweepError as e:
        print(e.reason)

# actually listening / checking for tweets where bot is mentioned 

def listen_for_mentions():
    mentions = api.mentions_timeline(
        read_last_seen(FILE_NAME), tweet_mode='extended')
    for mention in reversed(mentions):
        if ('!inspire' in mention.full_text.lower()):
            try:

                inspire(mention)

            except tweepy.TweepError as e:
                print(e.reason)
                api.update_status(
                    '@TheArifJordan can you help out -> ' + mention.user.screen_name + " ?", mention.id)

        elif ('!steal' in mention.full_text.lower()):
            try:
                returnMedia(mention)
            except tweepy.TweepError as e:
                print(e.reason)

        elif 'good bot' in mention.full_text.lower():
            try:
                replyToGoodBot(mention)

            except tweepy.TweepError as e:
                print(e.reason)
        elif ('bad bot' in mention.full_text.lower()):
            try:
                replyToBadBot(mention)
            except tweepy.TweepError as e:
                print(e.reason)
        elif ('who made you' or 'who created you' or 'who is your dad' in mention.full_text.lower()):
            try:
                replyToQuestion(mention)
            except tweepy.TweepError as e:
                print(e.reason)
    return


while True:
    try:
        listen_for_mentions()

        time.sleep(10)

    except tweepy.TweepError as e:
        print(e.reason)
