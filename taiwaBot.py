import pathlib
import textwrap
import google.generativeai as genai
import make_voice
import re
from IPython.display import display
from IPython.display import Markdown



def to_markdown(text):
  text = text.replace('(', '  )')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

API_KEY = 'AIzaSyD83xNcxVRtuJWePbPSrjCHswSasyzd7CY' 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

speaker = 1
giri_model = "甘えん坊な彼女みたいに返答して"
speed = 2.0
chat = model.start_chat(history=[])
chat.send_message(giri_model)


def taiwa_change(input_text):
	#input_text = input("入力 >> ")
	response = chat.send_message(input_text)
	make_voice.synthesize_voice(response.text, speaker = speaker,speed = speed, filename="voicevox_output.wav")
	print(response.text)
	return response.text

def text_taiwa(input_text):
	tmpresponse = chat.send_message(input_text.content)
	return re.sub(r'\(.*?\)', '', str(tmpresponse.text))

def question(Q_text):
	response = model.generate_content(Q_text)
	chunks = split_string(response.text)
	return chunks


def split_string(input_string, max_length=2000):
# 文字列をmax_lengthごとに分割   
	return [input_string[i:i+max_length] for i in range(0, len(input_string), max_length)]
