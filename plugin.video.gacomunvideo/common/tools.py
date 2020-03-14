# -*- coding: utf-8 -*-

import logger
import xbmcaddon
import re
import urllib2
import xbmcgui
import xbmcplugin
import sys
import urllib

from platformcode import logger
     
def getSetting(settingName):
    setting=xbmcaddon.Addon().getSetting(settingName)
        
    return setting

def getUrl(url):
    #logger.debug(url)
# Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

    req = urllib2.Request(url, headers=hdr)
    f=urllib2.urlopen(req)
    data=f.read()
    f.close()

    return data

def findall(pattern, searText, flags=0):
    #logger.debug("findall - pattern: {0}".format(pattern))

    try:

        return re.findall(pattern, searText,flags)

    except Exception as e:
        logger.debug(str(e))
        return None

def addItemMenu(label, thumbnail, url, IsPlayable = 'false', isFolder= True,fanart=''):

    handle = int(sys.argv[1])

    logger.debug("addItemMenu - label:{0}, thumbnail: {1}, url: {2}, IsPlayable: {3}, isFolder: {4}".format(label,thumbnail,url,IsPlayable,isFolder))

    li= xbmcgui.ListItem(label=label, thumbnailImage=thumbnail)
    li.setProperty('IsPlayable', IsPlayable)
    li.setArt({'fanart': fanart})

    xbmcplugin.addDirectoryItem(handle, listitem = li, url = url, isFolder = isFolder)

def build_url(query):

    base_url = sys.argv[0]

    return base_url + '?' + urllib.urlencode(query)


def play_resolved_url(url):
    logger.debug("play_resolved_url ["+url+"]")
    listitem = xbmcgui.ListItem(path=url)
    return xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)


