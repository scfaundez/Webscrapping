# -*- coding: utf-8 -*-
"""lider.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_4TsSODY-AoYN0WftLrvRaH3fT1NAGTI
"""

#Instalar/importal librerías
!pip install xlsxwriter
!pip install selenium
!apt-get update # to update ubuntu to correctly run apt install
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin

from numpy.core.fromnumeric import amin
import requests
from bs4 import BeautifulSoup
from datetime import date
import re 
import numpy as np 
import pandas as pd 
from IPython.display import clear_output
from time import sleep

def super(pages):

    referencia = []
    marca = []
    price = []
    cantidad = []
    producto = []
    categoria = []
    tipo_producto = []
    urls = []

    print("Web Scraping en supermercado Lider!")

    

    #Iterar por pagina para encontrar las urls de cada oferta de depto y almacenar los resultados en una lista llamada urls
    for i in range(1,pages*80,80):
      main_url = 'https://www.lider.cl/supermercado/category/?No='+ str(i-1) + '&isNavRequest=Yes&Nrpp=' + '80&page=' + str(pages)
      main_response = requests.get(main_url)
      main_soup = BeautifulSoup(main_response.text, 'lxml')
      containers = main_soup.find_all('div',{'class':'responsive-holder-xs'})

      for container in containers:
        urls.append(container.find('a',class_='product-link')['href'])

    urls=list(set(urls))
    linkbase='https://www.lider.cl'
    urls = [linkbase + s  for s in urls]   
       
    counter = 0 
    for url in urls:
        response = requests.get(url,allow_redirects=False)
        sleep(0.05)
        soup = BeautifulSoup(response.text,'lxml')
        divi = soup.find("div", {"id": "productPrice"})
        encabezado = soup.find("ol", {'class': 'breadcrumb col-md-12 hidden-xs'})
        print(f"Buscando en producto {counter} / {pages*80} ...")
        counter +=1
        

        #Guardar informacion de productos

        try:
          referencia.append(soup.find('span', itemprop='productID').text.strip())
        except (AttributeError,IndexError):
          referencia.append(np.nan)

        try:
          marca.append(soup.find('span', itemprop='brand').text.strip())
        except (AttributeError,IndexError):
          marca.append(np.nan)

        try:
          price.append(divi.find('p', {"class":"price"}).text.strip())
        except (AttributeError,IndexError):
          price.append(np.nan)

        try:
          divi2 = soup.find("div", {"class": "product-info col-lg-3 col-md-5 col-sm-5 col-xs-10"})
          cantidad.append(divi2.select_one('span + span + span').text.strip())
        except (AttributeError,IndexError):
          cantidad.append(np.nan)

        try:
          producto.append(soup.find('span', itemprop='name').text.strip())
        except (AttributeError,IndexError):
          producto.append(np.nan)

        try:
          table = soup.find("table",{"class":"table table-striped"})
          table_rows = table.find_all('tr')
          l = []
          for tr in table_rows:
            td = tr.find_all('td')
            row = [i.text for i in td]
            l.append(row)
          key_row1 = [x for x in l if x[0] == (('Tipo Productos') or ('Producto'))]
          key_row=key_row1[0]
          key_type=key_row[1]
          tipo_producto.append(key_type)
        except (AttributeError,IndexError):
          tipo_producto.append(np.nan)

        try:
          categoria.append(encabezado.select_one('span').text.strip())
        except (AttributeError,IndexError):
          categoria.append(np.nan)




        #Clausula para mantener cantidad de variables por cada oferta de departamento, en caso de no existir esa variable se llena con nan
        if len(referencia) != counter:
            referencia.append(np.nan)
        if len(marca) != counter:
            marca.append(np.nan)
        if len(price) != counter:
            price.append(np.nan)
        if len(cantidad) != counter:
            cantidad.append(np.nan)
        if len(producto) != counter:
            producto.append(np.nan)
        if len(tipo_producto) != counter:
            tipo_producto.append(np.nan)
        if len(categoria) != counter:
            categoria.append(np.nan)
        
        #print(f"Marcas en {marca} encontrados: {len(modelo)}")
        clear_output(wait=True)

    #print(f"Total informacion extraida de productos en {pages}: {len(pages)} y producto {referencia}")
    print('Web Scraping Completado!\n')
    

    df = pd.DataFrame({'fecha descarga':date.today(),'ID_Producto':referencia,'Marca':marca, 'Precio':price, 'Cantidad':cantidad, 'Nombre_Producto':producto,'Tipo_Producto':tipo_producto, 'url':urls, 'categoria':categoria})


    return df

appended_data = []
pages=385
df=super(pages)
appended_data.append(df)
appended_data = pd.concat(appended_data, ignore_index=True)
appended_data.to_excel("lider.xlsx")
df = pd.read_excel("/content/drive/MyDrive/bases_datos/lider_raw282021.xlsx")

df = pd.read_excel("/content/drive/MyDrive/bases_datos/lider_raw262021.xlsx")

#limpiar variables numeros de string
df['Precio'] = df['Precio'].str.replace('$','')
df['Precio'] = df['Precio'].str.replace('.','')
df['Precio'] = df['Precio'].str.replace(',','.')
df['Cantidad'] = df['Cantidad'].str.replace(',','.')
df['Precio'] = df['Precio'].astype(float)
df = df.drop(['Unnamed: 0'], axis=1)

new = df["Cantidad"].str.split(" ", n = 1, expand = True)
df["Cantidades"]= new[0]
df["Unidades"]= new[1]

df["Cantidades"]= new[0]
df["Unidades"]= new[1]

df.to_excel('/content/drive/MyDrive/bases_datos/lider.xlsx')