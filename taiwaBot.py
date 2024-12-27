import pathlib
import textwrap
import google.generativeai as genai
import voice
from IPython.display import display
from IPython.display import Markdown



def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

API_KEY = 'AIzaSyD83xNcxVRtuJWePbPSrjCHswSasyzd7CY' 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

pre_text = "彼女みたいに返答して"

chat = model.start_chat(history=[])
chat.send_message(pre_text)


def taiwa_change(input_text):
	#input_text = input("入力 >> ")
	response = chat.send_message(input_text)
	voice.synthesize_voice(response.text, speaker=1, filename="voicevox_output.wav")
	print(response.text)
	return response.text

"""
def main():
	while True:
		input_text = input("入力 >> ")
		taiwa_change(input_text)

if __name__ == "__main__":
	main()
"""
