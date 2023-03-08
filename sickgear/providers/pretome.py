# coding=utf-8
#
# This file is part of SickGear.
#
# SickGear is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SickGear is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickGear.  If not, see <http://www.gnu.org/licenses/>.

import re
import traceback

from . import generic
from .. import logger
from ..helpers import try_int
from bs4_parser import BS4Parser

from _23 import unidecode
from six import iteritems


class PreToMeProvider(generic.TorrentProvider):

    def __init__(self):
        generic.TorrentProvider.__init__(self, 'PreToMe')

        self.url_base = 'https://pretome.info/'

        self.urls = {'config_provider_home_uri': self.url_base,
                     'login': self.url_base + 'takelogin.php',
                     'search': self.url_base + 'browse.php?search=%s&tags=&st=1&tf=all&cat[]=7'}

        self.url = self.urls['config_provider_home_uri']

        self.api_key, self.username, self.password, self.minseed, self.minleech = 5 * [None]

    def _authorised(self, **kwargs):

        return super(PreToMeProvider, self)._authorised(post_params=dict(
            login='Login', returnto='%2F', login_pin=self.api_key, username=self.username, password=self.password))

    def _search_provider(self, search_params, **kwargs):

        results = []
        if not self._authorised():
            return results

        items = {'Cache': [], 'Season': [], 'Episode': [], 'Propers': []}

        rc = dict([(k, re.compile('(?i)' + v)) for (k, v) in iteritems({'info': 'details', 'get': 'download'})])
        for mode in search_params:
            for search_string in search_params[mode]:
                search_string = unidecode(search_string)
                search_url = self.urls['search'] % search_string

                html = self.get_url(search_url)
                if self.should_skip():
                    return results

                cnt = len(items[mode])
                try:
                    if not html or self._has_no_results(html):
                        raise generic.HaltParseException

                    with BS4Parser(html, attr='cellpadding="2"') as soup:
                        tbl_rows = [] if not soup else soup.find_all('tr')

                        if 2 > len(tbl_rows):
                            raise generic.HaltParseException

                        head = None
                        for tr in tbl_rows[1:]:
                            cells = tr.find_all('td')
                            if 10 > len(cells):
                                continue
                            try:
                                head = head if None is not head else self._header_row(
                                    tr, {'seed': r'up', 'leech': r'down'})
                                seeders, leechers, size = [try_int(n, n) for n in [
                                    cells[head[x]].get_text().strip() for x in ('seed', 'leech', 'size')]]
                                if self._reject_item(seeders, leechers):
                                    continue

                                info = tr.find('a', href=rc['info'])
                                title = (info.get('title') or info.get_text()).strip()
                                download_url = self._link(tr.find('a', href=rc['get'])['href'])

                            except (AttributeError, TypeError, ValueError, IndexError):
                                continue

                            if title and download_url:
                                items[mode].append((title, download_url, seeders, self._bytesizer(size)))

                except generic.HaltParseException:
                    pass
                except (BaseException, Exception):
                    logger.error(u'Failed to parse. Traceback: %s' % traceback.format_exc())

                self._log_search(mode, len(items[mode]) - cnt, search_url)

            results = self._sort_seeding(mode, results + items[mode])

        return results

    def ui_string(self, key):

        return ('%s_api_key' % self.get_id()) == key and 'Pin' or \
               ('%s_api_key_tip' % self.get_id()) == key and \
               '\'Pin=\' used in the <a href="%s">search input</a> at %s' % \
               (self.url_base, self.name) or ''


provider = PreToMeProvider()