#######################################################################
## Script en python para hacer webscraping en sitio web de productos ##
## Autor: <Gregorio Bolivar> elalconxvii@gmail.com                   ##
########################################################################
# Paquete para hacer los request
import requests

# Paquete para usabilidad de json
import json

# Paquete para hacer el webcraping
from bs4 import BeautifulSoup

# Paquete para hacer descarga de archivos
#import wget

# Paquete para poder verificar si existe carpetas o archivos
import pathlib

# Para manipular archivos del sistema
import os

# url de la web
web = 'https://www.cheaplaptopkeyboard.com'
    
# Extraer la url del iem
url = (web).strip()
# Definir json
dataJson = {}
# Request a la url del item
page = requests.get(url)
# Webcraping 
soup = BeautifulSoup(page.content, 'html.parser')
# Buscar contenido en la pagina principal
for content in soup.find_all('li', class_='category_top'):
    # Extraer los a > href
    cont = content.find_all('a')
    # hacer busqueda independiente para extraer las categorias de cada item
    # Extraer la url del iem
    urlLink = (cont[0].get('href')).strip()
    # Request a la url del item
    pageCategory = requests.get(urlLink)
    # Webcraping
    soupCategory = BeautifulSoup(pageCategory.content, 'html.parser')
    # Categoria 
    category = soupCategory.select("div#category_description div.centerBoxHeader")[0].string
    # Detalle de la categoria
    categoryDescription = soupCategory.select("div#category_description div.centerBoxContent")[0].string
    # Extraer las Marca
    marca = category.split(' ')[0]
    dataJson['marca'] = marca
    dataJson['marcaDescripcion'] = categoryDescription
    dataJson['products'] = []
    path = os.getcwd() + os.sep + 'products' + os.sep + marca
    print(marca)
    try:
        os.stat(path)
    except:
        os.mkdir(path)

    # buscar los nodos donde esta la categoria
    for contentCategory in soupCategory.find_all('div', id='part_number'):
        # Buscar los elementos de cada item donde esta la categorias independientes
        contCat = contentCategory.find_all('ul', class_='modelsList')
        cont = 0
        for contentModel in contCat[0].find_all('li'):
            # Url del detalle del producto
            urlItem = (contentModel.find_all('a')[0].get('href')).strip()
            # Hacer la peticion del detalle del producto
            pageItem = requests.get(urlItem)
            
            # Mantener el contenido html para hacer busqueda de lo que se quiere obtener
            soupItem = BeautifulSoup(pageItem.content, 'html.parser')
            # extraer Title fotos, nombre, descripcion , categorias y marcas
            title = soupItem.select("title")[0].string
            model = title.split(' ')[1]
            name = soupItem.select("div > #productsName")[0].string
            img = soupItem.select("div#productsImage a ")[0].get('href')
            label = soupItem.select("div#productsDes div#productIntroduction h3")[0].text
            description = soupItem.select("div#productsDes div#productIntroduction div")[0].text
            # Create item object
            dataJson['products'].append({
                'title': title,
                'model': model,
                'name': name,
                'img': img,
                'label': label,
                'description': description,
            })
            print(name)
    saveFile = path + os.sep + marca.lower() + '-data.json'
    with open(saveFile, "w") as f:
        json.dump(dataJson, f)
