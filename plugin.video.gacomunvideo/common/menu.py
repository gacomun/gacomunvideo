from common import tools, config


def mainmenu():
    label='Eventos HQ'
    thumbnail='http://4.bp.blogspot.com/-VlnuTY3viAg/UWszxZnB96I/AAAAAAAAApQ/VgnL-wD2czc/s320/LOGONUEVO.png'
    url = tools.build_url({'action':'eventoshq','url_':''})
    tools.addItemMenu(label = label,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)
    
    label=config.get_localized_string(30014)
    thumbnail=''
    url = tools.build_url({'action':'libreria','url_':''})
    tools.addItemMenu(label = label,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)

    label=config.get_localized_string(30001)
    thumbnail=''
    url = tools.build_url({'action':'BPeliculas','url_':''})
    tools.addItemMenu(label = label,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)

    label=config.get_localized_string(30002)
    thumbnail=''
    url = tools.build_url({'action':'BSeries','url_':''})
    tools.addItemMenu(label = label,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)
    
    label='Latelete.tv'
    thumbnail=''
    url = tools.build_url({'action':'lateletetv','url_':''})
    tools.addItemMenu(label = label,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)
    
    label=config.get_localized_string(30003)
    thumbnail=''
    url = tools.build_url({'action':'configurar','url_':''})
    tools.addItemMenu(label = label,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)
    
def bpeliculasmenu():
    label=config.get_localized_string(30004)
    thumbnail=''
    url = tools.build_url({'action':'BPAnadidos','url_':''})
    tools.addItemMenu(label = label,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)
    label=config.get_localized_string(30005)
    thumbnail=''
    url = tools.build_url({'action':'BPCategoria','url_':''})
    tools.addItemMenu(label = label,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)
    label=config.get_localized_string(30006)
    thumbnail=''
    url = tools.build_url({'action':'BPNoVistos','url_':''})
    tools.addItemMenu(label = label,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)
    label=config.get_localized_string(30007)
    thumbnail=''
    url = tools.build_url({'action':'BPSagas','url_':''})
    tools.addItemMenu(label = label,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)
    label=config.get_localized_string(30008)
    thumbnail=''
    url = tools.build_url({'action':'BPGeneros','url_':''})
    tools.addItemMenu(label = label,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)


def bpcategoriamenu():
    label=config.get_localized_string(30008)
    thumbnail=''
    url = tools.build_url({'action':'BPGeneros','url_':''})
    tools.addItemMenu(label = label,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)
    label=config.get_localized_string(30009)
    thumbnail=''
    url = tools.build_url({'action':'BPCTitulo','url_':''})
    tools.addItemMenu(label = label,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)
    label=config.get_localized_string(30010)
    thumbnail=''
    url = tools.build_url({'action':'BPCAnyo','url_':''})
    tools.addItemMenu(label = label,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)


def bseriesmenu():
    label=config.get_localized_string(30011)
    thumbnail=''
    url = tools.build_url({'action':'BSEnProgreso','url_':''})
    tools.addItemMenu(label = label,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)
    label=config.get_localized_string(30005)
    thumbnail=''
    url = tools.build_url({'action':'BSCategoria','url_':''})
    tools.addItemMenu(label = label,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)
    label=config.get_localized_string(30006)
    thumbnail=''
    url = tools.build_url({'action':'BSNoVistos','url_':''})
    tools.addItemMenu(label = label,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)
    label=config.get_localized_string(30008)
    thumbnail=''
    url = tools.build_url({'action':'BSGeneros','url_':''})
    tools.addItemMenu(label = label,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)

def bscategoriamenu():
    label=config.get_localized_string(30008)
    thumbnail=''
    url = tools.build_url({'action':'BSGeneros','url_':''})
    tools.addItemMenu(label = label,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)
    label=config.get_localized_string(30009)
    thumbnail=''
    url = tools.build_url({'action':'BSCTitulo','url_':''})
    tools.addItemMenu(label = label,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)
    label=config.get_localized_string(30010)
    thumbnail=''
    url = tools.build_url({'action':'BSCAnyo','url_':''})
    tools.addItemMenu(label = label,thumbnail= thumbnail, url= url,IsPlayable = 'false', isFolder= True)
