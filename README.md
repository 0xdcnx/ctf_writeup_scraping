# ctf_writeup_scraping
The goal of this project is to create a scipt that scrappes and lists all the available CTF challenges/wargames in a website, and also lists the available writeups for a given challenge.

Currently only lists challenges in overthewire.org
Working on listing available levels for each challenge. 

Current usage: python main.py otw
Prints a list of wargame challenges in overthewire.org


Future usage: python main.py otw [challenge] [level]
Without mentioning the optional arguments [challenge] and [level], prints a list of wargame challenges in overthewire.org
If only [challenge] is passed, lists all the available levels for that challenge.
If [challenge] and [level] are passed, details for that level are printed.
