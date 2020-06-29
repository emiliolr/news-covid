# news-covid

This is the associated code and data for the paper "News Media During an International Crisis: What Twitter Data Says About COVID-19." 
This is a freshman Monroe Scholar project and was funded by William & Mary.

# Data

To comply with [Twitter's content redistribution policy](https://developer.twitter.com/en/developer-terms/agreement-and-policy) (see the "Content Redistribution" heading), I have dehydrated my tweet data sets. This means that the _.ipynb_ files will have difficulty running without some intervention. 

The tweet IDs are inlcuded in `data/tweet_ids`. To rehydrate the tweet data set, you can use [Hydrator](https://github.com/DocNow/hydrator) or query the Twitter API directly. The format for the standard data set used in this project is shown below, with one example row.

ID | User | Source_Name | Tweet_Text | Date_Time
--- | --- | --- | --- | --- | 
1234991970243604482 | @ABC | ABC News | BREAKING: Joe Biden will win the Virginia primary, ABC News projects based on analysis of the exit poll. | 2020-03-04 00:00:05

# Folders 

`collection`

Contains the data collection method, `newest_API_collection.py`. 

`data`

`analysis`

`exploration`

`paper`
