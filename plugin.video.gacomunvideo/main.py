# -*- coding: utf-8 -*-


REMOTE_DBG = False

# append pydev remote debugger
if REMOTE_DBG:
    # Make pydev debugger works for auto reload.
    # Note pydevd module need to be copied in XBMC\system\python\Lib\pysrc
    try:
        import sys
        sys.path.append('C:/todo/workspace/KodiPortable/App/Kodi/system/python/Lib/pysrc')
        import pydevd    # stdoutToServer and stderrToServer redirect stdout and stderr to eclipse console
#         import pysrc.pydevd as pydevd # with the addon script.module.pydevd, only use `import pydevd`
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
    except ImportError:
        sys.stderr.write("Error: " +
            "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")
        sys.exit(1)

from Common import logger
from Common import tools
import re
import xbmcplugin
import urlparse
import json

args = urlparse.parse_qs(sys.argv[2][1:])
#recupera el argumento action
action = args.get('action', None)
domain = "http://enraged.es/kodiaddon"
addon_handle = int(sys.argv[1])

if action is None:

    #Aquí sólo entra la primera vez para que el usuario pueda escoger categorías (fotos o videos)

    html = tools.getUrl(domain)
    
    pattern = '<figure>(.*?)</figure>'

    matches = tools.findall(pattern,html, re.DOTALL)

    for match in matches:
        
        pattern = 'ng-href="#/category/(.*?)'
        category = tools.findall(pattern, match , re.DOTALL)[0]

        if category == 'photo':
            url = tools.build_url({'action':'categorias','url_':'http://enraged.es/kodiaddon/php/getCategorias.php?contentType=photo'})
        else:
            url = tools.build_url({'action': 'categorias', 'url_' : 'http://enraged.es/kodiaddon/php/getCategorias.php?contentType=video'})
      
        pattern = 'alt="(.*)"'
        label = tools.findall(pattern,match, re.DOTALL)[0]

        pattern = 'src="(.*?)"'
        thumbnail = tools.findall(pattern,match, re.DOTALL)[0]

        thumbnail = thumbnail.replace("./", "/")
        thumbnail = domain + thumbnail

        tools.addItemMenu(label = label,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)

    xbmcplugin.endOfDirectory(addon_handle) 

else:
   
    if action[0] == 'categorias':

        url_ = args.get('url_',None)[0]

        response = tools.getUrl(url_)

        data = json.loads(response)
       
        for item in data:
            category = item['category']
            description =  item['description']
            thumbnail = domain + "/" + item['thumbnail']

            url = tools.build_url({'action':'subcategorias','url_':'http://enraged.es/kodiaddon/php/getContenido.php?category=' + category})

            tools.addItemMenu(label = description,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)
     
        xbmcplugin.endOfDirectory(addon_handle) 

    if action[0] == 'subcategorias':

        url_ = args.get('url_',None)[0]

        response = tools.getUrl(url_)

        data = json.loads(response)

        counter = 1

        for item in data:

            contentPath = item['contentPath']
            description ="video: " + str(counter)
            thumbnail=""
            
            url = domain + "/" + contentPath

            counter= counter + 1

            tools.addItemMenu(label = description,thumbnail= thumbnail, url= url,IsPlayable = 'true', isFolder= False)

        xbmcplugin.endOfDirectory(addon_handle)




