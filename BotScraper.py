import telegram, requests
from openpyxl import load_workbook 
from requests_html import HTMLSession

#---------------------------Definicion de funciones -------------------------------------------------

def notificar_telegram(precio1, precio2):
    TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'  
    CHATID = 'xxxxxxxxxxxxxxx'
    TEXTO = f'El teclado Logitech MX keys, ha bajado de precio, antes => {precio1}, ahora => {precio2}'   
    requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHATID}&text={TEXTO}')

def obtener_precio(url,x_path):
    try:
        s = HTMLSession()
        r = s.get(url)
        r.html.render(timeout=20)#Para dar tiempo a que se cargue todo el codigo JavaScript en caso la conexión a internet este lenta
        precio = r.html.xpath(x_path, first=True).text
        return float(precio[4:])
    
    except:
        TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'  
        CHATID = 'xxxxxxxxxxxxxx'
        TEXTO = 'Ups..algo salió mal, revisa el script del botscraper para el seguimiento del teclado'   
        requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHATID}&text={TEXTO}')


def comparar_precio(precio_actual,num_celda):
    PATH = 'D:/A_PYTHON/ProgramasPython/Bot_Scraper/Seguimiento_productos.xlsx'
    archivo_excell = load_workbook(PATH)
    hoja = archivo_excell.get_sheet_by_name('teclado')
    precio_inicial = float(hoja[f'B{num_celda}'].value)

    #La siguiente linea de codigo es para efectos de pruebas y validar los precios.
    print(f'precio inicial: {precio_inicial}'+' ----> '+f'precio actual: {precio_actual}')

    if precio_inicial > precio_actual:
        #Llamamos a la funcion que nos envia una notificacion via telegram 
        #informando que el producto ha bajado de precio. 
        notificar_telegram(precio_inicial, precio_actual)

#----------------------------Llamadas a las funciones-----------------------------------------------------------

URLS_XPATHS = [
    ('https://www.amazon.com/-/es/Teclado-iluminado-inal%C3%A1mbrico-avanzado-Logitech/dp/B08CQ8BYSC/ref=sr_1_2?__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=logitech%2Bmx%2Bkeys&qid=1605249579&sr=8-2&th=1',
    '//*[@id="priceblock_ourprice"]')
    ]

num_celda = 2
for url, xpath in URLS_XPATHS:
    precio_actual = obtener_precio(url,xpath)#Obtenemos el precio que tiene el teclado acutalmente
    comparar_precio(precio_actual,num_celda)#Compraramos el precio inicial con el actual y notificamos si hay rebaja
    num_celda += 1
