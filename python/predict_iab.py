import os
import pickle
from tqdm import tqdm
import torch
from pprint import pprint
from cleantext import clean
from collections import Counter

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

from nltk.stem import WordNetLemmatizer
from sentence_transformers import SentenceTransformer, util

class Predict_IAB:
	def __init__(self, text_file, category = None, data_path = None, text_data_path = None, category_path = None, model_name = None):
		self.data_path = data_path if data_path else '../data/static_category/'
		self.text_data_path = text_data_path if text_data_path else '../data/text/'
		self.category_path = category_path if category_path else '../data/category'
		self.category = 'ryan_category.pkl'
		self.models = [
			'all-mpnet-base-v2', #768
			'bert-base-nli-mean-tokens', #768
			'bert-large-uncased' #1024
		]
		self.model_name = model_name if model_name else self.models[0]

		category_list = pickle.load(open(os.path.join(self.data_path, self.category), 'rb'))
		self.get_custom_stopwords()
		text = self.clean_text(pickle.load(open(os.path.join(self.text_data_path, text_file), 'rb')))

		recurring_n_words = self.get_recurring_n(text, n = 5)
		# print('Top 5 words:')
		# pprint(recurring_n_words)
		mapping = self.score_mapping(recurring_n_words, category_list, self.model_name)
		self.save_mapping(mapping, text_file, self.category_path)

	def get_custom_stopwords(self):
		with open('stop_words.pkl', 'rb') as file:
			self.custom_stopwords = pickle.load(file)
		file.close()

	def clean_text(self, text_dict):
		stop = stopwords.words('english')
		lemmatizer = WordNetLemmatizer()
		text = text_dict['text'].replace('[^A-Za-z0-9 ]+', ' ')
		text = clean(text, clean_all = False, 
						   extra_spaces = True, 
						   stemming = False,
						   stopwords = True, 
						   lowercase = True, 
						   numbers = True, 
						   punct = True
					)
		text = ' '.join([word for word in text.split() if word not in (stop)])
		text = ' '.join([word for word in text.split() if word not in (self.custom_stopwords)])
		text = ' '.join([lemmatizer.lemmatize(word) for word in text.split()])
		return text

	def get_recurring_n(self, text, n = 5):
		return Counter(text.split()).most_common(n)

	def score_mapping(self, recurring_n_words, category_list, model_name):
		mapping = dict()
		model = SentenceTransformer(model_name)
		embs_word = torch.zeros(len(recurring_n_words), 768)
		embs_category = torch.zeros(len(category_list), 768)

		for i, word in enumerate(tqdm(recurring_n_words)):
			word = word[0].lower()
			embedding_word = model.encode(word, convert_to_tensor = True)
			embs_word[i] = embedding_word

		if (os.path.isfile(os.path.join(self.data_path, 'category_list_embedding.pkl'))):
			embs_category = pickle.load(open(os.path.join(self.data_path, 'category_list_embedding.pkl'),'rb'))
		else:
			for i, category in enumerate(tqdm(category_list)):
				category = category[1].lower()
				embedding_category = model.encode(category, convert_to_tensor = True)
				embs_category[i] = embedding_category

			with open(os.path.join(self.data_path, 'category_list_embedding.pkl'), 'wb') as file: 
				pickle.dump(embs_category, file)

		scores, indices = torch.max(util.cos_sim(embs_word, embs_category), dim = -1)

		for i, idx in enumerate(indices):
			mapping[recurring_n_words[i][0]] = {
				'id': category_list[idx][0],
	 		    'data': recurring_n_words[i][0],
	 		    'table': category_list[idx][1],
	 		    'score': scores[i].item(),
	 		    'count': recurring_n_words[i][1]
			}
		return mapping

	def save_mapping(self, mapping, mapping_file, category_path):
		with open(os.path.join(category_path, mapping_file), 'wb') as file: 
			pickle.dump(mapping, file) 
		print('Category mapping saved at:', os.path.join(category_path, mapping_file))
