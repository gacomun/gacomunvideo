import sqlite3
import xbmc
from sqlite3 import Error
from common import logger
from core import filetools
from platformcode import config
 
 
fname = filetools.join(config.get_data_path(), "gacomunvideo.sqlite")

def exists_bd():
    dev=False
    dev=filetools.exists(fname)
    return dev
    
def hardReset_bd():
    drop_bd()
    create_bd()


def execute_sql(sql):
    conn = sqlite3.connect(fname)
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    records = c.fetchall()
    if sql.lower().startswith("select"):
        nun_records = len(records)
        if nun_records == 1 and records[0][0] is None:
            nun_records = 0
            records = []
    else:
        nun_records = conn.total_changes
    conn.close()
    return nun_records, records

def create_bd():
    conn = sqlite3.connect(fname)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS Series (idKodi INTEGER PRIMARY KEY, nombre TEXT, idExterno INTEGER, poster TEXT,fanart TEXT,plot TEXT,estado TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS Temporadas (idKodi INTEGER , temporada INTEGER , Capitulos INTEGER , PRIMARY KEY (idKodi, temporada))')
    c.execute('CREATE TABLE IF NOT EXISTS Categorias (idCategoria INTEGER PRIMARY KEY, descripcion TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS CategoriaSeries (idKodi INTEGER, idCategoria INTEGER , PRIMARY KEY (idKodi, idCategoria))')
    conn.commit()
    conn.close()
    
def drop_bd():
    conn = sqlite3.connect(fname)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS Series')
    c.execute('DROP TABLE IF EXISTS Temporadas')
    c.execute('DROP TABLE IF EXISTS Estados')
    c.execute('DROP TABLE IF EXISTS Categorias')
    c.execute('DROP TABLE IF EXISTS CategoriaSeries')
    conn.commit()
    conn.close()
    
def execute_sql_kodi(sql):
    """
    Ejecuta la consulta sql contra la base de datos de kodi
    @param sql: Consulta sql valida
    @type sql: str
    @return: Numero de registros modificados o devueltos por la consulta
    @rtype nun_records: int
    @return: lista con el resultado de la consulta
    @rtype records: list of tuples
    """
    logger.info("")
    file_db = ""
    nun_records = 0
    records = None

    # Buscamos el archivo de la BBDD de videos segun la version de kodi
    video_db = config.get_platform(True)['video_db']
    if video_db:
        file_db = filetools.join(xbmc.translatePath("special://userdata/Database"), video_db)

    # metodo alternativo para localizar la BBDD
    if not file_db or not filetools.exists(file_db):
        file_db = ""
        for f in filetools.listdir(xbmc.translatePath("special://userdata/Database")):
            path_f = filetools.join(xbmc.translatePath("special://userdata/Database"), f)

            if filetools.isfile(path_f) and f.lower().startswith('myvideos') and f.lower().endswith('.db'):
                file_db = path_f
                break

    if file_db:
        logger.info("Archivo de BD: %s" % file_db)
        conn = None
        try:
            import sqlite3
            conn = sqlite3.connect(file_db)
            cursor = conn.cursor()

            logger.info("Ejecutando sql: %s" % sql)
            cursor.execute(sql)
            conn.commit()

            records = cursor.fetchall()
            if sql.lower().startswith("select"):
                nun_records = len(records)
                if nun_records == 1 and records[0][0] is None:
                    nun_records = 0
                    records = []
            else:
                nun_records = conn.total_changes

            conn.close()
            logger.info("Consulta ejecutada. Registros: %s" % nun_records)

        except:
            logger.error("Error al ejecutar la consulta sql")
            if conn:
                conn.close()

    else:
        logger.debug("Base de datos no encontrada")

    return nun_records, records