import os
import time
import pickle
import whisper

from constants import *

import warnings
warnings.filterwarnings('ignore')

class Audio_To_Text:
	def __init__(self, audio_data_path = None, text_data_path = None, model_type = 'tiny.en'):
		self.audio_data_path = audio_data_path if audio_data_path else PATH_DATA_AUDIO
		self.text_data_path = text_data_path if text_data_path else PATH_DATA_TEXT
		
		if (model_type not in WHISPER_MODEL_TYPES):
			print('Model not found. Please re check')
			quit()
		
		self.model = whisper.load_model(model_type)

	def transcribe(self, audio_file):
		return self.model.transcribe(os.path.join(self.audio_data_path, audio_file))

	def save_text(self, text, text_file):
		with open(os.path.join(self.text_data_path, text_file), 'wb') as file: 
			pickle.dump(text, file)
		print('Transcribed text saved at:', os.path.join(self.text_data_path, text_file))
		return text_file
