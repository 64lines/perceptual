# -*- coding: latin-1 -*-
from utils.utils import Formatter
formatter = Formatter()

class MachineLearningTrainer():
    POSITIVE_REVIEWS_PATH = 'resources/spanish_positive_reviews.txt'
    NEGATIVE_REVIEWS_PATH = 'resources/spanish_negative_reviews.txt'
    POSITIVE_METADATA_PATH = 'metadata/positive_metadata.txt'
    NEGATIVE_METADATA_PATH = 'metadata/negative_metadata.txt'

    def __init__(self):
        self.positive_metadata = []
        self.negative_metadata = []
        
    def get_reviews(self, file_name):
        file_data = open(file_name, 'r+')
        list_reviews = file_data.readlines()
        file_data.close()
        return list_reviews

    def save_metadata(self, file_name, metadata):
        file_metadata = open(file_name, 'w+')
        sorted(metadata, key=lambda x: x['weight'], reverse=True)        
        for word_object in metadata:
            file_metadata.write("%s|%s\n" % (word_object['word'], word_object['weight']))
        file_metadata.close()

    def generate_model_metadata(self, file_name):
        list_reviews = self.get_reviews(file_name)
        big_data_list = []

        # Setting the words up
        for review in list_reviews:
            for word in formatter.format_text(review).split(' '):
                is_new = True

                for i in range(0, len(big_data_list)):
                    if big_data_list[i]['word'] == word:
                        is_new = False
                        big_data_list[i]['weight'] += 1

                if is_new:
                    word_model = {'word':'', 'weight': 1}
                    word_model['word'] = word
                    if word_model not in big_data_list:
                        big_data_list.append(word_model)

        return big_data_list
    
    def generate_metadata(self, metadata_path, reviews):
        metadata = self.generate_model_metadata(reviews)
        self.save_metadata(metadata_path, metadata)
        print "%s was generated." % metadata_path
        return metadata

    def train_models(self):
        """
        Model with the positive/negative words already analized and
        weighted using the files training files especified.
        """
        print "Generating positive and negative trained data..."

        self.positive_metadata = self.generate_metadata(self.POSITIVE_METADATA_PATH, 
            self.POSITIVE_REVIEWS_PATH)
        self.negative_metadata = self.generate_metadata(self.NEGATIVE_METADATA_PATH, 
            self.NEGATIVE_REVIEWS_PATH)

