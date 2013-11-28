import tweepy
import json
import math

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
        self.starname
        self.location
        self.geolat
        self.geolng
        self.queries = []
        self.results = {}
        self.stars = {}
    
    #OLD COLLECTOR
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

    #FIX ME - store by tweet.id not screen_name
    def collectOthersTweets(self):
        # collects and creates a file of tweet about celeb
        
        self.queries.append('"just met" -RT')
        
        api = tweepy.API(self.auth)
        
        # go through queries about celeb and find 50 tweets
        for query in self.queries:
            with open('justMetHtown', 'a+') as outfile:
                for tweet in tweepy.Cursor(api.search,q= query,geocode = "29.752554,-95.37040089999999,20mi", lang = "en").items(100):
                    self.results[tweet.user.screen_name] = {}
                    self.results[tweet.user.screen_name]['Text']= tweet.text
                    self.results[tweet.user.screen_name]['Created'] = str(tweet.created_at)
                    self.results[tweet.user.screen_name]['Place']=str(tweet.place)
                    self.results[tweet.user.screen_name]['Geo'] = tweet.geo
                    self.results[tweet.user.screen_name]['Coord']=tweet.coordinates
                    self.results[tweet.user.screen_name]['Follower Count']= tweet.user.followers_count
                    self.results[tweet.user.screen_name]['Verified'] = tweet.user.verified
                    self.results[tweet.user.screen_name]['Entities']= tweet.entities
                    json.dump(self.results,outfile)
                    outfile.write('\n')
    
    def parsingTweeters(self):
    	api = tweepy.API(self.auth)
    	for tweeter in self.results.keys():
    		with open('TweetStars', 'a+') as outfile:
    			user= api.get_user(tweeter)
    			
    			if (user.followers_count > 20000) or (user.verified == True):
    				#print user.screen_name 
    				#print user.followers_count 
    				self.stars[tweeter] = {}
    				self.stars[tweeter]['Follower Count']= user.followers_count
    				self.stars[tweeter]['Verified']= user.verified
    				self.stars[tweeter]['Geo']= self.results[tweeter]['Geo']
    				self.stars[tweeter]['Direct Star'] = True
    				json.dump(self.stars,outfile)
    				outfile.write('\n')
    			
    	
    def parsingMentions(self):
        # going through mentioned users to determine if talking about celeb   
        api = tweepy.API(self.auth)             
        for k in self.results.keys():
        	with open('Stars', 'a+') as outfile:
	            for mentionedPerson in self.results[k]['Entities']['user_mentions']:
	                mentionedUser = api.get_user(mentionedPerson['screen_name'])
	               
	                if (mentionedUser.followers_count > 20000) or (mentionedUser.verified == True):
	                	#print mentionedUser.screen_name
	                	#print k
	                	self.stars[mentionedUser.screen_name] = {}
	                	self.stars[mentionedUser.screen_name]['Follower Count']= mentionedUser.followers_count
	                	self.stars[mentionedUser.screen_name]['Verified']= mentionedUser.verified
	                	self.stars[mentionedUser.screen_name]['Geo']= self.results[k]['Geo']
	                	self.stars[mentionedUser.screen_name]['Direct Star'] = False
	                	json.dump(self.stars,outfile)
	                	outfile.write('\n')
                        
        def CosineSim(self, vec_query, vec_doc):
        #dot product
        dot = 0
        qmag = 0
        dmag = 0
        for idx, qn in enumerate(vec_query):
            dot = dot + (qn*vec_doc[idx])
            qmag = qmag + (qn*qn)
            dmag = dmag + (vec_doc[idx]*vec_doc[idx])
        qmag = math.sqrt(qmag)
        dmag = math.sqrt(dmag)
        return dot/(qmag*dmag)
    
    def buildVector(self, star):
        vec = []
        
        if(self.stars[star]['Verified']):
            vec.append(1)
        else:
            vec.append(0)
        
        vec.append(self.stars[star]['Mention Count'])
        
        if(self.stars[star]['Geo']!='null'):
            vec.append(1)
        else:
            vec.append(0)
        
        if(self.stars[star]['Direct Star']):
            vec.append(1)
        else:
            vec.append(0)
        
        return vec

    def rankStars(self):
        print self.stars
        ranked = []
        
        #Vector =[Verification, #Mentions, GeoTaged, FromCeleb]    
        ideal = [1,5,1,1]
        
        #Rank Each Star based on features and ideal similarity
        for star in self.stars.keys():
            starvec = self.buildVector(star)
            rank = self.CosineSim(starvec,ideal)
            rank = rank + .3*(math.log10(self.stars[star]['Follower Count'])/10)
            rank = rank + .3*(starvec[0])
            rank = rank + .2*(1+math.log10(starvec[1])/10)
            rank = rank + .1*(starvec[2])
            rank = rank + .1*(starvec[3])
            ranked.append((star,rank))
        
        rsorted = sorted(ranked, key=lambda data: data[1])
        rsorted = [i for i in reversed(rsorted)]
        
        print rsorted
                        
                        
    def readInput(self):
        lines = [line.strip() for line in open('input_data.txt')]
        self.location = lines[0]
        self.starname = lines[1]
        self.geolat = lines[2]
        self.geolng = lines[3]

                        
if __name__ == "__main__":
    tc = TweetCollector()
    tc.readInput()
    
    #tc.collectTweetsByLoc()
    #tc.collectOthersTweets()
    #tc.parsingMentions()
    #tc.parsingTweeters()
    #tc.collectCelebTweets()
