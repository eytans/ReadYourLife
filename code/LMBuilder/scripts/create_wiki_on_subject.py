import pickle_for_titles
import os.path
import re
import sys
import utils
import argparse

__author__ = 'eytan'
wiki_xml_end = r'</mediawiki>'
wiki_xml_start = r'''<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.10/ http://www.mediawiki.org/xml/export-0.10.xsd" version="0.10" xml:lang="en">
  <siteinfo>
    <sitename>Wikipedia</sitename>
    <dbname>enwiki</dbname>
    <base>https://en.wikipedia.org/wiki/Main_Page</base>
    <generator>MediaWiki 1.27.0-wmf.7</generator>
    <case>first-letter</case>
    <namespaces>
      <namespace key="-2" case="first-letter">Media</namespace>
      <namespace key="-1" case="first-letter">Special</namespace>
      <namespace key="0" case="first-letter" />
      <namespace key="1" case="first-letter">Talk</namespace>
      <namespace key="2" case="first-letter">User</namespace>
      <namespace key="3" case="first-letter">User talk</namespace>
      <namespace key="4" case="first-letter">Wikipedia</namespace>
      <namespace key="5" case="first-letter">Wikipedia talk</namespace>
      <namespace key="6" case="first-letter">File</namespace>
      <namespace key="7" case="first-letter">File talk</namespace>
      <namespace key="8" case="first-letter">MediaWiki</namespace>
      <namespace key="9" case="first-letter">MediaWiki talk</namespace>
      <namespace key="10" case="first-letter">Template</namespace>
      <namespace key="11" case="first-letter">Template talk</namespace>
      <namespace key="12" case="first-letter">Help</namespace>
      <namespace key="13" case="first-letter">Help talk</namespace>
      <namespace key="14" case="first-letter">Category</namespace>
      <namespace key="15" case="first-letter">Category talk</namespace>
      <namespace key="100" case="first-letter">Portal</namespace>
      <namespace key="101" case="first-letter">Portal talk</namespace>
      <namespace key="108" case="first-letter">Book</namespace>
      <namespace key="109" case="first-letter">Book talk</namespace>
      <namespace key="118" case="first-letter">Draft</namespace>
      <namespace key="119" case="first-letter">Draft talk</namespace>
      <namespace key="446" case="first-letter">Education Program</namespace>
      <namespace key="447" case="first-letter">Education Program talk</namespace>
      <namespace key="710" case="first-letter">TimedText</namespace>
      <namespace key="711" case="first-letter">TimedText talk</namespace>
      <namespace key="828" case="first-letter">Module</namespace>
      <namespace key="829" case="first-letter">Module talk</namespace>
      <namespace key="2300" case="first-letter">Gadget</namespace>
      <namespace key="2301" case="first-letter">Gadget talk</namespace>
      <namespace key="2302" case="case-sensitive">Gadget definition</namespace>
      <namespace key="2303" case="case-sensitive">Gadget definition talk</namespace>
      <namespace key="2600" case="first-letter">Topic</namespace>
    </namespaces>
  </siteinfo>
'''


class WikiCreator(object):
    DEBUG = utils.DEBUG

    def __init__(self, path_to_wiki, path_to_titles_pickle):
        if not os.path.exists(path_to_wiki):
            raise RuntimeError("error - couldn't find wiki file")
        if not os.path.exists(path_to_titles_pickle):
            raise RuntimeError("error - couldn't find titles file.\ntitles path: "+path_to_titles_pickle + \
                               "\ncurrent dir: " + os.path.curdir)
        self._path_to_wiki = path_to_wiki
        self._titles = pickle_for_titles.load_pickle(path_to_titles_pickle)
        self._wiki_file = None
        self._re = re.compile(r'\[\[([^\]]*)\]\]') # this expression will return all text inside a [[ ]]

    def _print_read_page_error(self, title, text, reason=""):
        if WikiCreator.DEBUG:
            after = self._wiki_file.read(100)
            utils.error_print("Error when reading: " + title + "." + "at: " + str(self._titles[title][0]) + " reason: "\
                              + reason + "\n100 chars before:\n")
            self._wiki_file.seek(self._titles[title][0] - 100)
            utils.error_print(self._wiki_file.read(100) + "\npage: ")
            utils.error_print(text)
            utils.error_print("\n100 after:\n")
            utils.error_print(after + "\ndone\n")

    def _get_page(self, title):
        if title not in self._titles:
            return None
        # TODO: this is a fix for page not ending correctly as pythons read reads chars and not bytes (i.e. we were of
        #       because of the encoding). this fix isnt good performance wise so if you have time change it.
        self._wiki_file.seek(self._titles[title][0])
        res = self._wiki_file.read(self._titles[title][1]).strip()
        start_line = res.splitlines()[0]
        end_line = res.splitlines()[-1]
        if (not start_line.strip().startswith(u'<page>')) or \
                ((not end_line.strip().endswith(u'</page>\n')) and (not end_line.strip().endswith(u'</page>'))):
            utils.error_print("u'</page>\\n' is " + str(not end_line.strip().endswith(u'</page>\n')))
            utils.error_print("u'<page>' is " + str((not start_line.strip().startswith(u'<page>'))))
            self._print_read_page_error(title, res, "bad page start or end\n start line: " +
                                        start_line + "\n end: " + end_line)
        return res

    def _get_links(self, page):
        results = self._re.findall(page)
        return [r.split('|')[0] for r in results]

    def print_subjected_wiki(self, title, link_range=3, out_file=sys.stdout.buffer):
        utils.normal_print(wiki_xml_start, out_file)
        with open(self._path_to_wiki, 'r', encoding='utf8') as wiki_file:
            self._wiki_file = wiki_file
            cur_titles = [title]
            titles_set = set(cur_titles)
            next_pages = []
            while link_range > 0:
                link_range -= 1
                while len(cur_titles) > 0:
                    title = cur_titles.pop()
                    page = self._get_page(title)
                    if page:
                        utils.normal_print(page, out_file)
                        links = self._get_links(page)
                        for link in links:
                            if link not in titles_set:
                                next_pages.append(link)
                                titles_set.add(link)
                cur_titles = next_pages
                next_pages = []
        utils.normal_print(wiki_xml_end, out_file)

if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(description='Create a new wiki with data on a specific subject')
    args_parser.add_argument('dump', action='store', help='path to wiki dump file')
    args_parser.add_argument('titles_pickle', action='store', help='path to pickle file of wiki dump indexes')
    args_parser.add_argument('subject', action='store', help='title of the page to start with')
    args_parser.add_argument('--range', '-r', action='store', type=int, default=3,
                             help='how many links to check from first page')
    args_parser.add_argument('--outfile', '-o', action='store', default=None, help='file to write output too')
    args = args_parser.parse_args(sys.argv[1:])
    creator = WikiCreator(args.dump, args.titles_pickle)
    outfile = args.outfile
    if outfile is None:
        outfile = sys.stdout.buffer
    else:
        outfile = open(outfile, 'w', encoding='utf8')
    try:
        creator.print_subjected_wiki(args.subject, args.range, outfile)
    finally:
        outfile.close()
