from topmembers import TopMembers
from topposts import TopPosts
import time


def posts_to_bbcode(title, head1, head2, posts, output):
    output.write("[size=200]" + str(title) + "[/size]\n")
    output.write("[spoiler][b]" + str(head1) + " - " + str(head2) + "[/b]\n")
    output.write("[list=1]\n")
    for post in posts:
        output.write("[*][url=" + post[0] + "]" + "By " + post[1] + " - [b]" + str(post[2]) + "[/b]" + "[/url][/*]\n")
    output.write("[/list][/spoiler]\n\n")


def members_to_bbcode(title, head1, head2, members, output):
    output.write("[size=200]" + str(title) + "[/size]\n")
    output.write("[spoiler][b]" + str(head1) + " - " + str(head2) + "[/b]\n")
    output.write("[list=1]\n")
    for member in members:
        output.write("[*]" + member[0] + " - [b]" + str(member[1]) + "[/b]" + "[/*]\n")
    output.write("[/list][/spoiler]\n\n")


starttime = time.time()

topmembers = TopMembers("PythonBot", "autonomous")
topposts = TopPosts("PythonBot", "autonomous")

repped = topmembers.mostreppedusers(10)
posters = topmembers.gettopposters(10)
rep_per = topmembers.most_rep_per_post_users(10)
posts = topposts.gettopposts(10)
waywts = topposts.gettopwaywt(10)

with open("topposts_output.txt", "a") as f:
    f.write("Current date & time " + time.strftime("%c") + "\n")
    posts_to_bbcode("Top 10 Posts (non-WAYWT)", "Poster", "Reputation", posts, f)
    posts_to_bbcode("Top 10 WAYWT Posts", "Poster", "Reputation", waywts, f)
    members_to_bbcode("Top 10 Members (post count)", "User", "Post Count", posters, f)
    members_to_bbcode("Top 10 Members (reputation)", "User", "Reputation", repped, f)
    members_to_bbcode("Top 10 Members (rep per post)", "User", "Reputation Per Post", rep_per, f)

    f.write("\nRuntime: " + str(time.time() - starttime) + "\n")  #