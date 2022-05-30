from dotenv import load_dotenv
import os
import tweepy as tw
import pandas as pd


def configure_dotenv() -> tuple:
    load_dotenv()
    return os.getenv("api_key"), os.getenv("api_key_secret"), os.getenv("access_token"), os.getenv("access_token_secret")


def authenticate(api_key, api_key_secret, access_token, access_token_secret):
    auth = tw.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth)
    return api


def get_tweets(api, user, limit):
    tweets = tw.Cursor(api.user_timeline, screen_name=user,
                       count=200, tweet_mode="extended").items(limit)
    return tweets


def create_dataframe(data, columns):
    res = []
    for tweet in data:
        res.append([tweet.full_text])

    df = pd.DataFrame(res, columns=columns)
    return df


def create_csv(dataframe, path):
    dataframe.to_csv(path, sep='\t', encoding='utf-8', index=False)


def main():
    api_key, api_key_secret, access_token, access_token_secret = configure_dotenv()
    api = authenticate(api_key, api_key_secret,
                       access_token, access_token_secret)

    tweets = get_tweets(api, "NASA", 70000)
    df = create_dataframe(data=tweets, columns=['Tweet'])

    create_csv(df, "src/model_creation/data/data.csv")


if __name__ == "__main__":
    main()
