from topmembers import TopMembers
from topposts import TopPosts
import time

starttime = time.time()

topmembers = TopMembers("PythonBot", "autonomous")
topposts = TopPosts("PythonBot", "autonomous")

repped = topmembers.mostreppedusers()
posters = topmembers.gettopposters()
rep_per = topmembers.most_rep_per_post_users(10)
posts = topposts.gettopposts(10)
waywts = topposts.gettopwaywt(10)


print "[size=200]Top 10 Posts (non-WAYWT)[/size]"
print "[spoiler][b]" + "Poster" + " - Reputation[/b]"
print "[list=1]"
for post in posts:
    print "[*][url=" + post[0] + "]" + "By " + post[1] + " - [b]" + str(post[2]) + "[/b]" + "[/url][/*]"
print "[/list][/spoiler]"
print " "

print "[size=200]Top 10 WAYWT Posts[/size]"
print "[spoiler][b]" + "Poster" + " - Reputation[/b]"
print "[list=1]"
for post in waywts:
    print "[*][url=" + post[0] + "]" + "By " + post[1] + " - [b]" + str(post[2]) + "[/b]" + "[/url][/*]"
print "[/list][/spoiler]"
print " "

print "[size=200]Top 10 Members (post count)[/size]"
print "[spoiler][b]" + "User" + " - Post Count[/b]"
print "[list=1]"
for user in posters:
    print "[*]" + user[0] + " - [b]" + str(user[1]) + "[/b]" + "[/*]"
print "[/list][/spoiler]"
print " "

print "[size=200]Top 10 Members (reputation)[/size]"
print "[spoiler][b]" + "User" + " - Reputation[/b]"
print "[list=1]"
for user in repped:
    print "[*]" + user[0] + " - [b]" + str(user[1]) + "[/b]" + "[/*]"
print "[/list][/spoiler]"
print " "

print "[size=200]Top 10 Members (rep per post)[/size]"
print "[spoiler][b]" + "User" + " - Reputation Per Post[/b]"
print "[list=1]"
for user in rep_per:
    print "[*]" + user[0] + " - [b]" + "{0:.2f}".format(user[1]) + "[/b]" + "[/*]"
print "[/list][/spoiler]"

print time.time() - starttime  #


# Desired output:
# [size=200]Top 10 Members (post count)[/size]
# [list=1][*]bela 1427[/*]
# [*]cameron- 1382[/*]
# [*]Syeknom 1254[/*]
# [*]germinal 838[/*]
# [*]starfox64 774[/*]
# [*]sknss 666[/*]
# [*]ramseames 511[/*]
# [*]RycePooding 478[/*]
# [*]smiles 434[/*]
# [*]Bobbin.Threadbare 416[/*]
# [/list]
#
# [size=200]Top 10 Members (reputation)[/size]
# [list=1]
# [*]cameron- 2352[/*]
# [*]bela 1711[/*]
# [*]Syeknom 1646[/*]
# [*]germinal 1427[/*]
# [*]smiles 1271[/*]
# [*]sknss 1151[/*]
# [*]Bobbin.Threadbare 1138[/*]
# [*]maj 994[/*]
# [*]odradek 943[/*]
# [*]kyung 938[/*]
# [/list]
#
# [size=200]Top 10 Posts (reputation)[/size]
# [list=1]
# [*](u'http://care-tags.org/viewtopic.php?f=2&t=8&start=1320#p16270', u'matrimonioids', 61)[/*]
# [*](u'http://care-tags.org/viewtopic.php?f=3&t=413&start=0#p15225', u'odradek', 57)[/*]
# [*](u'http://care-tags.org/viewtopic.php?f=2&t=8&start=1080#p13654', u'hmwut', 56)[/*]
# [*](u'http://care-tags.org/viewtopic.php?f=3&t=413&start=0#p14883', u'maj', 56)[/*]
# [*](u'http://care-tags.org/viewtopic.php?f=2&t=8&start=1020#p13251', u'agvs', 55)[/*]
# [*](u'http://care-tags.org/viewtopic.php?f=2&t=8&start=1230#p15156', u'Rosenrot', 55)[/*]
# [*](u'http://care-tags.org/viewtopic.php?f=3&t=413&start=30#p15472', u'verilyvert', 54)[/*]
# [*](u'http://care-tags.org/viewtopic.php?f=2&t=8&start=1440#p18102', u'Rosenrot', 53)[/*]
# [*](u'http://care-tags.org/viewtopic.php?f=2&t=8&start=1260#p15588', u'Bobbin.Threadbare', 52)[/*]
# [*](u'http://care-tags.org/viewtopic.php?f=3&t=413&start=30#p15533', u'prawnzee', 51)[/*]
# [/list]