from topmembers import TopMembers
from topposts import TopPosts
import time


def posts_to_bbcode(title, head1, head2, posts):
    print "[size=200]", title, "[/size]"
    print "[spoiler][b]", head1, "-",  head2, "[/b]"
    print "[list=1]"
    for post in posts:
        print "[*][url=" + post[0] + "]" + "By " + post[1] + " - [b]" + str(post[2]) + "[/b]" + "[/url][/*]"
    print "[/list][/spoiler]"
    print " "


def members_to_bbcode(title, head1, head2, members):
    print "[size=200]", title, "[/size]"
    print "[spoiler][b]", head1, "-",  head2, "[/b]"
    print "[list=1]"
    for member in members:
        print "[*]" + member[0] + " - [b]" + str(member[1]) + "[/b]" + "[/*]"
    print "[/list][/spoiler]"
    print " "


starttime = time.time()

topmembers = TopMembers("PythonBot", "autonomous")
topposts = TopPosts("PythonBot", "autonomous")

repped = topmembers.mostreppedusers()
posters = topmembers.gettopposters()
rep_per = topmembers.most_rep_per_post_users(10)
posts = topposts.gettopposts(10)
waywts = topposts.gettopwaywt(10)

posts_to_bbcode("Top 10 Posts (non-WAYWT)", "Poster", "Reputation", posts)

posts_to_bbcode("Top 10 WAYWT Posts", "Poster", "Reputation", waywts)

members_to_bbcode("Top 10 Members (post count)", "User", "Post Count", posters)

members_to_bbcode("Top 10 Members (reputation)", "User", "Reputation", repped)

members_to_bbcode("Top 10 Members (rep per post)", "User", "Reputation Per Post", rep_per)

print time.time() - starttime  #