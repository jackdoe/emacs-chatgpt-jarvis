from pyaudio import PyAudio, paInt16
import wave, whisper, os, time
from pynput import keyboard
from chatgpt_wrapper import ChatGPT

LISTEN = False
OUTPUT = "/tmp/jarvis-chatgpt.txt"
RECORDING_FILE = "/tmp/jarvis-chatgpt.wav"
EXTRA_INPUT = "/tmp/jarvis-chatgpt-input.txt"

def on_press(key):
  global LISTEN
  if key ==  keyboard.Key.f12:
    LISTEN = True

def on_release(key):
  global LISTEN
  if key ==  keyboard.Key.f12:
    LISTEN = False

def out(t):
  with open(OUTPUT, "w") as f:
    f.write(t)

def read_extra_file():
  data = ''
  try:
    with open(EXTRA_INPUT, "r") as f:
      data = f.read()
  except:
    pass
  finally:
    os.remove(EXTRA_INPUT)
  return data

def microphone(name, seconds):
  with wave.open(name, 'wb') as wf:
    p = PyAudio()
    wf.setnchannels(1)
    sample = p.get_sample_size(paInt16)
    wf.setsampwidth(sample)
    wf.setframerate(44100)

    stream = p.open(format=paInt16,channels=1,rate=44100,input=True)

    chunks = 44100//1024*seconds
    for _ in range(0, chunks):
      wf.writeframes(stream.read(1024))
      if not LISTEN:
        break

    stream.close()
    p.terminate()

listener = keyboard.Listener(on_press=on_press,on_release=on_release)
listener.start()

bot = ChatGPT()
model = whisper.load_model("medium.en")
out("waiting, pres f12 to ask a question...")
print('...')
while True:
  if LISTEN:
    try:
      out("listening...")
      microphone(RECORDING_FILE, 60)

      out("transcribing...")
      r = model.transcribe(RECORDING_FILE)
    finally:
      os.remove(RECORDING_FILE)

    out(f"decoded: {r['text']}, asking chatgpt...")
    question = r["text"]
    extra = read_extra_file()
    stream  = bot.ask_stream(f"""You are the best software developer in the world, most experienced in go and python, answer the following question:

{question}
{extra}
""")

    response = f"> {question}\n\n"
    for chunk in stream:
      response += chunk
      out(response)

  time.sleep(0.1)
