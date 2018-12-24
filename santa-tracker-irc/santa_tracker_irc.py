# santa-tracker-irc
# Scrapes Google to track Santa and spits out his location on IRC.

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import pydle


location = ""
url = 'https://www.google.com/search?q=santa+tracker'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
headers = {'User-Agent': user_agent}


def simple_get(url):
    try:
        with closing(get(url, headers=headers, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def get_location():
    global location
    """
    Downloads the page where the list of mathematicians is found
    and returns a list of strings, one per mathematician
    """
    response = simple_get(url)

    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        location = html.find("div", {"class":"vk_h PU8lJc"})
        print("Hohoho! Santa is currently located at " + location.text +"! Merry Christmas!")


    # Raise an exception if we failed to get any data from the url
#    raise Exception('Error retrieving contents at {}'.format(url))


if __name__ == '__main__':
    get_location()