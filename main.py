from kivy.app import App
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty, BooleanProperty

from kivy.network.urlrequest import UrlRequest

from kivy.uix.carousel import Carousel

import urllib

#import requests

#import json

endpoint = 'http://calwatson.herokuapp.com/question'
my_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Im9za2lfYmVhciIsInBhc3N3b3JkIjoicGFzc3dvcmQ3In0.I8Z0BPvf_9sb9kp19Tek1ZxC50Im1YebB-TE3Oc6Rps'

class Tent(FloatLayout):

    welcome = StringProperty()
    search_term = StringProperty()
    search_sentiment = StringProperty()
    response = StringProperty()
    search = StringProperty()
    search1 = StringProperty()
    search2 = StringProperty()
    s_confidence = StringProperty()
    s1_confidence = StringProperty()
    s2_confidence = StringProperty()

    def query(self, term):

        payload = urllib.urlencode({'question': "{0}".format(term), 'token': my_token})
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}

        r = UrlRequest(endpoint, req_body=payload, req_headers=headers,debug=True)
        r.wait()

        #print(r.result)
        #r = requests.post(endpoint, data=payload)
        try:
            #d = json.loads(r.text)
            d = r.result

            search = d['question']['evidencelist'][0]['text']
            self.s_confidence = d['question']['evidencelist'][0]['value']

            search1 = d['question']['evidencelist'][1]['text']
            self.s1_confidence = d['question']['evidencelist'][1]['value']

            search2 = d['question']['evidencelist'][2]['text']
            self.s2_confidence = d['question']['evidencelist'][2]['value']
        except:
            search = 'Not found'
            search1 = 'Not found'
            search2 = 'Not found'
            

        self.search = ''
        self.search1 = ''
        self.search2 = ''
        j = 0

        chars_per_line = 8

        for i in search.split():

            if j == 40:
                break
            if j % chars_per_line == 0:
                self.search += '\n'
            self.search += i + ' '
            j += 1
        j = 0
        for i in search1.split():

            if j == 40:
                break

            if j % chars_per_line == 0:
                self.search1 += '\n'
            self.search1 += i + ' '
            j += 1


        j = 0
        for i in search2.split():

            if j == 40:
                break

            if j % chars_per_line == 0:
                self.search2 += '\n'
            self.search2 += i  + ' '
            j += 1


        return self.response

class Interface(App):
    def build(self):
        self.Instance = Tent()
        return self.Instance

if __name__ == '__main__':
    Interface().run()

    
