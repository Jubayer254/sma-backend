import logging

class IgnoreBrokenPipeFilter(logging.Filter):
    def filter(self, record):
        return 'Broken pipe' not in str(record.getMessage())
