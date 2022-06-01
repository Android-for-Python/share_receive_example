# share_receive_example

*Receive shared files or plain text from another app*

Files in [shared storage](https://github.com/Android-for-Python/Android-for-Python-Users#shared-storage) can be shared with other apps. To be usable by Kivy widgets, files must be in [private storage](https://github.com/Android-for-Python/Android-for-Python-Users#private-storage). The methods to copy files between these two types of storage are in the [androidstorage4kivy](https://github.com/Android-for-Python/androidstorgage4kivy/README.me) package.

This example receives video files shared by another app (for example share_send_example) and copies them to private storage. It maintains a queue, and plays the private files using the Kivy VideoPlayer.

There are two other shared storage examples [shared_storage_example](https://github.com/Android-for-Python/shared_storage_example) and [share_send_example](https://github.com/Android-for-Python/share_send_example).
