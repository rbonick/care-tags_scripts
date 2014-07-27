# -*- coding: utf-8 -*-

from datetime import datetime

from caretags_utils import CaretagsUtils


__author__ = 'Ryan'


class PostUtils:

    def __init__(self):
        self.util = CaretagsUtils()
        util.login_from_file()

    def get_posts_from_url(self, url):
        """
        Gets posts from a single page of a thread

        :param url: the link to pull posts from
        :return: A list of Post objects
        """
        page_soup = self.util.get_soup(url)
        return self.get_posts_from_soup(page_soup, url)

    def get_posts_from_soup(self, soup, thread_url):
        """
        Retrieves all posts from a given soup. Thread url is required to set each Post's thread_url

        :param soup: The soup to parse posts from
        :param thread_url: The thread url to be saved
        :return: A list of Post objects corresponding to the posts in the soup
        """
        posts = []
        for post_soup in soup.find_all(class_ = "post"):
            posts.append(self.__get_post_from_soup(post_soup.find(class_ = "inner")))
        for post in posts:
            # Set the thread_url for all the posts (up until "&start=xxxx")
            post.thread_url = thread_url.split("&start")[0]
        return posts

    def __get_post_from_soup(self, soup):
        """
        This method will create a post object from the BeautifulSoup of the post html

        :param soup: The BeautifulSoup object to parse
        :return: A Post object that contains info about each post.
        """
        post = Post()

        # Get author
        post.author = soup.find(class_ = "author").strong.a.text

        # Get date
        date = soup.find(class_ = "author").text.split(u"»")[1]
        post.date = datetime.strptime(date, " %a %b %d, %Y %I:%M %p ")

        # Get rep
        post.rep = int(soup.find(class_ = "reputation").text)

        # Get contents
        # TODO: improve content formatting?
        post.content = soup.find(class_ = "content").text

        # Get links
        for link in soup.find(class_ = "content").find_all("a"):
            post.links.append(link['href'])

        # Get thread (store in form of [name, url] in case something changes)
        post.thread_title = soup.h3.text.split("Re: ")[-1]

        return post


class Post:
    def __init__(self):
        self.author = ""
        self.date = None
        self.rep = 0
        self.content = ""
        self.links = []
        self.thread_title = ""
        self.thread_url = ""


if __name__ == "__main__":
    util = CaretagsUtils()
    util.login_from_file()

    forums = util.get_all_forums()
    threads = util.get_all_threads(forums[0])

    postUtil = PostUtils()
    postUtil.get_posts_from_url(threads[0])
