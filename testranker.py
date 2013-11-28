import math
import json

class TestRanker():
    def __init__(self):

        self.stars = {}
        
    #Strictly for testing - stars dict is populated by parsingTweeters and Parsing Mentions
    def TestData(self):
        self.stars["David"] = {}
        self.stars["David"]['Follower Count']= 35000
        self.stars["David"]['Mention Count'] = 2
        self.stars["David"]['Verified']= True
        self.stars["David"]['Geo']= "30.627977,-96.334407"
        self.stars["David"]['Direct Star'] = True
        
        self.stars["Christine"] = {}
        self.stars["Christine"]['Follower Count']= 100000
        self.stars["Christine"]['Mention Count'] = 12
        self.stars["Christine"]['Verified']= False
        self.stars["Christine"]['Geo']= 'null'
        self.stars["Christine"]['Direct Star'] = False
        
        self.stars["Keleigh"] = {}
        self.stars["Keleigh"]['Follower Count']= 21583
        self.stars["Keleigh"]['Mention Count'] = 6
        self.stars["Keleigh"]['Verified']= False
        self.stars["Keleigh"]['Geo']= "30.627977,-96.334407"
        self.stars["Keleigh"]['Direct Star'] = False
        
        self.stars["James"] = {}
        self.stars["James"]['Follower Count']= 1000470
        self.stars["James"]['Mention Count'] = 60
        self.stars["James"]['Verified']= True
        self.stars["James"]['Geo']= 'null'
        self.stars["James"]['Direct Star'] = True
        
        
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
                                
if __name__ == "__main__":
    tr = TestRanker()
    tr.TestData()
    tr.rankStars()

