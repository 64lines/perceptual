# Exec:
# $ python perceptual.py inputs/example_tweets.txt
#!/usr/bin/python
import sys
from utils import get_file_lines
from models import OpinionMiningAnalyzer
from models import PostManager
from models import FileManager
from settings import USE_DB

def main_exec():
    if USE_DB:
        manager = PostManager()
    else:
        manager = FileManager("inputs/negative_tweets.txt")

    analyzer = OpinionMiningAnalyzer()
    analyzer.list_entries = manager.get_entries()
    analyzer.analyize_entries() # Making analysis

    print "\nAnalysis:\n"
    print " - Analysis Result: %s" % analyzer.analysis_result

if __name__ == "__main__":
    main_exec()
