#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a program that scrapes web pages for
emails, urls, and phone numbers.
"""

__author__ = "Kyle Meiklejohn"

import argparse
import requests
import re
import pprint
from bs4 import BeautifulSoup
from htmlparser import MyHTMLParser


parser = MyHTMLParser()


def request_func(url):
    """
    This function dodes a get request on a cmd line url.
    """
    r = requests.get(url)
    html_string = r.content
    with open('nook.html', 'w') as file:
        file.write(html_string)
    return html_string


def html_parse_data(html_string):
    """
    Returns a list of phone numbers, emails, and urls from a website.
    """
    html_text = request_func(html_string)
    email = list(
        re.findall(
            r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)',
            html_text))
    url_list = list(set(re.findall(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', html_text)))

    parser.feed(html_text)
    phone_numbers = []
    for data in parser.data:
        pattern = r'\W*\D([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?\D'
        matches = re.search(pattern, data)
        if matches:
            phone_numbers.append(
                '({}) {}-{}'.format(matches.group(1), matches.group(2), matches.group(3)))

    return email, url_list, phone_numbers

def soup_parser(html_string):
    """using beautiful soup to parse and regex html data"""

    soup = BeautifulSoup(html_string, 'html.parser')
    tag_a = soup.find_all('a', href=True)
    tag_email = soup.find_all('a')
    tag_img = soup.find_all('img', src=True)
    url_list = list(set(re.findall(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(tag_a))))
    img_list = list(set(re.findall(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(tag_img))))
    
    email = list(
        re.findall(
            r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)',
            str(tag_email)))

    phone_numbers = []
    pattern = r'\W*\D([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?\D'
    matches = re.search(pattern, str(tag_a))
    if matches:
        phone_numbers.append(
                '({}) {}-{}'.format(matches.group(1), matches.group(2), matches.group(3)))
    
    combine_list = img_list + url_list + email + phone_numbers
     
    print "\n".join(set(combine_list))
    print phone_numbers
    return

def main():
    """ Main entry point of the app """
    parser = argparse.ArgumentParser(
        description="Scrape the internet for information")
    parser.add_argument('url', type=str, help='enter an url.')
    args = parser.parse_args()
    html_data = request_func(args.url)
    soup_parser(html_data)

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
