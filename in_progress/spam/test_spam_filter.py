"""Tests for EmailClassifier"""

import spam_filter

HAM = """Jeff,
I think your book is terrible and, by extension, you
are terrible.

Kindly,
Anonymous"""

SPAM = """Dear Sir,
You Have alredy one a FREE trip to tropical I-land!!!! Kindly open the file and
fill owt your info and male me it.

Sincerely,
Anonymous, Director of Prize Distribution
"""

def test_parse_email():
    """Test that a single email is parsed correctly"""
    classifier = spam_filter.EmailClassifier()
    assert len(classifier._parse_message(HAM)) == 15
