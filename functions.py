import requests
from bs4 import BeautifulSoup
from lxml import etree
from flask import Flask, jsonify, request

def todo_producto(producto):
    lista_titulos = []
    lista_precios = []
    lista_urls = []
    siguiente = 'https://listado.mercadolibre.com.ar/'+producto
    while True:
        r = requests.get(siguiente)
        if r.status_code == 200:
            boul = BeautifulSoup(r.content, 'html.parser')
            #titulos
            titulo = boul.find_all('h2', {'class': 'ui-search-item__title shops__item-title'})
            titulo = [i.text for i in titulo]
            lista_titulos.extend(titulo)
            #precios
            dom = etree.HTML(str(boul))
            precio = (dom.xpath('//li[@class="ui-search-layout__item shops__layout-item"]//div[@class="ui-search-result__content-wrapper shops__result-content-wrapper"]//div[@class="ui-search-result__content-columns shops__content-columns"]//div[@class="ui-search-result__content-column ui-search-result__content-column--left shops__content-columns-left"]/div[1]/div/div/div//span[@class="price-tag ui-search-price__part shops__price-part"]//span[@class="price-tag-amount"]//span[@class="price-tag-fraction"]'))
            precio = [i.text for i in precio]
            lista_precios.extend(precio)
            # urls
            urls= boul.find_all('a', {'class':'ui-search-item__group__element shops__items-group-details ui-search-link'})
            urls = [i.get('href') for i in urls]
            lista_urls.extend(urls)
            #validar
            init = boul.find('span', {"class":'andes-pagination__link'}).text
            init = int(init)
            end = boul.find('li', {'class':'andes-pagination__page-count'})
            end = int(end.text.split(" ")[1])
            
        else:
            break
        print(init, end)

        if init == end:
            break
        siguiente = dom.xpath('//div[@class="ui-search-pagination shops__pagination-content"]/ul/li[contains(@class,"--next")]/a')[0].get('href')
    return lista_titulos, lista_precios, lista_urls



def producto_acortado(producto,limite):
    lista_titulos = []
    lista_precios = []
    lista_urls = []
    siguiente = 'https://listado.mercadolibre.com.ar/'+producto
    while True:
        r = requests.get(siguiente)
        if r.status_code == 200:
            boul = BeautifulSoup(r.content, 'html.parser')
            #titulos
            titulo = boul.find_all('h2', {'class': 'ui-search-item__title shops__item-title'})
            titulo = [i.text for i in titulo]
            lista_titulos.extend(titulo)
            #precios
            dom = etree.HTML(str(boul))
            precio = (dom.xpath('//li[@class="ui-search-layout__item shops__layout-item"]//div[@class="ui-search-result__content-wrapper shops__result-content-wrapper"]//div[@class="ui-search-result__content-columns shops__content-columns"]//div[@class="ui-search-result__content-column ui-search-result__content-column--left shops__content-columns-left"]/div[1]/div/div/div//span[@class="price-tag ui-search-price__part shops__price-part"]//span[@class="price-tag-amount"]//span[@class="price-tag-fraction"]'))
            precio = [i.text for i in precio]
            lista_precios.extend(precio)
            # urls
            urls= boul.find_all('a', {'class':'ui-search-item__group__element shops__items-group-details ui-search-link'})
            urls = [i.get('href') for i in urls]
            lista_urls.extend(urls)
            #validar
            init = boul.find('span', {"class":'andes-pagination__link'}).text
            init = int(init)
            end = boul.find('li', {'class':'andes-pagination__page-count'})
            end = int(end.text.split(" ")[1])
            
        else:
            print("Algo salió mal")
            break
        print(init, end)
        if len(lista_titulos)>=int(limite):
            return lista_titulos[:limite], lista_precios[:limite], lista_urls[:limite]
        if init == end:
            break
        siguiente = dom.xpath('//div[@class="ui-search-pagination shops__pagination-content"]/ul/li[contains(@class,"--next")]/a')[0].get('href')
    return lista_titulos, lista_precios, lista_urls
