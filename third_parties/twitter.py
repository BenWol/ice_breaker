import os
import requests
from dotenv import load_dotenv
import tweepy

load_dotenv()

twitter_client = tweepy.Client(
    bearer_token=os.environ["TWITTER_BEARER_TOKEN"],
    consumer_key=os.environ["TWITTER_CONSUMER_KEY"],
    consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"],
    access_token=os.environ["TWITTER_ACCESS_TOKEN"],
    access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
)


def scrape_twitter_profile(username: str, num_tweets: int = 5, mock: bool = True):
    """
    Scrape Twitter profile information for a given username.

    This function fetches tweets and user information from the Twitter API for the specified username.
    It can handle both real API requests and mock responses for testing purposes.
    Args:
        username (str): The Twitter username to scrape.
        num_tweets (int, optional): The number of tweets to fetch. Defaults to 5.
        mock (bool, optional): Whether to use mock data. Defaults to True.

    Returns:
        dict: A dictionary containing user information and a list of tweets.
              The 'tweets' key contains a list of dictionaries, each representing a tweet
              with the following fields:
              - 'time_posted': A string representing the relative time the tweet was posted.
              - 'text': The content of the tweet.
              - 'url': The URL of the tweet.

    Note:
        This function scrapes a Twitter user's original tweets (i.e., not retweets or replies)
        and returns them as part of the user's profile information. The tweets are
        represented as a list of dictionaries within the returned data structure.
    """
    tweet_list = []

    if mock:
        EDEN_TWITTER_GIST = "https://gist.githubusercontent.com/emarco177/9d4fdd52dc432c72937c6e383dd1c7cc/raw/1675c4b1595ec0ddd8208544a4f915769465ed6a/eden-marco-tweets.json"
        tweets = requests.get(EDEN_TWITTER_GIST, timeout=5).json()
    else:
        user_id = twitter_client.get_user(username=username).data.id
        print(user)
        tweets = twitter_client.get_users_tweets(id=user_id, max_results=num_tweets, exclude=["retweets", "replies"])

    for tweet in tweets:
        tweet_dict = {}
        tweet_dict["time_posted"] = tweet["time_posted"]
        tweet_dict["text"] = tweet["text"]
        tweet_dict["url"] = f"https://twitter.com/{username}/status/{tweet["id"]}"
        tweet_list.append(tweet_dict)

    return tweet_list


if __name__ == "__main__":
    print(scrape_twitter_profile(username="EdenEmarco177"))