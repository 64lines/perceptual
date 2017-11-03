#!/usr/bin/python
# -*- coding: latin-1 -*-

from machine_learning.ml_trainer import MachineLearningTrainer
from machine_learning.ml_analyzer import MachineLearningAnalyzer
from emo_analyzer import EmoticonAnalyzer
from post.post import PostManager
from utils.utils import Formatter
from settings import USE_DB

formatter = Formatter()

class OpinionMiningAnalyzer:
    def __init__(self):
        self.positive_metadata = []
        self.negative_metadata = []

        # List of entries to evaluate
        self.list_entries = []

        # Analysis result, this should be checked after the analysis has been made.
        self.analysis_result = {
            "positive": 0, 
            "negative": 0, 
            "neutral": 0
        }

    def analyize_entries(self):
        self.train_ml_models()

        for entry in self.list_entries:
            if USE_DB:
                text = entry.post_text
            else:
                text = entry

            text = formatter.format_text(text)
            polarity = self.make_analysis(text)
            print "[%s] - %s " % (polarity, text)

            if USE_DB:
                manager = PostManager()
                manager.add_analysis_record(entry.id, polarity)

    def train_ml_models(self):
        ml_trainer = MachineLearningTrainer()
        ml_trainer.train_models()
        self.positive_metadata = ml_trainer.positive_metadata
        self.negative_metadata = ml_trainer.negative_metadata

    def get_emoticon_analysis(self, text):
        # Emoticon Analysis
        emo_analyzer = EmoticonAnalyzer()
        emo_result = emo_analyzer.analyze_text(text)
        return emo_result

    def get_machine_learning_analysis(self, text):
        ml_analyzer = MachineLearningAnalyzer()
        ml_analyzer.positive_metadata = self.positive_metadata
        ml_analyzer.negative_metadata = self.negative_metadata
        ml_result = ml_analyzer.make_analysis(text)
        return ml_result

    # Make general analysis of all the texts evaluated.
    def make_analysis(self, text):
        emo_result = self.get_emoticon_analysis(text)
        ml_result = self.get_machine_learning_analysis(text)

        result = ""
        if emo_result is not 'neutral':
            self.analysis_result[emo_result] += 1
            result = emo_result
        else:
            self.analysis_result[ml_result] += 1
            result = ml_result

        return result