from utils.utils import Formatter

PERCENTAGE_DIFFERENCE_NEUTRALITY = 0.05

formatter = Formatter()

class MachineLearningAnalyzer():
    def __init__(self):
        self.positive_metadata = []
        self.negative_metadata = []

    def make_analysis(self, text):
        result_polarity = ""
        positive_points = 0
        negative_points = 0
        percentage_positive = 0
        percentage_negative = 0
        
        list_of_words = formatter.format_text(text).split(' ')
        
        for word in list_of_words:
            find_positive = filter(lambda x: x['word'] == word, self.positive_metadata)
            find_negative = filter(lambda x: x['word'] == word, self.negative_metadata)
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
            result_polarity = "neutral"
        elif percentage_negative > percentage_positive:
            result_polarity = "negative"
        elif percentage_negative < percentage_positive:
            result_polarity = "positive"
        
        return result_polarity
