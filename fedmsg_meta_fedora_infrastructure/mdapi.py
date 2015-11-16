# This file is part of fedmsg.
# Copyright (C) 2015 Red Hat, Inc.
#
# fedmsg is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# fedmsg is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with fedmsg; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
# Authors:  Pierre-Yves Chibon <pingou@pingoured.fr>
#

from fedmsg_meta_fedora_infrastructure import BaseProcessor


def get_packages(message):
    ''' Returns the list of all the packages mentionned in the message. '''
    pkgs = set()
    for category in message['msg']['differences']:
        for action in message['msg']['differences'][category]:
            for details in message['msg']['differences'][category][action]:
                if '/' in details[0]:
                    name = details[-1]
                else:
                    name = details[0]
                name = name.split('(')[0]
                pkgs.add(name)
    return pkgs


def get_objects(message):
    repo = message['msg']['name']
    for category in message['msg']['differences']:
        for action in message['msg']['differences'][category]:
            for details in message['msg']['differences'][category][action]:
                if '/' in details[0]:
                    name = details[-1]
                else:
                    name = details[0]
                yield '%s/%s/%s/%s' % (repo, category, action, name)


def get_summary(message):
    ''' Returns a summary of the addition/deletion for each category in
    the specified message.
    '''
    summary = list()
    for category in sorted(message['msg']['differences']):
        cnt_a = len(message['msg']['differences'][category]['added'])
        cnt_d = len(message['msg']['differences'][category]['removed'])
        summary.append('{0}: +{1}/-{2}'.format(category, cnt_a, cnt_d))
    return summary


class MdapiProcessor(BaseProcessor):
    __name__ = "mdapi"
    __description__ = "the Fedora repository meta-data API"
    __link__ = "https://apps.fedoraproject.org/mdapi"
    __docs__ = "https://apps.fedoraproject.org/mdapi"
    __obj__ = "Medata API update"
    __icon__ = ("https://apps.fedoraproject.org/packages/"
                "images/icons/package_128x128.png")

    def subtitle(self, msg, **config):
        if 'mdapi.repo.update' in msg['topic']:
            tmpl = self._(
                u"mdapi noticed a {repo} repomd change: {summary}"
            )
            repo = msg['msg']['name']
            summary = ', '.join(get_summary(msg))
            return tmpl.format(repo=repo, summary=summary)
        else:
            raise NotImplementedError("%r" % msg)

    def secondary_icon(self, msg, **config):
        return self.__icon__

    def link(self, msg, **config):
        url = msg['msg']['url']
        if url.startswith('http'):
            return url
        else:
            return 'https://download.fedoraproject.org/pub/' + url

    def objects(self, msg, **config):
        return set(get_objects(msg))

    def packages(self, msg, **config):
        return set(get_packages(msg))
