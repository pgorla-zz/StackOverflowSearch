#!/usr/bin/env python

"""
Each StackExchange folder contains 6 XML files: badges, comments,
posts, posthistory, users, votes. We are only interested in posts.
And perhaps comments.

This script reads and processes the data from posts.xml.

Relevant Fields:
    Body, CreationDate, ClosedDate, FavoriteCount, Id, Score, Tags, 
    Title, ViewCount

"""

from lxml import etree

from bs4 import BeautifulSoup
from pandas import DataFrame


DATADIR = "scifidata/"

xml = "posts.xml"

doc = etree.parse("%s%s" % (DATADIR, xml))
posts = [dict(e.items()) for e in doc.getiterator() 
    if e.items() != []]
df = DataFrame(posts)

def decode_body(elem):
    try:
        elem = elem.encode('utf-8')
        return ''.join(BeautifulSoup(elem).findAll(text=True)
    except AttributeError:
        # This means an empty value got through.
        return None

df['Body'] = df['Body'].map(decode_body)
