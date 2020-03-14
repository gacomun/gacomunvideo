REMOTE_DBG = True
REMOTE_DBG = False

# append pydev remote debugger
if REMOTE_DBG:
    # Make pydev debugger works for auto reload.
    # Note pydevd module need to be copied in XBMC\system\python\Lib\pysrc
    try:
        import sys
        sys.path.append('/usr/share/kodi/system/python')
        import pydevd    # stdoutToServer and stderrToServer redirect stdout and stderr to eclipse console
#         import pysrc.pydevd as pydevd # with the addon script.module.pydevd, only use `import pydevd`
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
    except ImportError:
        sys.stderr.write("Error: " +
            "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")
        sys.exit(1)

import sys
from common import menu, sqliteDB
import xbmcplugin
from platformcode import logger
import urlparse
from canales import lateletetv, eventoshq, libreria


addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
action = args.get('action', None)

logger.debug("Ini")
if action is None:
#     if(not sqliteDB.exists_bd()):
#         sqliteDB.hardReset_bd()
#         libreria.actualizaLibreria()
    menu.mainmenu()
elif "eventoshq" in action[0]:
   logger.debug('eventoshq')
   eventoshq.mainlist(args)
elif "lateletetv" in action[0]:
   logger.debug('lateletetv')
   lateletetv.menu()
elif "BPeliculas" in action[0]:
   logger.debug('BPeliculas')
   menu.bpeliculasmenu()
elif "BPCategoria" in action[0]:
   logger.debug('BPCategoria')
   menu.bpcategoriamenu()
elif "BSCategoria" in action[0]:
   logger.debug('BSCategoria')
   menu.bscategoriamenu()
elif "BSeries" in action[0]:
   logger.debug('BSeries')
   menu.bseriesmenu()
elif "lateletetvAction" in action[0]:
   logger.debug('lateletetvAction')
   url_ = args.get('url_',None)[0]
   lateletetv.getvideo(url_)
elif "libreria" in action[0]:
   logger.debug('libreria')
   libreria.mainlist(args)
else:
   logger.debug('Sin Accion')
xbmcplugin.endOfDirectory(addon_handle);