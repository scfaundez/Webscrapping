# -*- coding: utf-8 -*-
"""chile_autos.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11aZdqzCPGqDkzwTOiyKwTZY7kUMAtZy-
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

def cars(marca,pages,region):

    urls = []
    modelo = []
    prices = []
    kilometros = []
    color = []
    body = []
    combustible = []
    cilindros = [] 
    distribuidor = []
    status = []
    identificador=[]

    print("Web Scraping Chile Autos")

    print(f"Buscando {region} para {marca}....")

    #Iterar por pagina para encontrar las urls de cada oferta de depto y almacenar los resultados en una lista llamada urls
    for i in range(0,pages*12,12):
        main_url = 'https://www.chileautos.cl/vehiculos/autos-vehículo/'+ marca.lower().replace(" ","-") + '/'+ region.lower().replace(" ","-")+ '-región' +'/?offset='+ str(i)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        main_response = requests.get(main_url, headers=headers)
        main_soup = BeautifulSoup(main_response.text,'html.parser')
        containers = main_soup.find_all('div',{'class':'listing-item standard'})


        for container in containers: 
            urls.append(container.find('a',class_='js-encode-search')['href'])

    linkbase='https://www.chileautos.cl'
    urls = [linkbase + s  for s in urls]     
    counter = 0 
    for url in urls:
        response = requests.get(url,allow_redirects=False, headers=headers)
        sleep(0.05)
        soup = BeautifulSoup(response.text,'html.parser')
        divi = soup.find_all('div', attrs={'class': 'key-details-item'})

        counter +=1
        
        #Guardar informacion

        try:
            modelo.append(soup.find('div',class_='col features-item-value features-item-value-vehculo').text.strip())
        except (AttributeError,IndexError):
            modelo.append(np.nan)
    
        try: 
            prices.append(soup.find('div',class_='col features-item-value features-item-value-precio').text.strip())
        except (AttributeError,IndexError):
            prices.append(np.nan)

        try: 
            kilometros.append(soup.find('div',class_='col features-item-value features-item-value-kilmetros').text.strip())
        except (AttributeError,IndexError):
            kilometros.append(np.nan)

        try: 
            color.append(soup.find('div',class_='col features-item-value features-item-value-color').text.strip())
        except (AttributeError,IndexError):
            color.append(np.nan)

        try: 
            body.append(soup.find('div',class_='col features-item-value features-item-value-body').text.strip())
        except (AttributeError,IndexError):
            body.append(np.nan)

        try: 
            combustible.append(soup.find('div',class_='col features-item-value features-item-value-combustible').text.strip())
        except (AttributeError,IndexError):
            combustible.append(np.nan)

        try: 
            cilindros.append(soup.find('div',class_='col features-item-value features-item-value-cilindros').text.strip())
        except (AttributeError,IndexError):
            cilindros.append(np.nan)

        try: 
            distribuidor.append(soup.find('span',class_='adtype-value').text)
        except (AttributeError,IndexError):
            distribuidor.append(np.nan)

        try: 
            status.append(soup.find('div',class_='car-not-available-banner').text)
        except (AttributeError,IndexError):
            status.append(np.nan)

        try: 
            identificador.append(soup.find('ul',class_='data-network-id').text)
        except (AttributeError,IndexError):
            identificador.append(np.nan)



        #Clausula para mantener cantidad de variables por cada oferta de departamento, en caso de no existir esa variable se llena con nan
        if len(modelo) != counter:
            modelo.append(np.nan)
        if len(prices) != counter:
            prices.append(np.nan)
        if len(kilometros) != counter:
            kilometros.append(np.nan)
        if len(color) != counter:
            color.append(np.nan)
        if len(body) != counter:
            body.append(np.nan)
        if len(combustible) != counter:
            combustible.append(np.nan)
        if len(cilindros) != counter:
            cilindros.append(np.nan)
        if len(distribuidor) != counter:
            distribuidor.append(np.nan)
        if len(status) != counter:
            status.append(np.nan)
        if len(identificador) != counter:
            identificador.append(np.nan)
        
        print(f"Marcas en {marca} encontrados: {len(modelo)}")
        clear_output(wait=True)

    print(f"Total informacion extraida de automoviles en {marca}: {len(modelo)}")
    print('Web Scraping Completado!\n')
    

    df = pd.DataFrame({'fecha descarga':date.today(),'modelo':modelo,'prices':prices,
                    'kilometros':kilometros, 'color':color,'body':body,'combustible':combustible,'cilindros':cilindros,'distribuidor':distribuidor, 'url':urls, 'status':status})


    return df

appended_data = []

region1 = ['Antofagasta',
            'Araucanía',
            'Arica y Parinacota',
            'Atacama',
            'Aysén',
            'Bío Bío',
            'Coquimbo',
            'Los Lagos',
            'Los Ríos',
            'Magallanes y Antártica Chilena',
            'Maule',
            'Metropolitana de Santiago',
            'OHiggins',
            'Tarapacá',
            'Valparaíso']


marca1=['Aston Martin',
        'Audi',
        'Baic',
        'BMW',
        'Brilliance',
        'Changan',
        'Chery',
        'Chevrolet',
        'Citroen',
        'Citroen',
        'Dfm',
        'Dfsk',
        'Dodge',
        'Dongfeng',
        'Ds',
        'Faw',
        'Ferrari',
        'Fiat',
        'Ford',
        'Foton',
        'Geely',
        'Great Wall',
        'Haval',
        'Honda',
        'Hyundai',
        'INFINITI',
        'Iveco',
        'Jac',
        'Jaguar',
        'Jeep',
        'Jmc',
        'Kia',
        'Kyc',
        'Lada',
        'Land Rover',
        'Lexus',
        'Lifan',
        'Mahindra',
        'Maserati',
        'Maxus',
        'Mazda',
        'Mercedes Benz',
        'MG',
        'MINI',
        'Mitsubishi',
        'Mitsubishi-Fuso',
        'Nissan',
        'Opel',
        'Peugeot',
        'Porsche',
        'Ram',
        'Renault',
        'Seat',
        'SKODA',
        'SsangYong',
        'Subaru',
        'Suzuki',
        'Toyota',
        'Uaz',
        'Volkswagen',
        'Volvo',
        'Zxauto']

for i in region1:
    for j in marca1:
            df=cars(j,100,i)
            df['region'] = i
            df['marca'] = j
            appended_data.append(df)

appended_data = pd.concat(appended_data, ignore_index=True)

z='automoviles_raw'
appended_data.to_excel("%s.xlsx" % z)

df=pd.read_excel('/content/automoviles_raw.xlsx', index_col=0)

#limpiar variables numeros de string
df['prices'] = df['prices'].str.replace('$','')
df['prices'] = df['prices'].str.replace('.','')
df['prices'] = df['prices'].str.replace('CLP','')
df['prices'] = df['prices'].str.replace(' usd','')
df['prices'] = df['prices'].str.lower()
df['combustible'] = df['combustible'].str.replace('Diesel (petróleo)','Diesel')
df['kilometros'] = df['kilometros'].str.replace('.','')
df['kilometros'] = df['kilometros'].str.replace('km','')

#Formatear algunas variables
df['distribuidor'] = df['distribuidor'].str.split('-').str[0]
df['marca'] = df['marca'].str.title()
df['color'] = df['color'].str.title()
df['modelo'] = df['modelo'].str.title()
df['agno'] = df['modelo'].str.split(' ').str[0]
df['modelo'] = df['modelo'].str.replace('\d+', '')
df['modelo'] = df['modelo'].str.strip()
df['marca'] = df['marca'].str.strip()
df['modelo'] = df['modelo'].str.replace('-','')
df['agno'] = df['agno'].str.replace(r'\D', '')
df['prices'] = df['prices'].str.replace(' usd','')

#convertir a floats or int
df['prices'] = df['prices'].astype(float)
df['kilometros'] = df['kilometros'].astype(float)
df['cilindros'] = df['cilindros'].astype(float)

df.to_excel("automoviles.xlsx")
df.to_stata("automoviles.dta")