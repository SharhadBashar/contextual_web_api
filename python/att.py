import os
import torch
import pickle
import whisper

from constants import *
from logger import Logger
from helper import json_response_message

import warnings
warnings.filterwarnings('ignore')

class Audio_To_Text_EN:
	def __init__(self, audio_data_path = None, text_data_path = None, model_type = 'tiny.en'):
		self.language = 'english'
		self.audio_data_path = audio_data_path if audio_data_path else PATH_DATA_AUDIO
		self.text_data_path = text_data_path if text_data_path else PATH_DATA_TEXT
		
		if (model_type not in WHISPER_MODEL_TYPES):
			return json_response_message(422, ERROR_WHISPER_MODEL.format(model_type), language = 'english')
		
		DEVICE = 'cuda:0' if torch.cuda.is_available() else 'cpu'

		self.model = whisper.load_model(model_type, device = DEVICE)

	def transcribe(self, audio_file, show_id, episode_id, language = 'english'):
		try:
			return self.model.transcribe(os.path.join(self.audio_data_path, audio_file))
		except Exception as error:
			return json_response_message(422, ERROR_TRANSCRIBE.format(episode_id, error), show_id, episode_id, language)

	def save_text(self, text, text_file, show_id, episode_id, language = 'english'):
		try:
			with open(os.path.join(self.text_data_path, text_file), 'wb') as file: 
				pickle.dump(text, file)
			Logger(201, LOG_TYPE['i'], TRANSCRIBE_SAVE.format(episode_id, os.path.join(self.text_data_path, text_file)), show_id, episode_id, language)
			return text_file
		except Exception as error:
			return json_response_message(422, ERROR_SAVE_TEXT.format(episode_id, error), show_id, episode_id, language)

class Audio_To_Text_FR:
	def __init__(self, audio_data_path = None, text_data_path = None, model_type = 'tiny'):
		self.language = 'french'
		self.audio_data_path = audio_data_path if audio_data_path else PATH_DATA_AUDIO
		self.text_data_path = text_data_path if text_data_path else PATH_DATA_TEXT
		
		if (model_type not in WHISPER_MODEL_TYPES):
			return json_response_message(422, ERROR_WHISPER_MODEL.format(model_type), language = 'french')
		
		self.model = whisper.load_model(model_type)

	def transcribe(self, audio_file, show_id, episode_id, language = 'french'):
		try:
			return self.model.transcribe(os.path.join(self.audio_data_path, audio_file))
		except Exception as error:
			return json_response_message(422, ERROR_TRANSCRIBE.format(episode_id, error), show_id, episode_id, language)

	def save_text(self, text, text_file, show_id, episode_id, language = 'french'):
		try:
			with open(os.path.join(self.text_data_path, text_file), 'wb') as file: 
				pickle.dump(text, file)
			Logger(201, LOG_TYPE['i'], TRANSCRIBE_SAVE.format(episode_id, os.path.join(self.text_data_path, text_file)), show_id, episode_id, language)
			return text_file
		except Exception as error:
			return json_response_message(422, ERROR_SAVE_TEXT.format(episode_id, error), show_id, episode_id, language)
