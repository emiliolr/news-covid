# news-covid

This is the associated code and data for the paper "News Media During an International Crisis: What Twitter Data Says About COVID-19." 
This was a freshman Monroe Scholar project funded by William & Mary.

# About the Data

To comply with [Twitter's content redistribution policy](https://developer.twitter.com/en/developer-terms/agreement-and-policy) (see the "Content Redistribution" heading), I have dehydrated my tweet data sets. This means that the _.ipynb_ files will have difficulty running without some intervention. 

The tweet IDs are inlcuded in seperate _.txt_ files in `data/dehydrated_data`. To rehydrate the tweet data set, you can use [Hydrator](https://github.com/DocNow/hydrator) or query the Twitter API directly. The format for the standard data set used in this project is shown below, with one example row included.

ID | User | Source_Name | Tweet_Text | Date_Time
--- | --- | --- | --- | --- | 
1234991970243604482 | @ABC | ABC News | BREAKING: Joe Biden will win the Virginia primary, ABC News projects based on analysis of the exit poll. | 2020-03-04 00:00:05

# Folders 

1. `collection`

Contains the data collection method, `newest_API_collection.py`. This will get all tweets in the past week from a given list of users, saving each user's obtained data as a seperate _.csv_ file. 

**Note:** this is used to collect **new** tweets, **not** to rehydrate the data sets used for this project.

2. `data`

Contains the dehydrated tweet data sets. For the data sets used in the paper, look at `data/dehydrated_data` (tweets from **March 4th - April 1st**). For the extended data sets, which include extra tweets that were not analyzed in the paper, look at `data/full_dehydrated_data` (tweets from **March 3rd - April 22nd**).

3. `analysis`

Contains the code for applying **sentiment analysis** (using TextBlob) and **named entity recognition** (using spaCy) to the data. `applying_analysis_methods.ipynb` also includes a basic pipeline for implementing **word collocations** (using NLTK), although this method was not used for the paper.

4. `exploration`

Contains the exploration notebooks. The code used to produce the visualizations from the "Results" section of the paper is included here. `basic_SA.ipynb` includes all the sentiment analysis exploration; `convergence_on_COVID.ipynb` looks at the percentage of articles about COVID over time; `looking_at_NEs.ipynb` includes all of the named entity recogntion exploration. 

5. `miscellaneous`

6. `paper`
