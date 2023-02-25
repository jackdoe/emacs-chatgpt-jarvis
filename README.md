# PROOF OF CONCEPT

> I always dreamed of not leaving emacs, with eww and chatgpt I am closer than ever.

This is a proof of concept program that allows you to use voice to interact with chatgpt and see the result in emacs.

ress F12 and it will record you (until you release F12) and transcribe the text using openai's whisper, ask chatgpt and print the output in the buffer.

__It stores the recording (up to 60 seconds) in /tmp/jarvis-chatgpt.wav__

Youtube video of how asking a question works:

[![example question](https://img.youtube.com/vi/P-5RBdM9X-8/0.jpg)](https://www.youtube.com/watch?v=P-5RBdM9X-8 "example question")

Youtube video of a refactor code request:

[![example refactor](https://img.youtube.com/vi/uWJ8-JU0aXY/0.jpg)](https://www.youtube.com/watch?v=uWJ8-JU0aXY "example refactor")

# install

* install https://github.com/openai/whisper
* pip install pyaudio pynput
* install https://github.com/mmabrouk/chatgpt-wrapper

Edit jarvis.py if you want to use another key

# running and using

* `python jarvis.py` (first time it has to download the medium.en model which is 1.4gb) and then it takes a minute to load it
* start emacs, and open the CHATGPT buffer
* press F12 to use
* press F11 to copy the current selection into "/tmp/jarvis-chatgpt-input.txt" which will be appended to the question, for example if you want to ask it to "refactor this piece of code" you press F11 to copy the seleciton, and then press F12 to ask the question


Add this to your init.el in order to keep watching the jarvis-chatgpt.txt file:

```
(write-region "" nil "/tmp/jarvis-chatgpt.txt")

(require 'filenotify)
(generate-new-buffer "CHATGPT")

(defun my-jarvis-callback (event)
  (with-current-buffer "CHATGPT"
    (erase-buffer)
    (insert-file-contents "/tmp/jarvis-chatgpt.txt" nil 0 5000)
    (goto-char (point-max))))

(file-notify-add-watch
  "/tmp/jarvis-chatgpt.txt" '(change) 'my-jarvis-callback)

(defun send-selection-to-jarvis ()
  (interactive)
  (write-region (region-beginning) (region-end) "/tmp/jarvis-chatgpt-input.txt" 0))
(global-set-key (kbd "<f11>") 'send-selection-to-jarvis)
```


# How it looks

![screenshot.png](screenshot.png)

> Dont judge my emacs theme.
