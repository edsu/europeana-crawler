#!/usr/bin/env python

"""
This script uses Europeana's sitemap to extract rdfa metadata from the
pages and save it off as ntriples to the local filesystem.
"""

import os
import re
import time
import logging

import ptree
import rdflib
import sitemap


def crawl(url):
    """
    crawl a website using its sitemap, and save off the rdfa extracted
    from the page.
    """
    count = 0 

    for urlset in sitemap.SitemapIndex.from_url(url):
        for url in urlset:
            try:
                fetch(url.loc)
            except:
                logging.exception("unable to fetch %s" % url.loc)
            # respect
            time.sleep(2)


def fetch(url):
    dirname = "store" + ptree.id2ptree(url)
    path = os.path.join(dirname, "metadata.nt")
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    graph = rdflib.Graph()
    graph.parse(url, format="rdfa")
    triples = len(graph)
    graph.serialize(open(path, "w"), format="nt")

    logging.info("saved %s as %i triples in %s" % (url, triples, path))

    return path


if __name__ == "__main__":
    logging.basicConfig(filename="crawl.log", level=logging.INFO)
    crawl("http://www.europeana.eu/portal/europeana-sitemap-index-hashed.xml")
