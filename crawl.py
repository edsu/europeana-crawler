#!/usr/bin/env python

"""
This script uses the Europeana's sitemap to extreact rdfa metadata from the
pages and save it off as ntriples to the local filesystem using pairtree to 
spread out the files.
"""

import os
import re
import time

import ptree
import rdflib
import sitemap


def crawl(url):
    """
    crawl a website using its sitemap, and save off the rdfa extracted
    from the page.
    """
    for urlset in sitemap.SitemapIndex.from_url(url):
        for url in urlset:
            graph = rdflib.Graph()
            graph.parse(url.loc, format="rdfa")
            print write_record(url.loc, graph)
            # not so fast sparky
            time.sleep(2)


def write_record(url, graph):
    """
    write the graph as ntriples to the filesystem using a pairtree to spread 
    it out
    """
    # get the identifier from the url
    m = re.search('([A-Z0-9]+).html$', url)
    if not m: return

    # create the directory if we need to
    id = m.group(1)
    dirname = "store" + ptree.id2ptree(id)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    # write dem triples out
    path = os.path.join(dirname, id + ".nt")
    graph.serialize(open(path, "w"), format="nt")

    return path


if __name__ == "__main__":
    crawl("http://www.europeana.eu/portal/europeana-sitemap-index-hashed.xml")
