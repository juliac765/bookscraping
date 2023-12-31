import re
import logging
from bs4 import BeautifulSoup
from locators.all_books_page import AllBooksPageLocators
from parsers.BookParser import BookParser

logger = logging.getLogger('scraping.all_books_page')

class AllBooksPage:
    def __init__(self, page_content):
        logger.debug('Parsing page content with BeautifulSoup...')
        self.soup = BeautifulSoup(page_content, 'html.parser')

    @property
    def books(self):
        logger.debug(f'Finding all books using `{AllBooksPageLocators.BOOKS}`")
        return [BookParser(e) for e in self.soup.select(AllBooksPageLocators.BOOKS)]

    @property
    def page_count(self):
        logger.debug('Finding number of catalogue pages available...')
        content = self.soup.select_one(AllBooksPageLocators.PAGER).string
        pattern = 'Page [0-9]+ of ([0-9]+)'
        matcher = re.search(pattern, content)
        pages = int(matcher.group(1))
        logger.debug(f'Extracted number of pages as integer: {pages} . ')
        return pages
