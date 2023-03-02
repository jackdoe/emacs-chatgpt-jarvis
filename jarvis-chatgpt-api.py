import openai
from pyaudio import PyAudio, paInt16
import wave, whisper, os, time
from pynput import keyboard
import traceback
LISTEN = False
OUTPUT = "/tmp/jarvis-chatgpt.txt"
RECORDING_FILE = "/tmp/jarvis-chatgpt.wav"
EXTRA_INPUT = "/tmp/jarvis-chatgpt-input.txt"
openai.api_key = os.getenv("OPENAI_API_KEY")

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
    try:
      os.remove(EXTRA_INPUT)
    except:
      pass
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

model = whisper.load_model("medium.en")
out("waiting, pres f12 to ask a question, region selection will be appended...")
print('...')
while True:
  if LISTEN:
    question = ''
    try:
      out("listening...")
      t0 = time.time()
      microphone(RECORDING_FILE, 60)
      if time.time() - t0 > 1:
        out("transcribing...")
        r = model.transcribe(RECORDING_FILE)
        question = r["text"]
      else:
        question = ''
    finally:
      try:
        os.remove(RECORDING_FILE)
      except:
        pass
    extra = read_extra_file()
    out(f"decoded: {question}\n{extra}\nasking chatgpt...")

    chatgpt_request = f"{question}\n{extra}"

    try:
      completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[
          {"role": "system", "content": "You are the best software developer in the world, most experienced in go and python, answer the following question:"},
          {"role": "user", "content": chatgpt_request}
        ]
      )

      response = f"# QUESTION:\n{question}\n{extra}\n# CHATGPT START\n"
      response += completion.choices[0].message.content
      response += '\n# CHATGPT END\n'
      out(response)
    except Exception as e:
      exception_stack = traceback.format_exc()
      out(f"Error: {str(e)}\n\n{exception_stack}")

  time.sleep(0.01)
