#!/usr/bin/env python

"""
This script uses Europeana's sitemap to extract rdfa metadata from the
pages and save it off as ntriples to the local filesystem.
"""

import os
import re
import time
import urllib
import logging
import multiprocessing

import ptree
import rdflib
import sitemap


def crawl(url):
    """
    crawl a website using its sitemap, and save off the rdfa extracted
    from the page.
    """
    pool = multiprocessing.Pool(processes=1)
    for urlset in sitemap.SitemapIndex.from_url(url):
        pool.map(fetch, [url.loc for url in urlset])
    pool.join()


def fetch(url):
    """
    GETs a url, extracts RDFa from it, and persists it to disk. fetch()
    will return the name of the file where the metadata was stored, or
    None if the RDF was already fetched.
    """
    dirname = "store" + ptree.id2ptree(url)
    path = os.path.join(dirname, "metadata.nt")

    # if it's there already don't bother getting it again
    if os.path.isfile(path):
        logging.info("already harvested %s as %s" % (url, path))
        return None

    # create the directory if necessary
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    # extract rdfa and save it
    try:
        graph = rdflib.Graph()
        html = urllib.urlopen(url).read()
        graph.parse(data=html, format="rdfa")
        triples = len(graph)
        graph.serialize(open(path, "w"), format="nt")
        logging.info("saved %s as %i triples in %s" % (url, triples, path))
    except: 
        logging.exception("unable to extract rdfa from %s" % url)

    # be nice
    time.sleep(2)
    return path


if __name__ == "__main__":
    logging.basicConfig(filename="crawl.log", level=logging.INFO)
    crawl("http://www.europeana.eu/portal/europeana-sitemap-index-hashed.xml")
