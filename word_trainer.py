# -*- coding: latin-1 -*-
positive_metadata = []
negative_metadata = []

def get_reviews(file_name):
    file_data = open(file_name, 'r+')
    list_reviews = file_data.readlines()
    file_data.close()
    return list_reviews

def save_metadata(file_name, metadata):
    file_metadata = open(file_name, 'w+')
    for word_object in metadata:
        file_metadata.write("%s|%s\n" % (word_object['word'], word_object['weight']))
    file_metadata.close()

def format_text(text):
    return text.lower().strip() \
        .replace('.', '. ') \
        .replace(',', ', ') \
        .replace('  ', ' ') \
        .replace('.', '') \
        .replace(',', '') \
        .replace('!', '') \
        .replace('?', '') \
        .replace('¿', '') \
        .replace('¡', '') \
        .replace('(', '') \
        .replace(')', '') \

def generate_model_metadata(file_name):
    list_reviews = get_reviews(file_name)
    big_data_list = []

    # Setting the words up
    for review in list_reviews:
        for word in format_text(review).split(' '):
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

def generate_models():
    # Model with the positive/negative words already analized and
    # weighted using the files training files especified.
    print "Generating positive and negative trained data..."

    # Trained model with positive training data
    file_positive_metadata = 'positive_metadata.txt'
    positive_metadata = generate_model_metadata('spanish_positive_reviews.txt')
    save_metadata(file_positive_metadata, positive_metadata)
    print "%s was generated." % file_positive_metadata

    # Trained model with negative training data
    file_negative_metadata = 'negative_metadata.txt'
    negative_metadata = generate_model_metadata('spanish_negative_reviews.txt')
    save_metadata('negative_metadata.txt', negative_metadata)
    print "%s was generated." % file_negative_metadata
    return positive_metadata, negative_metadata

