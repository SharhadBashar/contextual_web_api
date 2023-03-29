import os
import pickle
from tqdm import tqdm
from pprint import pprint
from cleantext import clean
from collections import Counter

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

from nltk.stem import WordNetLemmatizer
from sentence_transformers import SentenceTransformer, util

class Predict_IAB:
	def __init__(self, text_file, category = None, text_data_path = None, category_path = None, model_name = None):
		self.text_data_path = text_data_path if text_data_path else '../data/text/'
		self.category_path = category_path if category_path else '../data/category'
		self.category = 'ryan_category.pkl'
		self.model_name = model_name if model_name else 'all-mpnet-base-v2'

		category_list = pickle.load(open(os.path.join(self.category_path, self.category), 'rb'))
		self.get_custom_stopwords()
		text = self.clean_text(pickle.load(open(os.path.join(self.text_data_path, text_file), 'rb')))

		recurring_n_words = self.get_recurring_n(text, n = 5)
		print('Top 5 words:')
		pprint(recurring_n_words)
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
		print(text)
		input()
		text = ' '.join([lemmatizer.lemmatize(word) for word in text.split()])
		return text

	def get_recurring_n(self, text, n = 5):
		return Counter(text.split()).most_common(n)

	def score_mapping(self, recurring_n_words, category_list, model_name):
		model = SentenceTransformer(model_name)
		mapping = {}
		for word, count in tqdm(recurring_n_words):
			word = word.lower()
			mapping[word] = {
			    'id': -1,
			    'data': word,
			    'table': '',
			    'score': 0,
			    'count': count
			}
			embedding_word = model.encode(word, convert_to_tensor = True)
			for id, category in category_list:
				category = category.lower()
				embedding_category = model.encode(category, convert_to_tensor = True)
				cosine_score = round((util.cos_sim(embedding_word, embedding_category)).item(), 2)
				if (cosine_score > mapping[word]['score']):
					mapping[word]['id'] = id
					mapping[word]['score'] = cosine_score
					mapping[word]['table'] = category
		return mapping

	def save_mapping(self, mapping, mapping_file, category_path):
		print('Categories:')
		pprint(mapping)
		with open(os.path.join(category_path, mapping_file), 'wb') as file: 
			pickle.dump(mapping, file) 
		print('Category mapping saved at:', os.path.join(category_path, mapping_file))
		

