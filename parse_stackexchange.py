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
import sys

from bs4 import BeautifulSoup
from pandas import DataFrame


try:
    xml = sys.argv[1]
except IndexError:
    xml = "data/posts.xml"

out = "%s.csv" % xml.split('.')[0]

doc = etree.parse("%s" % xml)
posts = [dict(e.items()) for e in doc.getiterator() if e.items() != []]
df = DataFrame(posts)

def decode_body(elem):
    try:
        e = elem.encode('utf-8')
        elem = "".join(BeautifulSoup(e).findAll(text=True))
    except AttributeError:
        # This means an empty value got through.
        elem = ""
    return elem

def utcify(date):
    # Oddly enough, the timestamps are already in UTC format,
    # except for a missing 'Z' at the end.
    if type(date) == "str":
        return "%sZ" % date
    else:
        return ""

def parse_tags(tag):
    # Tags are strings "<tag1><tag2-long><tag3-even-longer>".
    try:
        tag = tag.replace('<', ' ')
        tag = tag.replace('>', ' ')
        tags = [t.replace('-', ' ') for t in tag.split()]
    except AttributeError:
        # This means there are no tags provided.
        tags = [""]

    return tags

df['Body'] = df['Body'].map(decode_body)
df['CreationDate'] = df['CreationDate'].map(utcify)
#df['ClosedDate'] = df['ClosedDate'].map(utcify)
df['Tags'] = df['Tags'].map(parse_tags)

cols = ['Id', 'Body', 'CreationDate', 'Title', 'Tags']

df.to_csv(out,
    cols=cols,
    index=False,
    index_label=False,
    encoding='utf-8')
