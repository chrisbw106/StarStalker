import tweepy
import json

class TweetCollector():
    def __init__(self):
        
        # authorization information
        self.consumer_key = 'ivTIyVE7N23P7Zf6val0A'
        self.consumer_secret = 'pLwuuHfSs5DQ6AjFgcvExvLCay3cBDPykw1KrLEeTI'
        self.access_token_key = '2187598915-rnBc8enRqFQeFwJIdBznDeMX3SFveRJhNJCrVCq'
        self.access_token_secret = '6aHe6iKgBTOvSO9Nh4zU5zA1XsvzFkwra8qy3eHaU8eRz'
        self.auth = tweepy.auth.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token_key, self.access_token_secret)
        
        # data storage
        self.queries = []
        self.results = {}
        self.stars = {}
    
    def collectTweetsByLoc(self):
        # collects and creates a file of tweets just by loc
        #get zipcode from google based on user query
        self.queries.append('college station,tx -RT')
    
        api = tweepy.API(self.auth)

        # go through queries and determine celebs
        for query in self.queries:
            with open('cstatLocCelebs2', 'a+') as outfile:
                for tweet in tweepy.Cursor(api.search,q= query, result_type="recent",lang = "en").items(250):
                    
                    self.results['User ID'] = tweet.user.id
                    self.results['Screen Name'] = tweet.user.screen_name
                    self.results['Text']= tweet.text
                    self.results['Created']= str(tweet.created_at)
                    self.results['Place']= str(tweet.place)
                    self.results['Geo'] = tweet.geo
                    self.results['Coord'] = tweet.coordinates
                    self.results['Follower Count'] = tweet.user.followers_count
                    self.results['Verified'] = tweet.user.verified
                    self.results['Mentions'] = tweet.entities
                    json.dump(self.results,outfile)
                    outfile.write('\n')

    def collectOthersTweets(self):
        # collects and creates a file of tweet about celeb
        
        self.queries.append('"just met" -RT')
        
        api = tweepy.API(self.auth)
        
        # go through queries about celeb and find 50 tweets
        for query in self.queries:
            with open('justMetHtown', 'a+') as outfile:
                for tweet in tweepy.Cursor(api.search,q= query,geocode = "29.752554,-95.37040089999999,20mi", lang = "en").items(250):
                    
                    '''self.results['User ID'] = tweet.user.id
                    self.results['Screen Name'] = tweet.user.screen_name
                    self.results['Text']= tweet.text
                    self.results['Created']= str(tweet.created_at)
                    self.results['Place']= str(tweet.place)
                    self.results['Geo'] = tweet.geo
                    self.results['Coord'] = tweet.coordinates
                    self.results['Follower Count'] = tweet.user.followers_count
                    self.results['Verified'] = tweet.user.verified
                    self.results['Mentions'] = tweet.entities'''
                    self.results[tweet.user.screen_name] = {('Text', tweet.text),('Created',str(tweet.created_at)),('Place',str(tweet.place),('Geo',tweet.geo),('Coord',tweet.coordintates)('Follower Count', tweet.user.followers_count),('Verified',tweet.user.verified),('Entities', tweet.entities)}
                    '''json.dump(self.results,outfile)
                    outfile.write('\n')'''
    
    
    def parsingResults(self):
        # going through mentioned users to determine if talking about celeb
        
        '''for clump in self.results
            if(('Follower Count') > 20000):
            if('Verified' = 'true'):
            
            if('Geo' != 'null'):
            if('Place' != 'None'):
            if('Coord' != 'null'):'''
                
            for k in self.results.keys():
                for mentionedPerson in self.results[k]['Entities']['user_mentions']:
					mentionedUser = api.get_user(mentionedPerson)
					if (mentionedUser['followers_count'] > 20000) or (mentionedUser['verified'] equals True)):
						self.stars[mentionedPerson] = {('Follower Count', mentionedUser['followers_count']),('Verification',mentionedUser['verified']),('Geo Tag', self.results[k]['Geo'])} 
					if(mentionedPerson equals self.results[k]):
						self.stars[mentionedPerson]= ('Direct Celeb', True)
					else:
						self.stars[mentionedPerson]= ('Direct Celeb', False)
            
    

    '''
    def collectCelebTweets(self):
        
        self.queries.append('from: jmanziel2')
        self.results = {}
        api = tweepy.API(self.auth)
        
        # go through queries about celeb and find 50 tweets
        for query in self.queries:
            for tweet in tweepy.Cursor(api.search,rpp = 100,q= query,result_type="mixed").items(200):
                if query not in self.results.keys():
                    self.results[query] = []
                self.results[query].append(dict([(tweet.user.name, [tweet.geo,tweet.text])]))
    
        #create json file
        with open('celebTweetsLG.json','wb') as file :
            json.dump(self.results,file)
    '''
        
if __name__ == "__main__":
    tc = TweetCollector()
    #tc.collectTweetsByLoc()
    tc.collectOthersTweets()
#tc.collectCelebTweets()
