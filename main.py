#!/usr/bin/env python
# -*- coding: utf-8 -*-#
#-------------------------------------------------------------------------------
# Name:        androidApp.py
# Purpose:     Simple example of a android application skeleton that manages
#              application menu using ActionBar and SidePanelMenu that slides
#              over the main panel
#
# Author:      Licia Leanza
#
# Created:     13-04-2014
# Copyright:   (c) Licia Leanza: 2014
# Licence:     GPL v2
#-------------------------------------------------------------------------------

#--------------------------------------------------------------------------
'''dictionary that contains the correspondance between items descriptions
and methods that actually implement the specific function and panels to be
shown instead of the first main_panel
'''

SidePanel_AppMenu = {'Search':['on_search',None],
                     'voce due':['on_due',None],
                     'voce tre':['on_tre',None],
                     }
id_AppMenu_METHOD = 0
id_AppMenu_PANEL = 1

#--------------------------------------------------------------------------
import kivy
kivy.require('1.8.0')

from kivy.metrics import dp

from kivy.uix.widget import Widget

from kivy.app import App
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.carousel import Carousel
from kivy.properties import StringProperty, NumericProperty, BooleanProperty


from kivy.garden.navigationdrawer import NavigationDrawer
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.actionbar import ActionBar, ActionButton, ActionPrevious
from kivy.properties import  ObjectProperty

from kivy.network.urlrequest import UrlRequest

import urllib


endpoint = 'http://calwatson.herokuapp.com/question'
my_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Im9za2lfYmVhciIsInBhc3N3b3JkIjoicGFzc3dvcmQ3In0.I8Z0BPvf_9sb9kp19Tek1ZxC50Im1YebB-TE3Oc6Rps'

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

#

class AppActionBar(ActionBar):
    ActionBar.background_image = ''
    ActionBar.background_color = (0.364705882,0.637254902,0.823529412,1)


class ActionMenu(ActionPrevious):
    def menu(self):
        print 'ActionMenu'
        RootApp.toggle_sidepanel()

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
    #side_panel_width = dp(200)
    side_panel_init_offset = dp(2)

    def __init__(self, **kwargs):
        super(NavDrawer, self).__init__( **kwargs)
        self.separator_image_width=dp(5)

    def close_sidepanel(self, animate=True):
        if self.state == 'open':
            if animate:
                self.anim_to_state('closed')
            else:
                self.state = 'closed'

class AndroidApp(App):
    #have a reference toscreen manager called mang
    
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

    def login(self, email, password):
        auth_token = ""
        payload = urllib.urlencode({'email': email, 'password': password})
        endpoint = "http://calwatson.herokuapp.com/users/sign_in"
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
        r = UrlRequest(endpoint, req_body=payload, req_headers=headers,debug=True)
        r.wait()
        if r.result == "No user account exists for that customer":
            pass
        elif r.result == "Incorrect password":
            pass
        elif r.result['auth_token'] != None:
            auth_token = r.result['auth_token']
            my_token = auth_token
        else:
            print "Should never get here"
        return auth_token

    def signup(self, email, password):
        payload = urllib.urlencode({'email': email, 'password': password})
        endpoint = "http://calwatson.herokuapp.com/users/sign_up"
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
        r = UrlRequest(endpoint, req_body=payload, req_headers=headers,debug=True)
        r.wait()
        if r.result == "Successful sign up":
            pass
        elif r.result == "That email is already taken.":
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
            pass
            # not able to find auth token
            pass
        return last_queries

    def query(self, term):

        payload = urllib.urlencode({'question': "{0}".format(term), 'token': my_token})
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}

        r = UrlRequest(endpoint, req_body=payload, req_headers=headers,debug=True)
        r.wait()

        try:
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

            self.s_confidence = ''
            self.s2_confidence = ''
            self.s3_confidence = ''

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


    def build(self):

        global RootApp
        RootApp = self

        # NavigationDrawer
        self.navigationdrawer = NavDrawer()
        #self.navigationdrawer.side_panel_width = .2
        #self.navigationdrawer.separator_width = 0

        # SidePanel
        side_panel = SidePanel()
        
        self.navigationdrawer.add_widget( side_panel)

        # MainPanel
        self.main_panel = MainPanel()

        self.navigationdrawer.anim_type = 'slide_above_anim'
        self.navigationdrawer.add_widget(self.main_panel)

        return self.navigationdrawer

    def toggle_sidepanel(self):
        self.navigationdrawer.toggle_state()

    def on_search(self):
        self._switch_main_page('Search', PaginaUno)

    def on_due(self):
        print 'DUE... exec'
        self._switch_main_page('voce due', PaginaDue)
    def on_tre(self):
        print 'TRE... exec'
        self._switch_main_page('voce tre',  PaginaTre)

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
