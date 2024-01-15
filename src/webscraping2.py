from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import traceback
from datetime import datetime
def webscraping(url_scraping, categoria_scraping='todas'):
    options = Options()
    options.headless = False  # Cambia a True para no mostrar el navegador
    driver = webdriver.Chrome(options=options)
    driver.get(url_scraping)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card-news")))
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        noticias = soup.find_all('article', class_='card-news')
        if not noticias:
            print("No se encontraron artículos de noticias. Revisa los selectores.")
            driver.quit()
            return set()

    except Exception as e:
        print(f"Error durante la carga de la página o el análisis: {traceback.format_exc()}")
        driver.quit()
        return set()

    categorias = set()
    for articulo in noticias:
        try:
            url_noticia = articulo.find('a')['href']
            titulo = articulo.find('a').get_text(strip=True)

            # Suponiendo que la categoría es parte de la URL (ajustar según la estructura real)
            categoria = url_noticia.split('/')[3] if len(url_noticia.split('/')) > 3 else 'Desconocida'
            categorias.add(categoria)

            # Suponiendo que la fecha está incluida en la URL o en algún elemento dentro del artículo
            fecha_texto = url_noticia.split('--')[1][:8] if '--' in url_noticia else 'FechaDesconocida'
            try:
                fecha = datetime.strptime(fecha_texto, '%Y%m%d').strftime('%Y-%m-%d')
            except ValueError:
                fecha = 'FechaDesconocida'

            if categoria_scraping == 'todas' or categoria == categoria_scraping:
                print(f"Título: {titulo}, URL: {url_noticia}, Categoría: {categoria}, Fecha: {fecha}")
                # Aquí puedes añadir el código para escribir en un archivo o hacer lo que necesites con los datos
        except Exception as e:
            print(f"Error al procesar un artículo: {e}")

    driver.quit()
    return categorias


# Ejemplo de uso
categorias = webscraping('https://www.telemadrid.es', 'todas')
print("Categorías disponibles:", categorias)
