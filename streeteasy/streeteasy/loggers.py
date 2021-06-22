"""Add option to suppress log statements about logged items
From https://gitlab.com/mshepherd/scrapy-extensions/-/blob/master/scrapy_extensions/loggers.py
"""
from scrapy.logformatter import LogFormatter


class QuietLogFormatter(LogFormatter):
    """Be quieter about scraped items."""

    def scraped(self, item, response, spider):
        return (
            super().scraped(item, response, spider)
            if spider.settings.getbool("LOG_SCRAPED_ITEMS")
            else None
        )
