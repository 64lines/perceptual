from word_trainer import generate_models
from word_trainer import format_text

PERCENTAGE_DIFFERENCE_NEUTRALITY = 0.05

def make_analysis(text, positive_metadata, negative_metadata):
    positive_points = 0
    negative_points = 0
    percentage_positive = 0
    percentage_negative = 0
    list_of_words = []

    for word in format_text(text).split(' '):
        find_positive = filter(lambda x: x['word'] == word, positive_metadata)
        find_negative = filter(lambda x: x['word'] == word, negative_metadata)
        if len(find_positive) > 0:
            positive_points += find_positive[0]['weight']
        if len(find_negative) > 0:
            negative_points += find_negative[0]['weight']

    total_points = positive_points + negative_points
    if total_points:
        percentage_positive = float(positive_points) / total_points
        percentage_negative = float(negative_points) / total_points

    print "positive index: %.2f%%" % (percentage_positive * 100)
    print "negative index: %.2f%%" % (percentage_negative * 100)

    if abs(percentage_negative - percentage_positive) < PERCENTAGE_DIFFERENCE_NEUTRALITY:
        return "neutral"
    elif percentage_negative > percentage_positive:
        return "negative"
    elif percentage_negative < percentage_positive:
        return "positive"

def run_analyzer():
    text = raw_input('Write text: ')
    positive_metadata, negative_metadata = generate_models()

    if text == 'p':
        positive_metadata.sort()
        print positive_metadata
        print "Size: %s" % len(positive_metadata)
        return
    elif text == 'n':
        negative_metadata.sort()
        print negative_metadata
        print "Size: %s" % len(negative_metadata)
        return
    elif text.split(' ')[0] == 'find' and len(text.split(' ')) == 2:
        print "positive %s" % filter(lambda x: x['word'] == text.split(' ')[1], positive_metadata)
        print "negative %s" % filter(lambda x: x['word'] == text.split(' ')[1], negative_metadata)
        return

    print make_analysis(text, positive_metadata, negative_metadata)

# run_analyzer()
