# -*- coding: utf-8 -*-#
import kivy
import random
import time
#kivy.require('1.8.0')

from kivy.metrics import dp

from kivy.uix.widget import Widget

from kivy.app import App
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.carousel import Carousel
from kivy.properties import StringProperty, NumericProperty, BooleanProperty,ListProperty

#from navigationdrawer import * 
#from kivy.garden.navigationdrawer import NavigationDrawer
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import  ObjectProperty

#from kivy.network.urlrequest import UrlRequest
#import urllib
# patent dictionary
from patents import *

#endpoint = 'http://calwatson.herokuapp.com/question'
#my_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Im9za2lfYmVhciIsInBhc3N3b3JkIjoicGFzc3dvcmQ3In0.I8Z0BPvf_9sb9kp19Tek1ZxC50Im1YebB-TE3Oc6Rps'

#RootApp = None

class Fox(FloatLayout):
    #have a reference toscreen manager called mang
    patent_traits =set(documents.keys())

    navbar_label = StringProperty()
    logged_in = False

    login_text = StringProperty()

    patent_matches = NumericProperty()
    
    welcome = StringProperty()
    search_term = StringProperty()
    search_sentiment = StringProperty()

    my_token = StringProperty()

    response = StringProperty()

    search0 = StringProperty()
    search1 = StringProperty()
    search2 = StringProperty()
    search3 = StringProperty()
    search4 = StringProperty()

    search_titl0 = StringProperty()
    search_titl1 = StringProperty()
    search_titl2 = StringProperty()
    search_titl3 = StringProperty()
    search_titl4 = StringProperty()

    s_confidence = StringProperty()
    s1_confidence = StringProperty()
    s2_confidence = StringProperty()

    local_result = ListProperty()
    local_search_term = ListProperty()
    confidence = NumericProperty()

    def login(self, email, password):
        time.sleep(.75)
        auth_token = ""
        #payload = urllib.urlencode({'email': email, 'password': password})
        endpoint = "http://calwatson.herokuapp.com/users/sign_in"
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
        #r = UrlRequest(endpoint, req_body=payload, req_headers=headers,debug=True)
        #r.wait()

        if True:
            self.navbar_label = "Logged in as " + email
            self.login_text = 'Welcome!'
            self.my_token = "tokentoek" #r.result['auth_token']
            self.logged_in = True
            self.manager.current = 'analysis'
            #change Screen!
        else:
            print "Should never get here"
        return auth_token

    def signup(self, email, password):
        payload = urllib.urlencode({'email': email, 'password': password})
        #endpoint = "http://calwatson.herokuapp.com/users/sign_up"
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
        #r = UrlRequest(endpoint, req_body=payload, req_headers=headers,debug=True)
        r.wait()
        if r.result == "Successful sign up":
            self.login_text = 'Welcome!'
            self.login(email,password)

        elif r.result == "That email is already taken.":
            self.login_text = r.result
            pass
        else:
            print "Should never get here"
        return

    def get_last_five_queries(self, token):
        payload = urllib.urlencode({'token': token})
        endpoint = "http://calwatson.herokuapp.com/users/last_requests"
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
        r = UrlRequest(endpoint, req_body=payload, req_headers=headers,debug=True)
        r.wait()

        try:
            last_queries = r.result['answers']
        except:
            # not able to find auth token
            pass
        return last_queries

    def local_query(self,term):
        time.sleep(.5)
        amount_found = 0
        results = [documents[word] for word in self.patent_traits if word in term]
        self.patent_matches = len(results)
        if self.patent_matches < 6:
            #extremely precise patent measure based on machine learning and big-data
            self.confidence = 100 * (0.6 + .25*(1 - abs((1.0/(6-(self.patent_matches))))))
        else:
            self.confidence = 0.73
        i =  5 - self.patent_matches
        if i >0:
            while i >0:
                rando = random.choice(list(documents.values()))
                if rando not in results:
                    results.append(rando)
                    i-=1

        self.search_titl0 = "US" + str(random.randint(3,9)) + str(random.randint(0,10)) + str(random.randint(0,10))+ str(random.randint(0,10))+ str(random.randint(0,10))+ str(random.randint(0,10))+ str(random.randint(0,10))

        self.search_titl1 = "US" + str(random.randint(3,9)) + str(random.randint(0,10)) + str(random.randint(0,10))+ str(random.randint(0,10))+ str(random.randint(0,10))+ str(random.randint(0,10))+ str(random.randint(0,10))


        self.search_titl2 = "US" + str(random.randint(3,9)) + str(random.randint(0,10)) + str(random.randint(0,10))+ str(random.randint(0,10))+ str(random.randint(0,10))+ str(random.randint(0,10))+ str(random.randint(0,10))


        self.search_titl3 = "US" + str(random.randint(3,9)) + str(random.randint(0,10)) + str(random.randint(0,10))+ str(random.randint(0,10))+ str(random.randint(0,10))+ str(random.randint(0,10))+ str(random.randint(0,10))


        self.search_titl4 = "US" + str(random.randint(3,9)) + str(random.randint(0,10)) + str(random.randint(0,10))+ str(random.randint(0,10))+ str(random.randint(0,10))+ str(random.randint(0,10))+ str(random.randint(0,10))

        self.search0 = results[0]
        self.search1 = results[1]
        self.search2 = results[2]
        self.search3 = results[3]
        self.search4 = results[4]
        return results

class AndroidApp(App):
    def build(self):
        self.Instance = Fox()
        return self.Instance

if __name__ == '__main__':
    AndroidApp().run()
