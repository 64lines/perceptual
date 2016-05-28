# Exec:
# $ python perceptual.py inputs/example_tweets.txt
#!/usr/bin/python
import sys
from utils import get_file_lines
from models import OpinionMiningAnalyzer
from models import DatabaseConnection

def main_exec():
    db_connection = DatabaseConnection()
    analyzer = OpinionMiningAnalyzer()
    analyzer.list_entries = db_connection.get_post_entries()
    analyzer.analyize_entries() # Making analysis

    print "\nAnalysis:\n"
    print " - Analysis Result: %s" % analyzer.analysis_result

if __name__ == "__main__":
    main_exec()
