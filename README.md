care-tags_repmeter
==================

Displays reputation earned on [care-tags.org](http://care-tags.org/index.php)
----
Given a user number (readable off their user page url ("...&u=\<usernumber>")), it displays all reputation that user has received and graphs it, along with showing the user's post with the highest net reputation.

Installation:
-------
1. Download as a zip
2. Extract into directory of choice

Before using:
--------
Make sure to have the following things installed:
* Python 2.7
* Pip (makes the next two way easier to install)
* BeautifulSoup4 (>pip install beautifulsoup4)
* Requests (>pip install requests)

Usage:
------
1. Navigate to the directory you extracted to (make sure to go to the second care-tags_repmeter folder)
2. Run "python main.py -u \<USERNAME> -p \<PASSWORD> -n \<USERNUMBER (to show rep of)>
3. The script will run, albeit a bit slowly. Please be patient with it, it takes longer the more posts/rep you have.

License:
------
MIT License (can pretty much do what you want with this)

If you want to improve this, then by all means go ahead!

Issues/FAQ:
-------
If you have any issues, please message me on care-tags.org, username "rjbman", or feel free to create an issue here. Please make sure the issue isn't resolved in the FAQs.

####Q: Aren't you gonna steal my username and password?
####A: Nope. The code, which I tried to make as readable as possible, just uses that to login to the forum. The data isn't saved at all, or sent anywhere besides care-tags.org to login.
