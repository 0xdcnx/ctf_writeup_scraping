from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import requests
import sys


class Content:
    def __init__(self, url, header, challenges: list):
        self.url = url
        # self.title = title
        self.header = header
        self.challenges = challenges  # See how to improve

    def get_obj(self) -> dict:
        return {self.header: self.challenges}


def get_soup(url: str):
    """ 
    Returns BeautifulSoup object from a given url only if status code is 200 and no Exceptions are thrown
    Otherwise returns None
    """
    try:
        request = requests.get(url)
        if request.status_code != 200:
            return None
    except requests.exceptions.RequestException as ex:
        print(ex.strerror())
        return None
    return BeautifulSoup(request.text, "lxml")

def get_webdriver(url, keyword):
    """
    Returns a Selenium webdriver from a given url 
    Checks if @param keyword is in title. If not, returns None
    """
    try:
        """
        Setting Options.add_argument to use '--headless' maskes it so that no browser window is loaded when runnung Selenium
        """
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        assert keyword.lower() in driver.title.lower(), f'The webdriver was not created because {keyword} was not found in the title. This may or may not be a problem with the url {url}.'
        return driver
        
    except AssertionError as msg:
        print(msg)
        return None


def usage():
    print(f"Usage: python {sys.argv[0]} otw [challenge] [level]\n")
    print("- Without mentioning the optional arguments [challenge] and [level], prints a list of wargame challenges in overthewire.org.\n")
    print("- If only [challenge] is passed, lists all the available levels for that challenge.\n")
    print("- If [challenge] and [level] are passed, details for that level are printed.")


def get_overthetwire_challenges(url) -> dict:
    """
    Function that returns a dict of challenges organized by categories for overthewire.org
    key = Challenge category
    value = list of challenges organized as dicts
    
    Returns None if errors were found when creating a BeautifulSoup object
    """
    soup = get_soup(url)
    if soup is not None:
        target = soup.find("div", id="sidemenu").find_all("ul")
        obj = {}
        for ul in target:
            header = ul.li.sh.text
            challenges = ul.find_all("a", class_="updatedmarkercontainer")
            challenges_ = [challenge.text.strip() for challenge in challenges]
            links = [challenge["href"] for challenge in challenges]

            """
            Creates a list of dictionaries. Each dict has the challenge name and the link
            """
            challenges_and_links = [
                dict({"name": c, "link": url.replace("/wargames/", l)})
                for c, l in zip(challenges_, links)
            ]

            content = Content(url, header, challenges_and_links)
            obj.update(content.get_obj())
        return obj
    else:
        print("Unable to get a response...\nCheck the link...")
        return None


def otw():
    url = "https://overthewire.org/wargames/"
    otw = get_overthetwire_challenges(url)
    print(f"Listing challenges for {url}...\n")
    for category, challenges in otw.items():
        print(f"{category} challenges:\n--------------------")
        for index, challenge in enumerate(challenges):
            print(f"{index+1}. {challenge['name']}")
        print('')



def get_challenge_link(challenge_name) -> str:
    return_url = None
    url = "https://overthewire.org/wargames/"
    otw = get_overthetwire_challenges(url)
    print(f"Searching for challenge...")
    for challenges in otw.values():
        for challenge in challenges:
            if(challenge['name'].lower() == challenge_name.lower()):
                return_url = challenge['link']
                return return_url

    return None

def list_levels(url, challenge) -> None:
    # soup = get_soup(url)
    driver = get_webdriver(url, challenge)
    if driver is not None:
        # sidemenu = soup.find("div", id="sshinfo")
        # info = sidemenu.find_all('div', id='sshinfo')
        sidemenu = driver.find_element(By.ID, 'sidemenu')
        # print(sidemenu.get_attribute('ul'))
        print(sidemenu.text)
    else:
        print("There was problem parsing the link...sorry")

if __name__ == "__main__":

    """
    Currently only works with overthewire.org (otw argument)
    Need to update code to allow other challenge websites
    """
    match (len(sys.argv)):
        case 1: usage()
            
        case 2: 
            if sys.argv[1] != 'otw':
                usage()
            else:
                otw()
        case 3: 
            if sys.argv[1] != 'otw':
                usage()
            else:
                url = get_challenge_link(sys.argv[2])
                if url == None:
                    print(f"Challenge [{sys.argv[2]}] not found...try executing again without [challenge] to see the available challenges.")
                else:
                    print(f"Challenge [{sys.argv[2]}] found!")
                    print("Loading levels. Please wait...")
                    list_levels(url, sys.argv[2])
        case 4: pass
    

