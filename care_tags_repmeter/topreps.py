from bs4 import BeautifulSoup
from collections import defaultdict
from operator import itemgetter
from repreader import RepReader
import urllib
import urllib2
import cookielib
import re
import time
import requests
import sys
import itertools


#Lists the top ten users by rep given
class TopRepGivers(RepReader):

	def __init__(self, username, password):
		RepReader.__init__(self, username, password)

	def __get_user_numbers(self,tags):
		numbers = []
		for tag in tags:
			link = tag.find("a").get('href')
			if link:
				result = re.match('(.*)(viewprofile\&u\=)(\d*)', link.decode('utf-8'), re.I | re.U)
				if result:
					numbers.append(str(result.group(3)))
		return numbers


	def get_member_list(self):
		#Initial variables
		pages = []		
		username = self.username
		password = self.password
		website = "http://care-tags.org/ucp.php?mode=login"


		#Login with provided credentials
		sess = self.session
		payload = {"username":username, "password":password,
				"autologin":"on", "login":"login"}


		#Visit memberlist page
		response = sess.post(website, data=payload)
		response = sess.get("http://care-tags.org/memberlist.php")
		
		bs = BeautifulSoup(response.text)
                
		#pull total number of current users from 'rightsight pagination' class
                member_list_rightside = bs.find('li',{'class':'rightside pagination'})
                member_list_rightside_match = re.match('(\d*)(.*)', member_list_rightside.text.strip())
                total_user_count = int(member_list_rightside_match.group(1))


		current_user_count = 0
		#iterate through all pages of member list
		while current_user_count < total_user_count:

			currentpage = "http://care-tags.org/memberlist.php?start=" + str(current_user_count)
			response = sess.get(currentpage)
			pages.append(response.text)
			current_user_count +=25 #25 members listed per page

		return pages


	def scrape_user_numbers(self):
		total_numbers = []
		bg1_numbers = []
		bg2_numbers = []	

		member_list_pages = self.get_member_list()
		for page in member_list_pages:
			#Make soup, pull user numbers
			bs = BeautifulSoup(page)
			bg1_numbers += self.__get_user_numbers(bs.find_all('tr',{'class':'bg1'}))
			bg2_numbers += self.__get_user_numbers(bs.find_all('tr',{'class':'bg2'}))
		return bg1_numbers + bg2_numbers

	def calculate_top_x(self, num):
		top_ten = []
		results = []
		rep_given = defaultdict(lambda : 0)
		numbers = self.scrape_user_numbers()
		pos = 1
		for number in numbers:
			print "Progress: user number " + str(number) + ". " + str(pos) + " of " + str(len(numbers))
			pos+=1
			results = self.receivedrep(number)
			for result in results: 
				rep_given[result[0]] += result[1]
		sorted_rep_given = sorted(rep_given.items(), key=itemgetter(1), reverse=True)
		counter = 0
		for item in sorted_rep_given:
			top_ten.append((item[0],item[1]))
			if( len(top_ten) == num): #num 2-tuples
				break
		return top_ten

		
	

if __name__ == "__main__":
	from optparse import OptionParser
	import sys

	parser = OptionParser()

	usage = "Usage: %prog -u <USERNAME> -p <PASSWORD>"
	parser = OptionParser(usage)

	parser.add_option(
		"-u",
		"--username",
		dest="user",
		help="Needs a username to login with",
		default=None
	)

	parser.add_option(
		"-p",
		"--password",
		dest="pw",
		help="Need the password to login user",
		default=None
	)

	(options, args) = parser.parse_args()
	test = TopRepGivers(options.user, options.pw)
	mylist = test.calculate_top_x(10)
	for item in mylist:
		print item[0] + " " + str(item[1])
