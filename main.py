from bs4 import BeautifulSoup
import requests

# -------------------- TODOS------------------------
# TODO #1 Create functions that parse content for each challenge website
# TODO #2 Create datamodel class for CTF challenge content (CTF website, challenge name, category, points, the writeup, and solution/flag)
# TODO #3 Create get_links() function to retrieve google links for writeups
# TODO #4 Read chapter 3 from https://github.com/REMitchell/python-scraping (getNextLink)
# getNextLink - from chapter 3 - return random link on a page
# TODO #5 Review documentation
# TODO #6 Create deadlines
# TODO #7 Improve datamodel class definition. Create another layer of abstractio / or add more fields to reflect collected data
# #


class Content:
    def __init__(self, url, header, challenges):
        self.url = url
        # self.title = title
        self.header = header
        self.challenges = challenges  # See how to improve

    def get_obj(self):
        return {self.header: self.challenges}


def get_soup(url):
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


def get_overthetwire_challenges(url) -> dict:
    """
    Function that returns a dict of challenges organized by categories for overthewire.org
    key = Challenge category
    value = list of challenges
    
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
            content = Content(url, header, challenges_)

            obj.update(content.get_obj())
            # for index, challenge in enumerate(challenges):
            #     challenge_name = challenge.text.strip()
            #     print(f"- {challenge_name}")

        return obj
    else:
        print("Unable to get a response...\nCheck the link...")
        return None


if __name__ == "__main__":
    url = "https://overthewire.org/wargames/"

    otw = get_overthetwire_challenges(url)
    print(otw)
