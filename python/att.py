import os
import time
import pickle
import whisper

import warnings
warnings.filterwarnings('ignore')

class Audio_To_Text:
	def __init__(self, audio_data_path = None, text_data_path = None, model_type = 'tiny.en'):
		self.audio_data_path = audio_data_path if audio_data_path else '../data/audio/'
		self.text_data_path = text_data_path if text_data_path else '../data/text/'
		self.model_types = ['tiny.en', 'tiny', 'small', 'base', 'medium', 'large']
		
		# if (not os.path.isfile(os.path.join(self.audio_data_path, audio_file))):
		# 	print('Audio file does not exist. Please check again')
		# 	return None
		# if (model_type not in self.model_types):
		# 	print('Model does not exist. Please check again')
		# 	return None

		
		self.model = whisper.load_model(model_type)
		# text = self.transcribe(audio_file)
		# self.save_text(text, audio_file.split('.')[0] + '.pkl')

	def transcribe(self, audio_file, model = 'tiny.en'):
		return self.model.transcribe(os.path.join(self.audio_data_path, audio_file))

	def save_text(self, text, text_file):
		with open(os.path.join(self.text_data_path, text_file), 'wb') as file: 
			pickle.dump(text, file)
		print('Transcribed text saved at:', os.path.join(self.text_data_path, text_file))
		return text_file
