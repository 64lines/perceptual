# Exec:
# $ python bag_of_words.py inputs/positive_words.txt inputs/negative_words.txt
#!/usr/bin/python
import sys
from utils import file_lines_to_list

POSITIVE_WORDS_PATH = "inputs/positive_words.txt"
NEGATIVE_WORDS_PATH = "inputs/negative_words.txt"

# Bag of words models using positive, negative and
# neutral statuses.
class BagOfWordsAnalizer():

    # Analizes the result and asigns the status according
    # to the positive and negative words. 
    def analyze_result(self, result):
        status = ""
        if result["positive"] > result["negative"]:
            status = "positive"
        elif result["positive"] < result["negative"]:
            status = "negative"
        else:
            status = "neutral"
        return status

    def bag_of_words(self, text):
        list_positive_words = file_lines_to_list(POSITIVE_WORDS_PATH)
        list_negative_words = file_lines_to_list(NEGATIVE_WORDS_PATH)

        result = {
            "positive": 0,
            "negative": 0,
            "neutral": 0
        }

        list_words = text.split(" ")
        for word in list_words:
            word = word.lower()
            if word in list_positive_words:
                result["positive"] += 1
            elif word in list_negative_words:
                result["negative"] += 1
            else:
                result["neutral"] += 1
        
        status = self.analyze_result(result)
        return [result, status]

# Looks for emoticons to figure out more quickly the
# sentiment of the tweet.
class EmoticonAnalyzer:
    
    def __init__(self):
        self.dict_emoticon = {
            "positive": [":-P", ";-)", ":-D", ":-)", ":D", ":)", "xD"],
            "negative": [":-||", ":-/", "D-:", ":-(", "D:", ":(", "Dx"]
        }

    def analyze_text(self, text):
        positive_index = 0
        negative_index = 0
        postive_key = "positive"
        negative_key = "negative"
        neutral_key = "neutral"

        for emoticon in self.dict_emoticon[postive_key]:
            if emoticon in text:
                positive_index += 1

        for emoticon in self.dict_emoticon[negative_key]:
            if emoticon in text:
                negative_index += 1
        
        if positive_index > negative_index:
            return postive_key
        elif negative_index > positive_index:
            return negative_key
        elif negative_index == positive_index:
            return neutral_key

def main_exec():
    status = ""
    text = raw_input("Write the text to be analyzed: ")
    model_bow = BagOfWordsAnalizer()
    result, status_bow = model_bow.bag_of_words(text)
     
    model_em = EmoticonAnalyzer()
    status_em = model_em.analyze_text(text)

    print " -> Emoticon Analizer status: [%s]" % status_em
    print " -> Bag of Words Analyzer status: [%s]" % status_bow

    # Chooses the emoticon analyzer as priority to 
    # guess the sentiment of the tweet.
    if status_em == "positive" or status_em == "negative":
        status = status_em
    else:
        status = status_bow
        
    print "\n (*) The text is [%s]\n" % status

if __name__ == "__main__":
    main_exec()
