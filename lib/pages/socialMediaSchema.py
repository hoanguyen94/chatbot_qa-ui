import pandas as pd

influencerColumns = ['channel', 'userid', 'name', "category1", "category2",
                     "country", "followers", "views", "likes", "comments", "shares"]

exampleDF_Influencers = pd.DataFrame({'channel': ["youtube", "tiktok"], 'userid': ["samso", "peter123"],
                                      'name': ['Sam', 'Peter'], "category1": ["music", "movies"], "category2": ["pop", "cartoon"],
                                      "country": ["Germany", "Austria"], "followers": [1000, 5000], "views": [10000, 4000],
                                      "likes": [100, 500], "comments": [200, 400], "shares": [100, 120]})
