from twython import Twython
import pandas as pd

def to_list(str_list):
    return [e.translate(e.maketrans('', '', "[]\\'")).strip() for e in str_list.split(',')]

def get_tweets_v2(keys_file, user_handles):
    creds = {}
    with open(keys_file, 'r') as f:
        c = f.read().split('\n')
        creds['Consumer_Key'] = c[0]
        creds['Consumer_Secret'] = c[1]
        creds['Access_Key'] = c[2]
        creds['Access_Secret'] = c[3]

    py_tweets = Twython(creds['Consumer_Key'], creds['Consumer_Secret'])
    num_requests = 0

    for user_handle in user_handles:
        try:
            temp_file = open(user_handle + '.csv', 'r')
            temp_file.close()
        except IOError:
            user_df = pd.DataFrame(columns = ['User', 'Source_Name', 'Date', 'Time', 'Tweet_Text', 'ID', 'Article_Link'])
            user_df.set_index('ID', inplace = True)
        else:
            user_df = pd.read_csv(user_handle + '.csv', index_col = 'ID')
            user_df.index = user_df.index.astype('str')

        at_limit = False
        older_than = None

        while not at_limit:
            queryA = {'q' : 'from:' + user_handle,
                    'result_type' : 'recent',
                    'count' : 100,
                    'lang' : 'en',
                    'tweet_mode' : 'extended',
                    'max_id' : older_than
                    }

            user_dict = {'User' : [], 'Source_Name' : [], 'Date' : [], 'Time' : [], 'Tweet_Text' : [], 'ID' : [], 'Article_Link' : []}

            for status in py_tweets.search(**queryA)['statuses']:
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

            temp_df = pd.DataFrame(user_dict)
            temp_df.set_index('ID', inplace = True)
            user_df = user_df.append(temp_df)
            user_df.sort_index(inplace = True)

            if list(temp_df.index) != []:
                older_than = temp_df.index[-1]
            else:
                at_limit = True

            num_requests += 1

        user_df.to_csv(user_handle + '.csv')

    print(num_requests)