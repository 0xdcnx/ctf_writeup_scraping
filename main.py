from bs4 import BeautifulSoup
import requests


class Content:
    def __init__(self, url, header, challenges: list):
        self.url = url
        # self.title = title
        self.header = header
        self.challenges = challenges  # See how to improve

    def get_obj(self) -> dict:
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


if __name__ == "__main__":
    url = "https://overthewire.org/wargames/"

    otw = get_overthetwire_challenges(url)
    print(otw)
