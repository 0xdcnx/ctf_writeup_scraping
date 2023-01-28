# ctf_writeup_scraping
The goal of this project is to create a scipt that scrappes and lists the available CTF challenges/wargames in a website, and also lists the available writeups for a selected challenge.

Currently only lists challenges in overthewire.org, and I'm currently working on listing available levels for each challenge so that later, the user can search for writeups for each level.

Current usage: <br>
`python main.py otw`

Prints a list of wargame challenges in overthewire.org


Future usage: <br>
`python main.py otw [challenge] [level]`

Without mentioning the optional arguments [challenge] and [level], prints a list of wargame challenges in overthewire.org.

If only [challenge] is passed, lists all the available levels for that challenge.

If [challenge] and [level] are passed, details for that level are printed.


## Jan 28th update log:
Added initial functionality to list levels for each challenge Using Selenium.
Since BS4 works with static responses, had to use Selenium for pages with JavaScript rendered data - ie the levels for OTW challenges. 


Current usage: <br>
`python main.py otw [challenge]`

**TODO:**
- Selenium uses page object design pattern. I need to better understand how/why use it;
- Ex: Create separation between the page(s) being loaded and the elements being used.