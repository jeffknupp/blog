class EmailClassifier(object):
    """Manage learning from and classification of email messages"""

    def __init__(self):
        pass

    def parse_message(self, message):
        """Return a list containing every word found in message"""
        pass

    def process_classified_message(self, message, classification):
        """Update our internal data store to reflect the information obtained
        from message with given classification.""" 
        pass

    def classify_message(self, message):
        pass

    def save(self):
        pass

    def load(self):
        pass
