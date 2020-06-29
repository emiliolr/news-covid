from twython import Twython
import pandas as pd

def get_tweets_v2(keys_file, user_handles):
    '''
    Input:
    keys_file - .txt file with Twitter API credentials, seperated by newlines
    user_handles - Twitter handles of users to get data for

    Output:
    .csv file for each user containing all tweets from past week
    '''

    #getting credentials
    creds = {}
    with open(keys_file, 'r') as f:
        c = f.read().split('\n')
        creds['Consumer_Key'] = c[0]
        creds['Consumer_Secret'] = c[1]
        creds['Access_Key'] = c[2]
        creds['Access_Secret'] = c[3]

    py_tweets = Twython(creds['Consumer_Key'], creds['Consumer_Secret'])
    num_requests = 0

    #getting tweets for each user
    for user_handle in user_handles:
        #first seeing if a new file must be made
        try:
            temp_file = open(user_handle + '.csv', 'r')
            temp_file.close()
        except IOError:
            user_df = pd.DataFrame(columns = ['User', 'Source_Name', 'Date', 'Time', 'Tweet_Text', 'ID', 'Article_Link'])
            user_df.set_index('ID', inplace = True)
        else:
            user_df = pd.read_csv(user_handle + '.csv', index_col = 'ID')
            user_df.index = user_df.index.astype('str')

        #keeping track of whether or not we're still getting new tweets
        at_limit = False
        older_than = None

        #getting tweets
        while not at_limit:
            #building query
            queryA = {'q' : 'from:' + user_handle,
                    'result_type' : 'recent',
                    'count' : 100,
                    'lang' : 'en',
                    'tweet_mode' : 'extended',
                    'max_id' : older_than
                    }

            #dict to save results
            user_dict = {'User' : [], 'Source_Name' : [], 'Date' : [], 'Time' : [], 'Tweet_Text' : [], 'ID' : [], 'Article_Link' : []}

            #querying the API through twython
            for status in py_tweets.search(**queryA)['statuses']:
                #building all rows
                if status['id_str'] not in user_df.index:
                    user_dict['User'].append('@' + status['user']['screen_name'])

                    user_dict['Source_Name'].append(status['user']['name'])

                    date_time = status['created_at'].split()
                    user_dict['Date'].append(' '.join(date_time[0 : 3]) + ' ' + date_time[5])
                    user_dict['Time'].append(date_time[3])

                    s = status['full_text']
                    if s.startswith('RT @'):
                        s = s.split(':')[0] + ': ' + status['retweeted_status']['full_text']
                    link_index = s.find('http')

                    if link_index != -1:
                        user_dict['Tweet_Text'].append(s[0 : link_index].replace('\n', ' '))
                    else:
                        user_dict['Tweet_Text'].append(s.replace('\n', ' '))

                    user_dict['ID'].append(status['id_str'])

                    if status['entities']['urls'] != []:
                        user_dict['Article_Link'].append(status['entities']['urls'][-1]['expanded_url'])
                    else:
                        user_dict['Article_Link'].append(None)

            #adding new rows to dataframe
            temp_df = pd.DataFrame(user_dict)
            temp_df.set_index('ID', inplace = True)
            user_df = user_df.append(temp_df)
            user_df.sort_index(inplace = True)

            #checking if we've hit the Twitter-imposed limit
            if list(temp_df.index) != []:
                older_than = temp_df.index[-1]
            else:
                at_limit = True

            num_requests += 1

        #save file
        user_df.to_csv(user_handle + '.csv')

    #print the total number of requests
    print(num_requests)

if __name__ == '__main__':
    get_tweets_v2('tInfo.txt', ['nytimes', 'CNN'])
