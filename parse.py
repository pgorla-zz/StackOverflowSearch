#!/usr/bin/env python

"""
Each StackExchange folder contains 6 XML files: badges, comments,
posts, posthistory, users, votes.

This script enters into the specified directory and combines the data 
into an xml file readable by Solr.

If there is no schema.xml written, it writes that too.
"""

from lxml import etree
from pandas import DataFrame


DATADIR = "scifidata/"


class Document(Object):
""" Generate a DataFrame from xml. """

    def __init__(self, xml):
        doc = etree.parse("%s%s" % (DATADIR, xml))
        self.dictitems = [dict(e.items()) for e in doc.getiterator()]
        self.df = DataFrame(self.dictitems)

doc = etree.parse("scifidata/posts.xml")
root = doc.getroot()

# Generates a list of all items for every row.
posts = [dict(elem.items()) for elem in doc.getiterator()]

# Might not need to specify index.
df = DataFrame(posts, index=range(len(posts)))

