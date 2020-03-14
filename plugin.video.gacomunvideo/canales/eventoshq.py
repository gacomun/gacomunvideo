# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup


from common import tools, config
# from core import scrapertools
from platformcode import logger

host = 'http://canales.eventoshq.me/ini.html'
headers = [['User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'],
           ['Referer', host]]
canalAction= "eventoshq"


def mainlist(args):
    
    action = args.get('action', None)
    
    logger.info(action[0])
    
    if action[0]==canalAction:
        principal()
    elif action[0]==canalAction+"f12018":
        f12018(args)
    elif action[0]==canalAction+"envivo":
        envivo(args)
    elif action[0]==canalAction+"descargas":
        descargas(args)
    elif action[0]==canalAction+"descargaspage":
        descargaspage(args)
    elif action[0]==canalAction+"descargasplay":
        descargasplay(args)
    else:
        logger.debug("Sin accion")


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info()
    itemlist = []

    header = {}
    if "|" in page_url:
        page_url, referer = page_url.split("|", 1)
        header = {'Referer': referer}

    data = tools.getUrl(page_url)

    subtitle = scrapertools.find_single_match(data, '<track kind="captions" src="([^"]+)" srclang="es"')

    try:
        code = scrapertools.find_single_match(data, '<p style="" id="[^"]+">(.*?)</p>' )
        _0x59ce16 = eval(scrapertools.find_single_match(data, '_0x59ce16=([^;]+)').replace('parseInt', 'int'))
        _1x4bfb36 = eval(scrapertools.find_single_match(data, '_1x4bfb36=([^;]+)').replace('parseInt', 'int'))
        parseInt  = eval(scrapertools.find_single_match(data, '_0x30725e,(\(parseInt.*?)\),').replace('parseInt', 'int'))
        url = decode(code, parseInt, _0x59ce16, _1x4bfb36)
        url = httptools.downloadpage(url, only_headers=True, follow_redirects=False).headers.get('location')
        extension = scrapertools.find_single_match(url, '(\..{,3})\?')
        itemlist.append([extension, url, 0,subtitle])

    except Exception:
        logger.info()
        if config.get_setting('api', __file__):
            url = get_link_api(page_url)
            extension = scrapertools.find_single_match(url, '(\..{,3})\?')
            if url:
                itemlist.append([extension, url, 0,subtitle])
    logger.debug(itemlist)

    return itemlist

def decode(code, parseInt, _0x59ce16, _1x4bfb36):
    logger.info()
    import math

    _0x1bf6e5 = ''
    ke = []

    for i in range(0, len(code[0:9*8]),8):
        ke.append(int(code[i:i+8],16))

    _0x439a49 = 0
    _0x145894 = 0

    while _0x439a49 < len(code[9*8:]):
        _0x5eb93a = 64
        _0x896767 = 0
        _0x1a873b = 0
        _0x3c9d8e = 0
        while True:
            if _0x439a49 + 1 >= len(code[9*8:]):
                _0x5eb93a = 143;

            _0x3c9d8e = int(code[9*8+_0x439a49:9*8+_0x439a49+2], 16)
            _0x439a49 +=2

            if _0x1a873b < 6*5:
                _0x332549 = _0x3c9d8e & 63
                _0x896767 += _0x332549 << _0x1a873b
            else:
                _0x332549 = _0x3c9d8e & 63
                _0x896767 += int(_0x332549 * math.pow(2, _0x1a873b))

            _0x1a873b += 6
            if not _0x3c9d8e >= _0x5eb93a: break

        # _0x30725e = _0x896767 ^ ke[_0x145894 % 9] ^ _0x59ce16 ^ parseInt ^ _1x4bfb36
        _0x30725e = _0x896767 ^ ke[_0x145894 % 9] ^ parseInt ^ _1x4bfb36
        _0x2de433 = _0x5eb93a * 2 + 127

        for i in range(4):
            _0x3fa834 = chr(((_0x30725e & _0x2de433) >> (9*8/ 9)* i) - 1)
            if _0x3fa834 != '$':
                _0x1bf6e5 += _0x3fa834
            _0x2de433 = (_0x2de433 << (9*8/ 9))

        _0x145894 += 1


    url = "https://openload.co/stream/%s?mime=true" % _0x1bf6e5
    return url

def descargasplay(args):
   
#     url = args.get('url_', None)
#     tools.play_resolved_url(url[0])
    url = "https://openload.co/embed/IUVSqqkpHIw/Formula.1.GP.Monaco.2018.Carrera.MOVF1.HDTV.720p.EveHQ.mp4"
    itemlist=get_video_url(page_url=url)
#     url = "https://1fiagec.oloadcdn.net/dl/l/MIrWuOT9imvGpO8f/IUVSqqkpHIw/Formula.1.GP.Monaco.2018.Carrera.MOVF1.HDTV.720p.EveHQ.mp4?mime=true"
    tools.play_resolved_url(url)


def descargaspage(args):
   
    url = args.get('url_', None)
    html = tools.getUrl(url[0])
#     html = tools.getUrl("http://descargas.eventoshq.me/2018/04/08/descargar-formula-1-gp-bahrein-2018-carrera-espanol/")
    pagedata = BeautifulSoup(html, "html.parser")
    ldesc = pagedata.find_all("iframe")
    for link in ldesc:
        try:
            href = link.get("src")
            patron = 'http.*\/(.*)'
            matches = re.compile(patron, re.DOTALL).findall(href)
            texto=matches[0]
            logger.debug(texto)
            title = config.get_localized_string(30013) +" "+texto
#             title = ""
            thumbnail = ""
            action=canalAction+"descargasplay"
            url = tools.build_url({'action':action,'url_':href})
            tools.addItemMenu(label = title,thumbnail= thumbnail, url= url,IsPlayable = 'true', isFolder= False)     
        except Exception as e:
            logger.debug(str(e))      
            
    logger.info("")

    
def descargas(args):
   
    url = args.get('url_', None)
    html = tools.getUrl(url[0])
    pagedata = BeautifulSoup(html, "html.parser")
    ldesc = pagedata.find_all("article")
    for link in ldesc:
        try:
            ldiv=link.findAll("div")
            href = ldiv[0].find("a").get("href")
            title = str(link.find("h3").text.encode("utf-8", "ignore")).translate(None, '\t\n')
#             title = ""
            thumbnail = ldiv[0].find("img").get("src").encode("utf-8", "ignore")
            action=canalAction+"descargaspage"
            url = tools.build_url({'action':action,'url_':href})
            tools.addItemMenu(label = title,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)     
        except Exception as e:
            logger.debug(str(e))      
            
    nextpage = pagedata.find_all("a", class_ = "next page-numbers")
    try:
        href = nextpage[0].get("href")
        title =config.get_localized_string(30012)
        thumbnail = ''
        action=canalAction+"descargas"
        url = tools.build_url({'action':action,'url_':href})
        tools.addItemMenu(label = title,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)     
    except Exception as e:
        logger.debug(str(e))      
    logger.info("")

def envivo(args):
    logger.info("")
    url = args.get('url_', None)
    html = tools.getUrl(url[0])
    pagedata = BeautifulSoup(html, "html.parser")
    lcat = pagedata.find_all("td")
    for link in lcat:
        try:
            if "t535230_row_0" in link.get("id"):
                href = link.find("a").get("href")
                title = link.find("a").get("href")
                thumbnail = link.find("img").get("src")
                action=canalAction+"envivov2"
                url = tools.build_url({'action':action,'url_':href})
                tools.addItemMenu(label = title,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)     
        except Exception as e:
            logger.debug(str(e))       
    logger.info("")

def mainlistotro(args):
    html = tools.getUrl(host)
    logger.debug(html)
    pagedata = BeautifulSoup(html, "html.parser")
    table = pagedata.find_all("table", class_ = "wdn_responsive_table flush-left")
    tabledata = BeautifulSoup(table[0].__str__(), "html.parser")
    
    links=tabledata.find_all("td")
    for link in links:
        href = link.find("a").get("href")
        title = link.find("a").get("href")
        thumbnail = link.find("img").get("src")
        url = tools.build_url({'action':'eventoshq','url_':href})
        tools.addItemMenu(label = title,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)
    
    
def principal():
    logger.info("")
    href = 'http://www.eventoshq.me/historial-repeticiones-formula-1-2018-eventoshq'
    title = "Formula 1 2018"
    thumbnail = 'http://i.imgur.com/OjRMqwz.png?1'
    action=canalAction+"f12018"
    url = tools.build_url({'action':action,'url_':href})
    tools.addItemMenu(label = title,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)
    
    title = "*Programación en vivo"
    action=canalAction+"envivo"
    href = 'http://canales.eventoshq.me/casita.html'
    thumbnail = 'http://i.imgur.com/gmSqxSF.png'
    url = tools.build_url({'action':action,'url_':href})
    tools.addItemMenu(label = title,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)

    title = "*Repeticiones Online"
    action=canalAction+"repeticiones"
    href = 'http://www.eventoshq.me/repeticiones-eventoshq'
    thumbnail = 'http://i.imgur.com/fvWZVo2.png'
    url = tools.build_url({'action':action,'url_':href})
    tools.addItemMenu(label = title,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)

    title = "Descargas en HQ"
    action=canalAction+"descargas"
    href = 'http://descargas.eventoshq.me/category/formula-1/'
    thumbnail = 'http://i.imgur.com/kIQSz3G.png'
    url = tools.build_url({'action':action,'url_':href})
    tools.addItemMenu(label = title,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)

    url = tools.build_url({'action':canalAction+"hitorialrepeticiones",'url_':""})
    tools.addItemMenu(label = "*Historial de Repeticiones",thumbnail= "", url= url,IsPlayable = 'false', isFolder= True)

    url = tools.build_url({'action':canalAction+"wwe",'url_':""})
    tools.addItemMenu(label = "*WWE",thumbnail= "", url= url, IsPlayable = 'false', isFolder= True)

    url = tools.build_url({'action':canalAction+"ppvlatino",'url_':""})
    tools.addItemMenu(label = "*Proyecto PPV Latino",thumbnail= "", url= url, IsPlayable = 'false', isFolder= True)


def f12018(item):
    logger.info("")
    itemlist = []
    data = tools.getUrl(item.url)
    patron = '<tr>(.*?)</tr>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    for linea in matches:
        patron2 = '<td.*;">.*<span.*>(.*?)</span>.*</td>.*<td.*>.*<a href="(.*)">.*<span.*>(.*?)</span>.*</td>.*<td.*>.*<a href="(.*?)">.*</td>'
        matches2 = re.compile(patron2, re.DOTALL).findall(linea)
        if len(matches2)>0:
            logger.info()       
            itemlist.append(Item(channel=item.channel, title=matches2[0][0]+" "+matches2[0][2], action="findvideos", url=matches2[0][1], thumbnail='', fanart=''))
            itemlist.append(Item(channel=item.channel, title=matches2[0][0], action="findvideos", url=matches2[0][3], thumbnail='', fanart=''))

    return itemlist


def todas(item):
    logger.info()
    itemlist = []
    data = tools.getUrl(item.url)
    patron = '<div id="video.*".*><div.*thumb.*<a href="(.*)"><.*data-src="(.*)" data-idcdn.*<p>.*title="(.*)".*</p></div>'

    matches = re.compile(patron, re.DOTALL).findall(data)
    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        url = scrapedurl
        title = scrapedtitle.decode('utf-8')
        thumbnail = scrapedthumbnail
        fanart = ''
        itemlist.append(
            Item(channel=item.channel, action="episodios", title=title, url=url, thumbnail=thumbnail, fanart=fanart))

    # Paginacion
    title = ''
    siguiente = scrapertools.find_single_match(data,
                                               '<a rel="nofollow" class="next page-numbers" href="([^"]+)">Siguiente &raquo;<\/a><\/div>')
    title = 'Pagina Siguiente >>> '
    fanart = ''
    itemlist.append(Item(channel=item.channel, action="todas", title=title, url=siguiente, fanart=fanart))
    return itemlist


def search(item, texto):
    logger.info()
    texto = texto.replace(" ", "+")
    item.url = item.url + texto

    if texto != '':
        return todas(item)
    else:
        return []


def categorias(item):
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url, headers=headers).data
    patron = "<a href='([^']+)' class='tag-link-.*? tag-link-position-.*?' title='.*?' style='font-size: 11px;'>([^<]+)<\/a>"

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        url = scrapedurl
        title = scrapedtitle
        itemlist.append(Item(channel=item.channel, action="todas", title=title, fulltitle=item.fulltitle, url=url))

    return itemlist


def episodios(item):
    censura = {'Si': 'con censura', 'No': 'sin censura'}
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url, headers=headers).data
    old_mode = scrapertools.find_single_match(data, '<th>Censura<\/th>')
    if old_mode:
        patron = '<td>(\d+)<\/td><td>(.*?)<\/td><td>(.*?)<\/td><td>(.*?)<\/td><td><a href="(.*?)".*?>Ver Capitulo<\/a><\/td>'

        matches = re.compile(patron, re.DOTALL).findall(data)

        for scrapedcap, scrapedaud, scrapedsub, scrapedcen, scrapedurl in matches:
            url = scrapedurl
            title = 'CAPITULO ' + scrapedcap + ' AUDIO: ' + scrapedaud + ' SUB:' + scrapedsub + ' ' + censura[scrapedcen]
            thumbnail = ''
            plot = ''
            fanart = ''
            itemlist.append(Item(channel=item.channel, action="findvideos", title=title, fulltitle=item.fulltitle, url=url,
                                 thumbnail=item.thumbnail, plot=plot))
    else:
        patron = '<\/i>.*?(.\d+)<\/td><td style="text-align:center">MP4<\/td><td style="text-align:center">(.*?)<\/td>.*?'
        patron +='<a class="dr-button" href="(.*?)" >'

        matches = re.compile(patron, re.DOTALL).findall(data)

        for scrapedcap, scrapedsub, scrapedurl in matches:
            url = scrapedurl
            if scrapedsub !='':
                subs= scrapedsub
            else:
                sub = 'No'
            title = 'CAPITULO %s SUB %s'%(scrapedcap, subs)
            thumbnail = ''
            plot = ''
            fanart = ''
            itemlist.append(Item(channel=item.channel, action="findvideos", title=title, fulltitle=item.fulltitle, url=url,
                                 thumbnail=item.thumbnail, plot=plot))

    return itemlist

def findvideos(item):
    logger.info()

    itemlist = []
    data = httptools.downloadpage(item.url, headers=headers).data
    patron = '<iframe src="(.*?)"'
    matches = re.compile(patron, re.DOTALL).findall(data)
    for linea in matches:
        server = 'openload'
        itemlist.append(item.clone(url=linea, action="play",category="eventoshq",contentChannel="eventoshq",channel="videolibrary", server=server,title="f1" ))
    return itemlist


