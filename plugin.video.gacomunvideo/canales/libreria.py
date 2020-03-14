# -*- coding: utf-8 -*-
# encoding=utf8  
import sys  

import re
import time
from bs4 import BeautifulSoup
import math


from common import tools, config, sqliteDB
from platformcode import logger,platformtools
from core import jsontools

canalAction= "libreria"
urlbasetmdb="http://image.tmdb.org/t/p/original"
key_tmdb="20160e4a753a7b8bd88c4428b44650e2"
reload(sys)  
sys.setdefaultencoding('utf8')


def mainlist(args):
    
    action = args.get('action', None)
    
    logger.info(action[0])
    
    if action[0]==canalAction:
        principal()
    elif action[0]==canalAction+"todo":
        todo(args)
    elif action[0]==canalAction+"herramientasMenu":
        herramientasMenu()
    elif action[0]==canalAction+"herramientasHardReset":
#         sqliteDB.hardReset_bd()
        actualizaLibreria()
    elif action[0]==canalAction+"categoria":
        categoriamenu()
    elif action[0]==canalAction+"estado":
        estadomenu()
    elif action[0]==canalAction+"herramientasMantenimiento":
        herramientasMantenimiento()
    else:
        logger.debug("Sin accion")


def herramientasMantenimiento():
    logger.info("")
    sqlSelect="Select idKodi, nombre, idExterno, poster, fanart, plot, estado  from Series"
    nun_recordsS, recordsS = sqliteDB.execute_sql(sqlSelect)
    if(nun_recordsS!=0):
        for row in recordsS:
            href = ''
            title = (row[1]).encode("utf-8", "ignore")
            thumbnail = row[3]
            action=""
            url = tools.build_url({'action':action,'url_':href})
            tools.addItemMenu(label = title,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= False)        
        
def actualizaLibreria():
    logger.info("")
    mantenimientoBD()
#     obtener resultados BBDD Kodi
    nun_records, records =getBBDDKodi()
#     Por cada elemento
    heading = config.get_localized_string(30020)
    p_dialog = platformtools.dialog_progress_bg("Actualizando", heading)
    p_dialog.update(0, '')
    if(nun_records!=0):
        t = float(100) / nun_records
        i=0
        for row in records:
            p_dialog.update(int(math.ceil((i + 1) * t)), heading, row[1])
#         Obtener id de resultado Kodi 
            id=getIdFromKodi(row)
            if(id==""):
                dict_data=search_themoviedb(row[1])
                if(dict_data['total_results']!=0):
                    elemento=dict_data['results'][0]
                    id=str(elemento['id'])
#         Buscar datos generales de TMDB con id
            dict_data2=tvshow_tmdb(id)            
            insertDataBBDD(dict_data2,row,id)            
#         Insertar datos generales en BBDD 
#         Insertar datos temporadas en BBDD 
#         Insertar datos generos en BBDD 
            i=i+1
    p_dialog.close()

def insertDataBBDD(data,row,idExterno):
    logger.info("")
    idKodi=str(row[0])
    nombre=""
    poster=""
    estado=""
    fanart=""
    plot=""
    try:
        nombre=row[1].encode("utf-8", "ignore").replace("'",'"')
        poster=urlbasetmdb+data['poster_path']
        estado=data['status'].encode("utf-8", "ignore")
        fanart=urlbasetmdb+data['backdrop_path']
        plot=data['overview'].encode("utf-8", "ignore").replace("'",'"')
        sqlInsert="INSERT INTO Series (idKodi, nombre, idExterno, poster, fanart, plot, estado) VALUES ("+idKodi+", '"+nombre+"', "+idExterno+", '"+poster+"', '"+fanart+"', '"+plot+"', '"+estado+"');"
        sqliteDB.execute_sql(sqlInsert)
    except Exception as e:
        logger.debug(nombre)
        logger.debug(str(e))  
    elementos=data['seasons']
    try:
         
        elementos=data['seasons']
        for it in elementos:
            temporada=str(it["season_number"])
            Capitulos=str(it["episode_count"])
            sqlInsert="INSERT INTO Temporadas (idKodi, temporada, Capitulos) VALUES ("+idKodi+", "+temporada+", "+Capitulos+");"
            sqliteDB.execute_sql(sqlInsert)
    except Exception as e:
        logger.debug(nombre)
        logger.debug(str(e))  
    try:
        elementos=data['genres']
        for it in elementos:
            idCategoria=str(it["id"])
            descripcion=str(it["name"])
            sqlInsert="INSERT OR IGNORE INTO Categorias (idCategoria, descripcion) VALUES ("+idCategoria+", '"+descripcion+"');"
            sqliteDB.execute_sql(sqlInsert)
            idCategoria=str(it["id"])
            sqlInsert="INSERT OR IGNORE INTO CategoriaSeries (idKodi, idCategoria) VALUES ("+idKodi+", "+idCategoria+");"
            sqliteDB.execute_sql(sqlInsert)

    except Exception as e:
        logger.debug(nombre)
        logger.debug(str(e))

     
def getIdFromKodi(row):
    logger.info("")
    patron = 'api\.themoviedb\.org\/3\/tv\/(.+)\?'
    id=""
    matches = re.compile(patron, re.DOTALL).findall(row[2])
    if len(matches)>0:
        id=matches[0]
    return id

def getBBDDKodi():
    logger.info("")
    sql = 'Select tv.idShow, tv.c00, tv.c10  from tvshow tv'
    nun_records, records = sqliteDB.execute_sql_kodi(sql)
    return nun_records, records
    

def mantenimientoBD():
    logger.info("")
#    Si no Existe BBDD?
#     if(not sqliteDB.exists_bd()):
#        Crear
#    Borrar Tablas
    sqliteDB.hardReset_bd()
#    
        
    
def herramientasMenu():
    logger.info("")
    href = ''
    title = config.get_localized_string(30018)
    thumbnail = ''
    action=canalAction+"herramientasHardReset"
    url = tools.build_url({'action':action,'url_':href})
    tools.addItemMenu(label = title,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= False)
    
    href = ''
    title = config.get_localized_string(30019)
    thumbnail = ''
    action=canalAction+"herramientasMantenimiento"
    url = tools.build_url({'action':action,'url_':href})
    tools.addItemMenu(label = title,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)

def todo(args):
    logger.info("")
    categoria = args.get('categoria', None)
    estado = args.get('estado', None)
    sql = 'SELECT idKodi, nombre, idExterno, poster, fanart, plot, estado FROM Series;'
    if(categoria is not None):
        sql = 'SELECT s.idKodi, s.nombre, s.idExterno, s.poster, s.fanart, s.plot, s.estado FROM Series s, CategoriaSeries c where s.idKodi=c.idKodi and c.idCategoria='+categoria[0]+';'
    if(estado is not None):
        sql = 'SELECT s.idKodi, s.nombre, s.idExterno, s.poster, s.fanart, s.plot, s.estado FROM Series s where s.estado="'+estado[0]+'";'
    nun_records, records = sqliteDB.execute_sql(sql)
    if nun_records == 0:
        href = ''
        title = config.get_localized_string(30016)
        thumbnail = ''
        action=''
        url = tools.build_url({'action':action,'url_':href})
        tools.addItemMenu(label = title,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= False)
    else:
        for row in records:
            colorB=""
            colorE=""
            if(row[6]=="Ended"):
                colorB="[COLOR springgreen]"
                colorE="[/COLOR]"
            elif(row[6]=="Canceled"):
                colorB="[COLOR tomato]"
                colorE="[/COLOR]"
            tempo, epiodioAct=searchinKodi(str(row[0]))
            if(tempo!=-1):
                if(tempo==0):
                    tempo=1
                sqlepi = 'SELECT idKodi, temporada, Capitulos FROM Temporadas where idKodi='+str(row[0])+' and temporada='+str(tempo)+';'
                nun_recordsepi, recordsepi = sqliteDB.execute_sql(sqlepi)
                if nun_recordsepi!= 0 and epiodioAct>= recordsepi[0][2]:
                    href = ''
                    title = colorB+row[1].encode("utf-8", "ignore")+" (T. "+str(tempo)+")"+colorE
                    thumbnail = row[3]
                    fanart = row[4]
                    action=''
                    url = tools.build_url({'action':action,'url_':href})
                    tools.addItemMenu(label = title,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= False,fanart=fanart)
#                 else:
#                     colorB="[COLOR tomato]"
#                     colorE="[/COLOR]"
                    
                        

def searchinKodi(idShow):
    numepisodioact=-1
    tempoAct=-1
    sql="Select e.idshow,tv.c00 nombre, min(e.c12) temporada  from episode e, tvshow tv, files f where e.idshow=tv.idshow and e.idfile=f.idfile and f.lastplayed isnull and tv.idShow="+str(idShow)+" group by e.idshow"
    nun_records, records = sqliteDB.execute_sql_kodi(sql)
    if nun_records != 0:
        tempoAct=records[0][2]
        sqlepis="Select MAX(CAST(e.c13 AS Int)) from episode e WHERE e.idShow="+str(idShow)+" and e.c12='"+records[0][2]+"'"
        nun_recordsepis, recordsepis = sqliteDB.execute_sql_kodi(sqlepis)
        numepisodioact=recordsepis[0][0]
    return tempoAct, numepisodioact

def search_themoviedb(ShowName):
    scrapedurl="https://api.themoviedb.org/3/search/tv?api_key="+key_tmdb+"&language=es-ES&query="+ShowName.encode("utf-8", "ignore").replace(" ","+")
    data = tools.getUrl(scrapedurl)
    dict_data = jsontools.load(data)
    return dict_data
def tvshow_tmdb(idShow):
    urltvshow="https://api.themoviedb.org/3/tv/"+str(idShow)+"?api_key="+key_tmdb+"&language=es-ES"
    logger.debug(urltvshow)
    datatvshow = tools.getUrl(urltvshow)
    dict_datatvshow = jsontools.load(datatvshow)
    return dict_datatvshow
        
    


    
    
def principal():
    logger.info("")
    href = ''
    title = config.get_localized_string(30017)
    thumbnail = ''
    action=canalAction+"herramientasMenu"
    url = tools.build_url({'action':action,'url_':href})
    tools.addItemMenu(label = title,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)
  
    href = ''
    title = config.get_localized_string(30015)
    thumbnail = ''
    action=canalAction+"todo"
    url = tools.build_url({'action':action,'url_':href})
    tools.addItemMenu(label = title,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)
    
    href = ''
    title = config.get_localized_string(30005)
    thumbnail = ''
    action=canalAction+"categoria"
    url = tools.build_url({'action':action,'url_':href})
    tools.addItemMenu(label = title,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)

    href = ''
    title = config.get_localized_string(30021)
    thumbnail = ''
    action=canalAction+"estado"
    url = tools.build_url({'action':action,'url_':href})
    tools.addItemMenu(label = title,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)
def categoriamenu():
    sql="SELECT idCategoria, descripcion FROM Categorias;"
    nun_records, records = sqliteDB.execute_sql(sql)
    for row in records:
        href = ''
        title = (row[1]).encode("utf-8", "ignore")
        thumbnail = ''
        action=canalAction+"todo"
        url = tools.build_url({'action':action,'categoria':str(row[0])})
        tools.addItemMenu(label = title,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)        

def estadomenu():
    sql="Select distinct(estado) from Series;"
    nun_records, records = sqliteDB.execute_sql(sql)
    for row in records:
        href = ''
        title = (row[0]).encode("utf-8", "ignore")
        thumbnail = ''
        action=canalAction+"todo"
        url = tools.build_url({'action':action,'estado':str(row[0])})
        tools.addItemMenu(label = title,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)        

