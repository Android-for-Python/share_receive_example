from android import mActivity,autoclass,activity
from threading import Thread
from androidstorage4kivy import SharedStorage
from kivy.clock import mainthread


Intent = autoclass('android.content.Intent')

# Source https://github.com/Android-for-Python/share_receive_example

'''
   NOTE: intent_filter.xml and intent_handler() must be customized 
         according to the file types handled by the app.
         The intent_filter tells Android what data types this app can handle

   READ:
   https://developer.android.com/training/sharing/receive#handling-content

   The intent filter for this example ( ./intent_filter.xml ) contains:

    <intent-filter>
        <action android:name="android.intent.action.SEND" />
        <category android:name="android.intent.category.DEFAULT" />
        <data android:mimeType="text/plain" />
    </intent-filter>
    <intent-filter>
        <action android:name="android.intent.action.SEND" />
        <category android:name="android.intent.category.DEFAULT" />
        <data android:mimeType="video/mp4" />
    </intent-filter>
    <intent-filter>
        <action android:name="android.intent.action.SEND_MULTIPLE" />
        <category android:name="android.intent.category.DEFAULT" />
        <data android:mimeType="video/mp4" />
    </intent-filter>
'''


class ShareListener():

    def __init__(self, text_callback=None, video_callback=None):              
        self.text_callback=text_callback
        self.video_callback=video_callback
        self.intent = mActivity.getIntent()
        self.intent_handler(self.intent)
        activity.bind(on_new_intent=self.intent_handler)

    @mainthread
    def video_callback_on_mainthread(self, file_path, MIME_type):
        self.video_callback(file_path,MIME_type)

    @mainthread
    def text_callback_on_mainthread(self, file_path, MIME_type):
        self.text_callback(file_path,MIME_type)

    def copy_to_private_file(self, uri, MIME_type):
        try:
            if self.text_callback:
                self.text_callback_on_mainthread('Copying file...',
                                                 'text/plain')
            file_path = SharedStorage().copy_from_shared(uri)
            if self.text_callback:
                self.text_callback_on_mainthread('Copied to private storage',
                                                 'text/plain')
            self.video_callback_on_mainthread(file_path, MIME_type)
        except Exception as e:
            print('ShareListener.copy_to_private_file() ' + str(e))

    def copy_to_private_files(self, uris, MIME_type):
        try:
            for i in range(uris.size()):
                uri = uris.get(i)
                self.copy_to_private_file( uri, MIME_type)
        except Exception as e:
            print('ShareListener.copy_to_private_files() ' + str(e))

    def intent_handler(self, intent):
        action = intent.getAction()
        if Intent.ACTION_SEND == action:
            MIME_type = intent.getType()
            if MIME_type == "text/plain":
                text = intent.getStringExtra(Intent.EXTRA_TEXT)
                if text and self.text_callback:
                    self.text_callback(text,MIME_type)
            elif MIME_type == "video/mp4":
                uri = intent.getParcelableExtra(Intent.EXTRA_STREAM)
                if uri and self.video_callback:
                    Thread(target=self.copy_to_private_file,
                           args=[uri,MIME_type], daemon=True).start()
        elif Intent.ACTION_SEND_MULTIPLE == action:
            MIME_type = intent.getType()
            if MIME_type == "video/mp4":
                uris = intent.getParcelableArrayListExtra(Intent.EXTRA_STREAM)
                if uris.size() and self.video_callback:
                    Thread(target=self.copy_to_private_files,
                           args=[uris, MIME_type], daemon=True).start()
