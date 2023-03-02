# PROOF OF CONCEPT

> I always dreamed of not leaving emacs, with eww and chatgpt I am closer than ever.

This is a proof of concept program that allows you to use voice to interact with chatgpt and see the result in emacs.

To transcribe your speech using OpenAI's Whisper, press the F12 key to start recording. Whisper will continue to transcribe your speech until you release the F12 key. After recording, ask ChatGPT for assistance and print the output in the buffer.

__It stores the recording (up to 60 seconds) in /tmp/jarvis-chatgpt.wav__

Youtube videos showing how it feels:

* using the chatgpt api (instead the headless browser wrapper) to explanin and refactor code:

[![example explain and refactor code](https://img.youtube.com/vi/KX0ZaXcgXNc/0.jpg)](https://www.youtube.com/watch?v=KX0ZaXcgXNc "example explain and refactor")

* asking a question:

[![example question](https://img.youtube.com/vi/P-5RBdM9X-8/0.jpg)](https://www.youtube.com/watch?v=P-5RBdM9X-8 "example question")

* refactor code

[![example refactor](https://img.youtube.com/vi/uWJ8-JU0aXY/0.jpg)](https://www.youtube.com/watch?v=uWJ8-JU0aXY "example refactor")

* rewrite text

[![example rewrite](https://img.youtube.com/vi/4Jyhs6SfFl0/0.jpg)](https://www.youtube.com/watch?v=4Jyhs6SfFl0 "example rewrite")

# Install

The whisper/pyaudio/chatgpt-wrapper are a bit more involved than pip install, whisper needs ffmpeg for example, so its best to follow the instructions on their homepages:

* pip install pynput
* install https://github.com/openai/whisper
* install https://pypi.org/project/PyAudio/ (on windows its just pip install pyaudio)
* install https://github.com/mmabrouk/chatgpt-wrapper or `pip install openai` if you have an api key from openai: https://platform.openai.com/account/api-keys

Edit jarvis.py if you want to use another key

# Running and Using jarvis

* If you have an API key, export it as OPENAI_API_KEY and use `jarvis-chatgpt-api.py` instead of `jarvis.py`
* Run `python jarvis.py` in your terminal. Note that the first time you run it, the `medium.en` model, which is 1.4GB in size, will be downloaded. It may take up to a minute to load the model.
* Open Emacs and navigate to the CHATGPT buffer.
* Press the F12 key to ask a question. If you have a region of text selected, it will be saved to `/tmp/jarvis-chatgpt-input.txt` and appended to your question. For example, if you want to ask Jarvis to "refactor this code", select the code and then press F12.
* If you press F12 for less than a second it will just send the selected region to ChatGPT.

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
  (if (use-region-p)
      (write-region (region-beginning) (region-end) "/tmp/jarvis-chatgpt-input.txt" 0)))
(global-set-key (kbd "<f12>") 'send-selection-to-jarvis)
```

# using jarvis.py outside of emacs

The interface for Jarvis is quite simple: it listens for the F12 keypress, records audio input, transcribes it, and sends the resulting text to the ChatGPT model to get an answer. Additionally, if there is any text in "/tmp/jarvis-chatgpt-input.txt", it will be appended to the question being asked.

The format of the question is as follows:

```
You are the best software developer in the world, most experienced in go and python, answer the following question:

{transcribed question from the microphone}
{data from jarvis-chatgpt-input.txt}
```

The output from ChatGPT is saved to `/tmp/jarvis-chatgpt.txt`, which is overwritten one chunk at a time. You can use inotify to monitor this file and re-read its contents as needed.

# How it looks

![screenshot.png](screenshot.png)

> Dont judge my emacs theme.

# BUGS

Because openai does not have API, chatgpt-wrapper uses the active firefox session via playwright, which is not super reliable, sometimes you might have to restart jarvis.py, so if you can get a key from openai and use `jarvis-chatgpt-api.py`
