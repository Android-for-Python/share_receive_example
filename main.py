# Example of receiving an Android Share of .mp4 file or plain text.

# This is a workaround for SDL2 crashes
import os
os.environ["SDL_AUDIODRIVER"] = "android"

from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.label import Label
from shutil import rmtree
from android import mActivity
from os.path import exists
from os import remove
from functools import partial

from sharelistener import ShareListener
from android_permissions import AndroidPermissions
from androidstorage4kivy import SharedStorage

################################################################
# Known issues, these are unrelated to demonstrating receiving a share.
#
# 1) Kivy VideoPlayer sometimes crashes when playing a sequence
# of videos, though each video plays if it is the first in the squenece.
# https://github.com/matham/ffpyplayer/issues/128
#
# 2) The ffpylayer package (not the uix widget of the same name)
# does not rotate Android portrait videos
# https://github.com/matham/ffpyplayer/issues/127
################################################################

# Source https://github.com/Android-for-Python/share_receive_example

class ShareReceiveExample(App):

    def build(self):
        # cleanup if Android didn't
        temp = SharedStorage().get_cache_dir()
        if temp and exists(temp):
            rmtree(temp)
        self.label = Label(text='Share some text or video with me')
        self.video = VideoPlayer(options={'allow_stretch':True})
        self.video.state = 'stop'
        self.video.bind(state = self.next_video)
        self.now_playing = None
        self.video_que = []
        box = BoxLayout(orientation='vertical')
        box.add_widget(self.video)
        box.add_widget(self.label)
        return box

    ### Permissions

    def on_start(self):
        self.dont_gc = AndroidPermissions(self.start_app)
        
    ### Start listener

    def start_app(self):
        self.dont_gc = None    
        self.share_listener = ShareListener(text_callback=self.new_text,
                                            video_callback=self.new_video)

    ### User event
    
    def quit_app(self,window,key,*args):
        # back button/gesture quits app
        if key == 27:
            mActivity.finishAndRemoveTask() 
            return True   
        else:
            return False

    ### Listener events
        
    def new_text(self, text, MIMEtype):
        self.label.text  = text

    def new_video(self, source, MIMEtype):
        if self.video.state == 'stop':
            self.play_video(source, MIMEtype, 0)
        else:
            self.video_que.append([source, MIMEtype])

    ### Actions
        
    def play_video(self, source, MIMEtype, dt):
        self.video.source = source
        self.video.state  = 'play'
        if self.now_playing and exists(self.now_playing):
            remove(self.now_playing)
        self.now_playing = source

    def next_video(self, id, state):
        if state == 'stop' and self.video_que:
            source, MIMEtype = self.video_que[0]
            self.video_que = self.video_que[1:]
            Clock.schedule_once(partial(self.play_video, source, MIMEtype))

    ### Lifecycle events
    
    def on_pause(self):
        self.resume_state = self.video.state
        if self.video.state  == 'play':
            self.video.state  = 'pause'
        return True

    def on_resume(self):
        if self.resume_state == 'play':
            self.video.state = 'play'

ShareReceiveExample().run()


