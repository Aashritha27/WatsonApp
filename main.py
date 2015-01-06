#!/usr/bin/env python
# -*- coding: utf-8 -*-#
#--------------------------------------------------------------------------
#dictionary mapping side panel IDs to a list of functions that get called on click
SidePanel_AppMenu = {
                     'Search':  ['on_search',None],
                     'Search History': ['on_history',None],
                     'Saved Searches':['on_saved',None],
                     'Settings':['on_settings',None],
                     }
id_AppMenu_METHOD = 0
id_AppMenu_PANEL = 1
#--------------------------------------------------------------------------
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

from kivy.garden.navigationdrawer import NavigationDrawer
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.actionbar import ActionBar, ActionButton, ActionPrevious
from kivy.properties import  ObjectProperty

#from kivy.network.urlrequest import UrlRequest

#import urllib
# patent dictionary
from patents import *

#endpoint = 'http://calwatson.herokuapp.com/question'
#my_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Im9za2lfYmVhciIsInBhc3N3b3JkIjoicGFzc3dvcmQ3In0.I8Z0BPvf_9sb9kp19Tek1ZxC50Im1YebB-TE3Oc6Rps'

RootApp = None

class SidePanel(BoxLayout):
    pass

class MenuItem(Button):
    background_normal = ''
    background_color=  (0.364705882,0.637254902,0.823529412,1)
    def __init__(self, **kwargs):
        super(MenuItem, self).__init__( **kwargs)
        self.bind(on_press=self.menuitem_selected)

    def menuitem_selected(self, *args):
        print self.text, SidePanel_AppMenu[self.text], SidePanel_AppMenu[self.text][id_AppMenu_METHOD]
        try:
            function_to_call = SidePanel_AppMenu[self.text][id_AppMenu_METHOD]
        except:
            print 'error in menu item calling!'
            return
        getattr(RootApp, function_to_call)()

class AppActionBar(ActionBar):
    ActionBar.background_image = ''
    #ActionBar.background_color = (0.364705882,0.637254902,0.823529412,1)
    ActionBar.background_color= (0.8784313725490196, 0.4196078431372549, 0.14901960784313725,1)

class ActionMenu(ActionPrevious):
    def menu(self):
        pass
        """
        if RootApp.logged_in:
            RootApp.toggle_sidepanel()
        else:
            RootApp.login_text = "Please login to continue." 
        """

class ActionQuit(ActionButton):
    pass
    def menu(self):
        print 'App quit'
        RootApp.stop()


class MainPanel(BoxLayout):
    pass

class AppArea(FloatLayout):
    pass

class PaginaUno(FloatLayout):
    pass

class PaginaDue(FloatLayout):
    pass

class PaginaTre(FloatLayout):
    pass


class AppButton(Button):
    nome_bottone = ObjectProperty(None)
    def app_pushed(self):
        print self.text, 'button', self.nome_bottone.state

class NavDrawer(NavigationDrawer):
    #this is a dirty way to change panel width
    #only way to do it for now
    side_panel_init_offset = dp(2)
    
    def __init__(self, **kwargs):
        super(NavDrawer, self).__init__( **kwargs)
        self.separator_image = 'assets/navigationdrawer_gradient_ltor.png'
        self.separator_image_width=dp(5)

    def close_sidepanel(self, animate=True):
        if self.state == 'open':
            if animate:
                self.anim_to_state('closed')
            else:
                self.state = 'closed'

class AndroidApp(App):
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

        print results
        print(len(results))
        return results

    def query(self, term):
        payload = urllib.urlencode({'question': "{0}".format(term), 'token': self.my_token})
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
        r = UrlRequest(endpoint, req_body=payload, req_headers=headers,debug=True)
        r.wait()
        print r.result

        try:
            d = r.result

            search0 = d['question']['evidencelist'][0]['text']
            self.s_confidence = d['question']['evidencelist'][0]['value']

            search1 = d['question']['evidencelist'][1]['text']
            self.s1_confidence = d['question']['evidencelist'][1]['value']

            search2 = d['question']['evidencelist'][2]['text']
            self.s2_confidence = d['question']['evidencelist'][2]['value']
        except:
            search0 = 'Not found'
            search1 = 'Not found'
            search2 = 'Not found'

            self.s_confidence = ''
            self.s2_confidence = ''
            self.s3_confidence = ''

        self.search0 = ''
        self.search1 = ''
        self.search2 = ''
        j = 0

        chars_per_line = 8
                                
        for i in search0.split():

            if j == 40:
                break
            if j % chars_per_line == 0:
                self.search0 += '\n'
                pass
            self.search0 += i + ' '
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


    def build(self):
        global RootApp
        RootApp = self
        # NavigationDrawer
        self.navigationdrawer = NavDrawer()
        #self.navigationdrawer.side_panel_width = .2

        # SidePanel
        side_panel = SidePanel()
        
        self.navigationdrawer.add_widget( side_panel)
        self.navigationdrawer.logged_in = False

        # MainPanel
        self.main_panel = MainPanel()

        self.navigationdrawer.anim_type = 'slide_above_anim'
        self.navigationdrawer.add_widget(self.main_panel)

        self.navbar_label = 'Tent'

        return self.navigationdrawer

    def toggle_sidepanel(self):
        self.navigationdrawer.toggle_state()

    def on_saved(self):
        self.navigationdrawer.close_sidepanel()
        if self.logged_in != True:
            self.login_text = 'Please login before continuing.'
        else:
            self.manager.current = 'saved_searches'
        #switch to saved
    def on_history(self):

        self.navigationdrawer.close_sidepanel()
        if self.logged_in != True:
            self.login_text = 'Please login before continuing.'
        else:
            self.manager.current = 'search_history'

    def on_settings(self):
        self.navigationdrawer.close_sidepanel()
        if self.logged_in != True:
            self.login_text = 'Please login before continuing.'
        else:
            self.manager.current = 'settings'

    def on_search(self):
        print('why??')
        self.navigationdrawer.close_sidepanel()
        print('why!?')
        if self.logged_in != True:
            self.login_text = 'Please login before continuing.'
        else:
            self.manager.current = 'analysis'

    def _switch_main_page(self, key,  panel):
        self.navigationdrawer.close_sidepanel()
        if not SidePanel_AppMenu[key][id_AppMenu_PANEL]:
            SidePanel_AppMenu[key][id_AppMenu_PANEL] = panel()
        main_panel = SidePanel_AppMenu[key][id_AppMenu_PANEL]
        self.navigationdrawer.remove_widget(self.main_panel)    # FACCIO REMOVE ED ADD perchè la set_main_panel
        self.navigationdrawer.add_widget(main_panel)            # dà un'eccezione e non ho capito perchè
        self.main_panel = main_panel

if __name__ == '__main__':
    AndroidApp().run()
