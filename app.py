# Exec:
# $ python perceptual.py inputs/example_tweets.txt
#!/usr/bin/python
from analysis.analysis import OpinionMiningAnalyzer
from files.files import FileManager
from settings import USE_DB

class PerceptualApp():
    EXAMPLE_TWEETS_PATH = "inputs/example_tweets.txt"

    def calculate_perception(self):
        if USE_DB:
            manager = PostManager()
        else:
            manager = FileManager(self.EXAMPLE_TWEETS_PATH)
        
        analyzer = OpinionMiningAnalyzer()
        analyzer.list_entries = manager.get_entries()
        analyzer.analyize_entries() # Making analysis
        self.show_results(analyzer.analysis_result)
    
    def show_results(self, analysis_result):
        print "\nAnalysis:\n"
        print " (*) Analysis Result:"
        for key in analysis_result.keys():
            print "  (+) %s: %s" % (key, analysis_result[key])

if __name__ == "__main__":
    app = PerceptualApp()
    app.calculate_perception()
