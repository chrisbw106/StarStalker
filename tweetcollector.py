import tweepy
import json
import math

class TweetCollector():
    def __init__(self):
        
        # SS authorization information
        #self.consumer_key = 'ivTIyVE7N23P7Zf6val0A'
        #self.consumer_secret = 'pLwuuHfSs5DQ6AjFgcvExvLCay3cBDPykw1KrLEeTI'
        #self.access_token_key = '2187598915-rnBc8enRqFQeFwJIdBznDeMX3SFveRJhNJCrVCq'
        #self.access_token_secret = '6aHe6iKgBTOvSO9Nh4zU5zA1XsvzFkwra8qy3eHaU8eRz'
        
        #David's login
        self.consumer_key = "zfkFLLrMmDA8ojyqyrYcw"
        self.consumer_secret = "eTf1oL8uCTp04OVQLtudOh33CA8MVdoIvnoYJppAn0"
        self.access_token_key = "1972352642-Niy99g2jyZGMIHfDKcKttNjmty0LUCri4dKHdFR"
        self.access_token_secret = "tbe9vEBgXhIgVuCue5YcPr20W1VRAXJkPwgVRpET4"
        
        #Christine's login
        #self.consumer_key = 'hWjShWB1zy3nFPiZAeiGDw'
        #self.consumer_secret = 'WVAiwKleMPcU6odK9GDgN78z2TO33besdXhWrmUEQ'
        #self.access_token_key = '496512154-WTtSOwcMnI98KC2gb5qI1P34tig1899EH03cPuBf'
        #self.access_token_secret = 'Ko8y1QhwPo3vScx6vslaLYPqAiuIjoLNXt5Tuyow'
        
        #Keleigh's login
        #self.consumer_key = 'tHn9c6xyP8Kuyot1UsqhQw'
        #self.consumer_secret = 'ilwnOuMm2wYZLbyyf7seNG3O943kj9vf5UMifAY8'
        #self.access_token_key = '344466953-k5pS83JQCqmEezlF7dMcFVlAxUPEFY02Yb4ZtzTh'
        #self.access_token_secret = 'rf6vGZgt8Neqt1u7lW7xbYyJItr9lx5lMSRpALFSKFU'
        
        self.auth = tweepy.auth.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token_key, self.access_token_secret)
        
        # data storage
        self.location = ""
        self.starname = ""
        self.geolat = ""
        self.geolng = ""
        self.queries = []
        self.results = {}
        self.stars = {}
    
    def readInput(self):
        lines = [line.strip() for line in open('input_dataCS.txt')]
        self.location = lines[0]
        self.starname = lines[1]
        self.geolat = lines[2]
        self.geolng = lines[3]

    def collectOthersTweets(self):
        # collects and creates a file of tweet about celeb
        
        if(self.starname != 'null'):
            self.queries.append("just met" + '"' + self.starname + '"' +'-RT')
            self.queries.append("just saw" + '"' + self.starname + '"' + '-RT')
            self.queries.append("spotted " + '"' + self.starname + '"' + '-RT')
            self.queries.append("sighted " + '"' + self.starname + '"' + '-RT')
        else:
            self.queries.append('"just met" -RT')
            self.queries.append('"just saw" -RT')
            self.queries.append('"spotted" -RT')

        api = tweepy.API(self.auth)
        
        # go through queries about celeb and find tweets
        for query in self.queries:
            with open('ResultsCS', 'a+') as outfile:
                for tweet in tweepy.Cursor(api.search,q= query,geocode = str(self.geolat)+"," + str(self.geolng)+ ",20mi", lang = "en").items(100):
                    self.results[tweet.id] = {}
                    self.results[tweet.id]['Screen Name'] = tweet.user.screen_name
                    self.results[tweet.id]['Name'] = tweet.user.name
                    self.results[tweet.id]['tId'] = tweet.id
                    self.results[tweet.id]['Text']= tweet.text
                    self.results[tweet.id]['Created'] = str(tweet.created_at)
                    self.results[tweet.id]['Place'] = str(tweet.place)
                    self.results[tweet.id]['Geo'] = tweet.geo
                    self.results[tweet.id]['Coord']= tweet.coordinates
                    self.results[tweet.id]['Follower Count'] = tweet.user.followers_count
                    self.results[tweet.id]['Verified'] = tweet.user.verified
                    self.results[tweet.id]['Entities']= tweet.entities
                    
                    json.dump(self.results[tweet.id],outfile)
                    outfile.write('\n')
        print len(self.results.keys())
    
    def parsingTweeters(self):
        # determining if tweeter is a celeb
    	api = tweepy.API(self.auth)
        
        for tId in self.results:
            with open('StarsCS', 'a+') as outfile:
                user = self.results[tId]
                if (user['Follower Count']> 20000) or (user['Verified'] == True):
                    if(user['Screen Name'] not in self.stars.keys()):
                        # checking for repeats
                        self.stars[user['Screen Name']] = {}
                        self.stars[user['Screen Name']]['Screen Name'] = user['Screen Name']
                        self.stars[user['Screen Name']]['Follower Count'] = user['Follower Count']
                        self.stars[user['Screen Name']]['Verified']= user['Verified']
                        self.stars[user['Screen Name']]['Geo']= [user['Geo']]
                        self.stars[user['Screen Name']]['Direct Star'] = True
                        self.stars[user['Screen Name']]['Mention Count'] = 1
                        self.stars[user['Screen Name']]['Name'] = user['Name']
                    else:
                        self.stars[user['Screen Name']]['Geo'].append(user['Geo'])
                        self.stars[user['Screen Name']]['Mention Count'] = self.stars[user['Screen Name']]['Mention Count'] + 1
                    json.dump(self.stars[user['Screen Name']],outfile)
                    outfile.write('\n')
    			
    def parsingMentions(self):
        # going through mentioned users to determine if talking about celeb
        
        api = tweepy.API(self.auth)
        
        for tId in self.results.keys():
        	with open('StarsCS', 'a+') as outfile:
	            for mentionedPerson in self.results[tId]['Entities']['user_mentions']:
                        mentionedUser = api.get_user(mentionedPerson['screen_name'])
                        if(mentionedUser.followers_count > 20000) or (mentionedUser.verified == True):
                            if(mentionedUser.screen_name not in self.stars.keys()):
                                # checking for repeats
                                self.stars[mentionedUser.screen_name] = {}
                                self.stars[mentionedUser.screen_name]['Screen Name'] = mentionedUser.screen_name
                                self.stars[mentionedUser.screen_name]['Follower Count']= mentionedUser.followers_count
                                self.stars[mentionedUser.screen_name]['Verified']= mentionedUser.verified
                                self.stars[mentionedUser.screen_name]['Geo']= [self.results[tId]['Geo']]
                                self.stars[mentionedUser.screen_name]['Direct Star'] = False
                                self.stars[mentionedUser.screen_name]['Mention Count'] = 1
                                self.stars[mentionedUser.screen_name]['Name'] = mentionedUser.name
                            else:
                                self.stars[mentionedUser.screen_name]['Geo'].append(self.results[tId]['Geo'])
                                self.stars[mentionedUser.screen_name]['Mention Count'] = self.stars[mentionedUser.screen_name]['Mention Count'] + 1
                                
                            json.dump(self.stars[mentionedUser.screen_name],outfile)
                            outfile.write('\n')

        if(self.starname != 'null'):
            tc.starCorrection()
                        
    def starCorrection(self):
        # fixes error when user searches for specific celeb
        api = tweepy.API(self.auth)
        starKeys = self.stars.keys()
        for star in starKeys:
            if(self.stars[star]['Name'] != self.starname):
                self.stars.pop(star, None)
    '''
    def geoCounter(self):
        # populate geoDict with locations and the number of mentions of that locationo
        locList = [set(self.stars[self.starname]['Geo'])] # locations minus duplicates
        geoDict = {}
        for loc in locList:
            for geo in self.stars[self.starname]['Geo']:#locations plus duplicates
                if loc == geo:
                    if loc not in self.geoDict.keys():
                        geoDict[loc] = {}
                        geoDict[loc]['Follower Count'] = self.stars[self.starname]['Follower Count']
                        geoDict[loc]['Verified']= self.stars[self.starname]['Verified']
                        geoDict[loc] = loc
                        geoDict[loc]['Direct Star'] = True
                        geoDict[loc]['Location Count'] = 1
                    else:
                        geoDict[loc]['Location Count'] = self.geoDict[loc]['Location Count'] + 1
        
        self.stars = geoDict

    def getStarname(self):
        return self.starname
    '''
                    
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
        
        vec.append(1 if self.stars[star]['Verified'] else 0)
        vec.append(1 if self.stars[star]['Mention Count'] else 0)
        for loc in self.stars[star]['Geo']:
            if loc == None:
                geoVal = 0
            else:
                geoVal = 1
        vec.append(geoVal)
        vec.append(1 if self.stars[star]['Direct Star'] else 0)
        
        return vec

    def rankStars(self):
        #print self.stars
        ranked = []
        
        #Vector =[Verification, #Mentions, GeoTaged, FromCeleb]    
        ideal = [1,5,1,1]
        
        #Rank Each Star based on features and ideal similarity
        for star in self.stars.keys():
            starvec = self.buildVector(star)
            cos = self.CosineSim(starvec,ideal)
            rank = 0
            rank = rank + .3*(math.log10(self.stars[star]['Follower Count'])/10)
            rank = rank + .2*(starvec[0])   #verification
            rank = rank + .15*(1+math.log10(starvec[1])/10)  #mention count
            rank = rank + .3*(starvec[2])   #geo
            geo = .3 * (starvec[2])
            rank = rank + .05*(starvec[3])   #directStar
            rank = rank + cos
            ranked.append((star,rank,cos,geo))
        
        rsorted = sorted(ranked, key=lambda data: data[1])
        rsorted = [i for i in reversed(rsorted)]
        
        for i in range(min(10,len(rsorted))):
            print str(i+1) + " " + str(rsorted[i])
        return rsorted
    
    def read_data(self,filename):
        #Used to read all tweets from the json file
        data = []
        try:
            with open(filename) as f:
                for line in f:
                    data.append(json.loads(line.strip()))
        except:
            print "Failed to read data!"
            return []
        print "The json file has been successfully read!"
        
        for tweet in data:
            self.results[tweet['tId']]= tweet
        print len(self.results.keys())

    def read_stars(self,filename):
        #Used to read all tweets from the json file
        data = []
        try:
            with open(filename) as f:
                for line in f:
                    data.append(json.loads(line.strip()))
        except:
            print "Failed to read data!"
            return []
        print "The json file has been successfully read!"
        
        for star in data:
            self.stars[star['Screen Name']]= star
        print len(self.stars.keys())

    def outputdata(self):
        output = []
        rank = self.rankStars()
        for i in range(min(10,len(rank))):
            user = rank[i][0]
            for multgeo in self.stars[user]['Geo']:
                if multgeo != None:
                    output.append(([self.stars[user]['Screen Name']], multgeo['coordinates']))
             
        for out in output:
            print out
        with open('outputCS', 'a+') as outfile:
            json.dump(output,outfile)
            outfile.write('\n')

            

if __name__ == "__main__":
    tc = TweetCollector()
    tc.readInput()
    #tc.collectOthersTweets()
    #tc.read_data('ResultsCS')
    #tc.parsingTweeters()
    #tc.parsingMentions()
    tc.read_stars('StarsCS')
    #print tc.stars
        #if(tc.getStarname != ''):
    #tc.geoCounter()
    #print "ranking yo"
    #tc.rankStars()
    tc.outputdata()
