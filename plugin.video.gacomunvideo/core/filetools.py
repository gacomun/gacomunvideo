# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# filetools
# Gestion de archivos con discriminación samba/local
# ------------------------------------------------------------

import os
import traceback

from platformcode import logger

try:
    from lib.sambatools import libsmb as samba
except:
    samba = None
    # Python 2.4 No compatible con modulo samba, hay que revisar

# Windows es "mbcs" linux, osx, android es "utf8"
if os.name == "nt":
    fs_encoding = ""
else:
    fs_encoding = "utf8"



def join(*paths):
    """
    Junta varios directorios
    Corrige las barras "/" o "\" segun el sistema operativo y si es o no smaba
    @rytpe: str
    @return: la ruta concatenada
    """
    list_path = []
    if paths[0].startswith("/"):
        list_path.append("")

    for path in paths:
        if path:
            list_path += path.replace("\\", "/").strip("/").split("/")

    if list_path[0].lower() == "smb:":
        return "/".join(list_path)
    else:
        return os.sep.join(list_path)

def exists(path):
    """
    Comprueba si existe una carpeta o fichero
    @param path: ruta
    @type path: str
    @rtype: bool
    @return: Retorna True si la ruta existe, tanto si es una carpeta como un archivo
    """
    path = encode(path)
    try:
        if path.lower().startswith("smb://"):
            return samba.exists(path)
        else:
            return os.path.exists(path)
    except:
        logger.error("ERROR al comprobar la ruta: %s" % path)
        logger.error(traceback.format_exc())
        return False

def encode(path, _samba=False):
    """
    Codifica una ruta según el sistema operativo que estemos utilizando.
    El argumento path tiene que estar codificado en utf-8
    @type path unicode o str con codificación utf-8
    @param path parámetro a codificar
    @type _samba bool
    @para _samba si la ruta es samba o no
    @rtype: str
    @return ruta codificada en juego de caracteres del sistema o utf-8 si samba
    """
    if not type(path) == unicode:
        path = unicode(path, "utf-8", "ignore")

    if path.lower().startswith("smb://") or _samba:
        path = path.encode("utf-8", "ignore")
    else:
        if fs_encoding:
            path = path.encode(fs_encoding, "ignore")

    return path

