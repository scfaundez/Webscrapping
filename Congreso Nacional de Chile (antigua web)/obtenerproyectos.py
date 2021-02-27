#!/usr/bin/env python
# coding: utf-8

# In[35]:


#!/usr/bin/python


import sys, getopt
import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl


def is_number(val):
   try:
      val = int(val)
      return True
   except ValueError:
      return False

def save_file(content,filename):
    with open(filename, "w") as f: 
        f.write(response.content.decode("utf-8")) 

def fetch_document(prmID):
    headers = {
        #'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    url = 'https://www.camara.cl/pley/pley_detalle.aspx'
    data = {'prmID':prmID}
    response = requests.get(url, headers=headers, data=data)
    return response

def fetch_authors(prmID, viewstate, viewstate_generator, eventvalidation):
    headers = {
        'Origin': 'https://www.camara.cl',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'X-Requested-With': 'XMLHttpRequest',
        #'Connection': 'keep-alive',
        'X-MicrosoftAjax': 'Delta=true',
        'Referer': f'https://www.camara.cl/pley/pley_detalle.aspx?prmID={prmID}',
    }

    params = (
        ('prmID', prmID),
    )

    data = {
      'ctl00$mainPlaceHolder$ScriptManager1': 'ctl00$mainPlaceHolder$UpdatePanel1|ctl00$mainPlaceHolder$btnAutores',
      '__EVENTTARGET': 'ctl00$mainPlaceHolder$btnAutores',
      '__EVENTARGUMENT': '',
      '__VIEWSTATE': viewstate,
      '__VIEWSTATEGENERATOR': viewstate_generator,
      '__EVENTVALIDATION': eventvalidation,
      'ctl00$mainPlaceHolder$Tbbusqueda': '',
      '__ASYNCPOST': 'true',
      '': ''
    }

    response = requests.post('https://www.camara.cl/pley/pley_detalle.aspx', headers=headers, params=params, data=data)
    return response

def get_buletin_nro(bs):
    infos = bs.select("table.tabla>tr>th")
    for idx, val in enumerate(infos):
        if val.text=='Numero de boletín:':
            return bs.select("table.tabla>tr>td")[idx].text
    return ''

def get_ultima_fecha_valida(tramit):
    for t in reversed(tramit):
        if t.text.strip()!='':
            return t.text
    return ''

def get_fechas_tramit(bs):
    tramit = bs.select("table.tabla#ctl00_mainPlaceHolder_grvtramitacion>tbody>tr>td:first-child")
    fecha_inicial = fecha_final = ''
    if len(tramit)>=1:
        fecha_inicial = tramit[0].text       
        #En algunos casos, la última línea no contiene fecha. En ese caso toma la ultima valida
        fecha_final = get_ultima_fecha_valida(tramit)
        #fecha_final = get_ultima_fecha_valida(tramit).text
    res = [fecha_inicial, fecha_final]
    return res 

def get_authors(bsa):
    authores = bsa.select("table.tabla>tbody>tr>td:first-child")
    res = [a.text.strip() for a in authores]
    if len(res)==0:
      res.append('')
    return res

def is_maintenance_page(soup):
    is_maintenance = soup.select(".content-head h2")[0].text=='Sitio Web Temporalmente en Mantención'
    return is_maintenance

def parse(start_prmID,end_prmID): 
    df = pd.DataFrame()
    for prmID in range(start_prmID,end_prmID+1):
        try:
            #Obtem documento
            d = fetch_document(prmID)
            bs = BeautifulSoup(d.content, features="html.parser")
            #Se página no existe sigue a siguiente prmID
            if (is_maintenance_page(bs)):
                print(f"Página {prmID} no existe:")
                continue
            viewstate = bs.find("input", {"id": "__VIEWSTATE"}).attrs['value']
            viewstate_generator = bs.find("input", {"id": "__VIEWSTATEGENERATOR"}).attrs['value']
            eventvalidation = bs.find("input", {"id": "__EVENTVALIDATION"}).attrs['value']
            
            #parse document 
            buletin = get_buletin_nro(bs)
            
            #si el boletín no existe es porque no existe prmID. sigue a siguiente
            if buletin==None or buletin=='':
                continue
            
            fechas = get_fechas_tramit(bs)
            fecha_inicial = fechas[0]
            fecha_final = fechas[1]
            
            #fetch Autores
            a = fetch_authors(prmID, viewstate, viewstate_generator, eventvalidation)
            
            #parse autores
            bsa = BeautifulSoup(a.content, features="html.parser")
            autores = get_authors(bsa)

            dados = []
            for autor in autores:
              dados.append([buletin, autor, fecha_inicial, fecha_final]) 
            df = df.append(pd.DataFrame(dados))

        except Exception as e:
            print('Erro - '+str(prmID)+':'+ str(e))      
            raise
        
        
    return df
        

def parse_and_save(start_prmID,end_prmID): 
    df = parse(start_prmID,end_prmID)
    if df.size==0:
      raise Exception("Warning: no se pudo obtener datos. compruebe el intervalo de prmIDs informado")
    df.columns = ['Boletin','Autores','Fecha Inicial','Fecha Final']
    str_start_prmID=str(start_prmID)
    str_end_prmID=str(end_prmID)
    df.to_excel(f"result-{str_start_prmID}-{str_end_prmID}.xlsx", index=False) 


def main(argv):
   usage = 'obtenervotos.py prmID_inicio prmID_final'
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"h")
      if (args==[] or len(args)!=2):
         raise Exception("Error: 2 parámetros obligatorios")
      if not is_number(args[0]) or not is_number(args[1]):
         raise Exception("Error: los 2 parámetros deben ser numéricos y corresponder a un intervalo de prmIDs")
      
   except getopt.GetoptError:
      print(usage)
      sys.exit(2)
   except Exception as e:
      print(e)
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print(usage)
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print("a trabajar... ")
   try:
      parse_and_save(int(args[0]),int(args[1]))
      print(f"Ok. Fichero generado: result-{args[0]}-{args[1]}.xlsx")
   except Exception as e:
      print(str(e))
   


# In[ ]:


#parse_and_save(1299,1300)
#parse_and_save(1252,13252)


# In[ ]:





# In[ ]:


if __name__ == "__main__":
   main(sys.argv[1:])
   

