from bs4 import BeautifulSoup
import requests

## TODOS
# TODO #1 Create functions that parse content for each challenge website
# TODO #2 Create datamodel class
# TODO #3 Create get_links() function to retrieve google links for writeups
# TODO #4 Read chapter 3 from https://github.com/REMitchell/python-scraping (getNextLink)
# getNextLink - from chapter 3 - return random link on a page
# TODO #5 Review documentation
# TODO #6 Create deadlines
#


if __name__ == "__main__":
    request = requests.get("https://overthewire.org/wargames/")

    # Program exits if response code is not 200
    if request.status_code != 200:
        print("Unable to get a response...\nExiting...")
        exit

    soup = BeautifulSoup(request.text, "lxml")

    # Gets a single ul -> convert to get all 3 uls
    # taget stores all ul parent elements that contain the target info
    target = soup.find("div", id="sidemenu").find_all("ul")
    for ul in target:
        header = ul.li.sh.text
        print(f"--------------------\n{header} challenges:")
        challenges = ul.find_all("a", class_="updatedmarkercontainer")
        for challenge in challenges:
            challenge_name = challenge.text.strip()
            print(f"- {challenge_name}")
