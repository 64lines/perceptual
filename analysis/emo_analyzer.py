# Looks for emoticons to figure out more quickly the
# sentiment of the tweet.
class EmoticonAnalyzer():
    DICT_EMOTICONS = {
        "positive": [
            ":-)", ":)", ":d", ":o)", ":]", ":3", ":c)",
            ":>", "=]", "8)", "=)", ":}", ":^)", ":-d",
            "8-d", "8d", "x-d", "xd", "x-d", "xd", "=-d",
            "=d", "=-3", "=3", "b^d", ":-))", ":'-)",
            ":')", ";-)", ";)", "*-)", "*)", ";-]", ";]",
            ";d", ";^)", ":-,", ":p"
        ],
        "negative": [
            ":-||", ":-/", "d-:", ":-(", "d:", ":(", "dx",
            ">:[", ":-(", ":(", ":-c", ":c", ":-<", ":<",
            ":-[", ":[", ":{", ";(", ":-||", ":@", ">:(",
            ":'-(", ":'(", ">:o", ":-o", ":o", ":-o", ":o",
            "8-0", "o_o", "o-o", "o_o", "o_o", "o_o", "o-o"
        ]
    }

    def analyze_text(self, text):
        positive_index = 0
        negative_index = 0
        result = ""

        for emoticon in self.DICT_EMOTICONS["positive"]:
            if emoticon in text:
                positive_index += 1

        for emoticon in self.DICT_EMOTICONS["negative"]:
            if emoticon in text:
                negative_index += 1

        if positive_index > negative_index:
            result = "positive"
        elif negative_index > positive_index:
            result = "negative"
        elif negative_index == positive_index:
            result = "neutral"

        return result