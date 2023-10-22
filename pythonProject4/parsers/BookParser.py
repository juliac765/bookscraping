import logging
import re
import logger
from locators.book_locators import BookLocators

logger = logging.getLogger('scraping.books_parser')
class BookParser:
    """
    a class to take in a html page (or part of it) and return properties of
    an item in it

    """

    RATINGS = { 'One' : 1,
                'Two' : 2,
                'Three' : 3,
                'Four' : 4,
                'Five': 5

    }
    def __init__(self, parent):
        logger.debug(f'New book found in `{parent}`.')
        self.parent = parent


    def __repr__(self):
        return f'< Book {self.name}, £{self.price}, with {self.rating} stars>'
    @property
    def name(self):
        locator = BookLocators.NAME_LOCATOR
        logger.debug('Finding book name...')
        item_link = self.parent.select_one(locator)
        item_name = item_link.attrs['title']
        logger.debug(f'Found book title `{item_name}` .')
        return item_name

    @property
    def link(self):
        locator = BookLocators.LINK_LOCATOR
        logger.debug('Finding book link...')
        item_link = self.parent.attrs['href']
        return item_link


    @property
    def price(self):
        locator = BookLocators.PRICE_LOCATOR
        logger.debug('Finding book price...')
        item_price = self.parent.select_one(locator).string  # £51.77

        pattern = '£([0-9]+\.[0-9]+)'
        matcher = re.search(pattern, item_price)
        return float(matcher.group(1))    #51.77


    @property
    def rating(self):
        locator = BookLocators.RATING_LOCATOR
        logger.debug('Finding book rating...')
        star_rating_tag = self.parent.select_one(locator)
        classes = star_rating_tag.attrs['class']   #['star-rating', 'three']
        rating_classes = [r for r in classes if r != 'star-rating']
        rating_number = BookParser.RATINGS.get(rating_classes[0])  #returns None if not found
        return rating_number



