from flask import Blueprint
from scraper import Scraper
# from auth import auth_required

calls = Blueprint('calls', __name__, url_prefix='/api')

@calls.route('/scrapedata', methods=['GET'])
# @auth_required
def scrapedata():
    return Scraper.scrape()