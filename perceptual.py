# Exec:
# $ python perceptual.py inputs/example_tweets.txt
#!/usr/bin/python
import sys
from utils import get_file_lines
from models import OpinionMiningAnalyzer

def main_exec():
    analyzer = OpinionMiningAnalyzer()
    analyzer.list_entries = get_file_lines(sys.argv[1])
    analyzer.analyize_entries() # Making analysis

    print "\nAnalysis:\n"
    print " - Analysis Result: %s" % analyzer.analysis_result

if __name__ == "__main__":
    main_exec()
