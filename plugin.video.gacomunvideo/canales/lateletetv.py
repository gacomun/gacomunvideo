from common import tools, logger
import re

def menu():
#     label='Latelete.tv'
#     thumbnail=''
#     url=''
#     tools.addItemMenu(label = label,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)
#     label='Configurar'
#     thumbnail=''
#     url=''
#     tools.addItemMenu(label = label,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)
    domain = "http://latelete.tv/"
    html = tools.getUrl(domain)
# <center>(.*?)</center>
    pattern = '<center>(.*?)</center>'
    canalesTabla = tools.findall(pattern, html , re.DOTALL)[0]
    logger.debug(canalesTabla)
    pattern = '<td>(.*?)</td>'
    canallista = tools.findall(pattern, canalesTabla , re.DOTALL)
    for canal in canallista:
        try:
            pattern = '<a href.*title="(.*?)"><.*></a>'
            label = tools.findall(pattern, canal , re.DOTALL)[0]
            pattern = '<img src="(.*?)" height'
            thumbnail = domain + tools.findall(pattern, canal , re.DOTALL)[0]
            pattern = '<a href="(.*?)" title=".*</a>'
            url_ = tools.findall(pattern, canal , re.DOTALL)[0]            
            url = tools.build_url({'action':'lateletetvAction','url_':url_})
            tools.addItemMenu(label = label,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)
        except Exception as e:
            logger.debug(str(e))

def getvideo(url_):
    logger.debug(url_)
    domain = url_
    html = tools.getUrl(domain)
#     logger.debug(html)
# <center>(.*?)</center>
#     pattern = '<iframe.*src="(.*?)"></iframe>'
#     videoframe = tools.findall(pattern, html )[0]
#     html = tools.getUrl(videoframe)
#     pattern = '<iframe.*src="(.*?)"></iframe>'
#     videoframe = tools.findall(pattern, html )[0]
#     logger.debug(videoframe)
    label='prueba'
    thumbnail=''
    url = 'rtmp://31.220.0.187/privatestream/ playpath=partidos965?keys=WVTsGhsO-0Apepn4-vkzWg&keyt=1448255210'
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    playlist.add(url, xlistitem)
    xbmc_player.play(playlist, xlistitem)
    tools.addItemMenu(label = label,thumbnail= thumbnail, url= url,IsPlayable = 'true', isFolder= False)
