import os
import time
import re
import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FacebookScraper:
    def __init__(self, driver_path: str, email: str, password: str):
        """
        Inicializa el scraper de Facebook.

        Args:
            driver_path (str): Ruta al msedgedriver.
            email (str): Correo de Facebook.
            password (str): Contraseña de Facebook.
        """
        self.service = Service(driver_path)
        self.options = Options()
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--disable-notifications")
        self.driver = webdriver.Edge(service=self.service, options=self.options)
        self.wait = WebDriverWait(self.driver, 20)
        self.email = email
        self.password = password

    def wait_and_find_element(self, by: By, value: str, timeout: int = 20):
        """
        Espera y busca un elemento en la página.

        Args:
            by (By): Mecanismo para buscar el elemento.
            value (str): Valor o selector del elemento.
            timeout (int, optional): Tiempo máximo de espera. Defaults to 20.

        Returns:
            WebElement o None: El elemento encontrado o None en caso de timeout.
        """
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:
            logging.error(f"Timeout esperando elemento: {value}")
            return None

    def login(self) -> bool:
        """
        Realiza el login en Facebook.

        Returns:
            bool: True si el login fue exitoso, False en caso contrario.
        """
        try:
            self.driver.get("https://www.facebook.com")
            email_input = self.wait_and_find_element(By.ID, "email")
            password_input = self.wait_and_find_element(By.ID, "pass")

            if not email_input or not password_input:
                raise Exception("No se encontraron los campos de login")

            email_input.send_keys(self.email)
            password_input.send_keys(self.password)

            login_button = self.wait_and_find_element(By.NAME, "login")
            if login_button:
                login_button.click()
                time.sleep(40)  # Espera a que se complete el login
                logging.info("Login exitoso")
                return True
            else:
                raise Exception("Botón de login no encontrado")
        except Exception as e:
            logging.error(f"Error en login: {e}")
            return False

    def search_term(self, search_term: str) -> bool:
        """
        Realiza una búsqueda de posts con un término específico.

        Args:
            search_term (str): Término a buscar.

        Returns:
            bool: True si la búsqueda se realizó correctamente, False en caso de error.
        """
        try:
            search_url = f"https://www.facebook.com/search/posts/?q={search_term.replace(' ', '%20')}"
            self.driver.get(search_url)
            time.sleep(5)  # Espera a que carguen los resultados
            logging.info("Búsqueda realizada correctamente")
            return True
        except Exception as e:
            logging.error(f"Error en búsqueda: {e}")
            return False

    def extract_posts(self, num_posts: int = 20):
        """
        Extrae un número determinado de posts.

        Args:
            num_posts (int, optional): Número de posts a extraer. Defaults to 20.

        Returns:
            list: Lista de diccionarios con la información de cada post.
        """
        posts_data = []
        scroll_attempts = 0
        max_scroll_attempts = 5

        try:
            while len(posts_data) < num_posts and scroll_attempts < max_scroll_attempts:
                # Buscar todos los posts visibles
                posts = self.driver.find_elements(By.XPATH, "//div[@role='article']")
                
                for post in posts:
                    if len(posts_data) >= num_posts:
                        break

                    try:
                        # Extraer el autor
                        try:
                            author = post.find_element(By.CSS_SELECTOR, "strong.html-strong span.x11i5rnm").text
                        except NoSuchElementException:
                            author = "Autor no disponible"
                        
                        # Extraer el link de la publicación
                        try:
                            link = post.find_element(By.XPATH, ".//a[contains(@href, '/posts/')]").get_attribute("href")
                        except NoSuchElementException:
                            link = "Link no disponible"

                        # Extraer la fecha
                        try:
                            date = post.find_element(By.CSS_SELECTOR, "span.xt0b8zv.x1rg5ohu").text
                        except NoSuchElementException:
                            date = "Fecha no disponible"

                        # Extraer el contenido
                        try:
                            content = post.find_element(By.CSS_SELECTOR, "span.x1yc453h.xzsf02u.xo1l8bm").text
                        except NoSuchElementException:
                            content = "Contenido no disponible"

                        # Extraer el número de reacciones
                        try:
                            reactions = post.find_element(By.XPATH, ".//span[contains(text(), 'reacción')]").text
                        except NoSuchElementException:
                            reactions = "Reacciones no disponibles"

                        # Extraer comentarios (si están visibles)
                        comments = []
                        try:
                            comment_elements = post.find_elements(By.XPATH, ".//div[contains(@aria-label, 'Comentario')]")
                            for comment in comment_elements:
                                text_comment = comment.text.strip()
                                if text_comment:
                                    comments.append(text_comment)
                        except NoSuchElementException:
                            comments = []

                        # Extraer hashtags del contenido usando regex
                        hashtags = re.findall(r"(#\w+)", content)

                        post_data = {
                            "Autor": author,
                            "Link": link,
                            "Fecha": date,
                            "Contenido": content,
                            "Reacciones": reactions,
                            "Comentarios": comments,
                            "Hashtags": hashtags
                        }

                        # Se verifica que al menos alguno de los datos importantes esté disponible
                        if any(value not in ["Autor no disponible", "Fecha no disponible", "Contenido no disponible", "Link no disponible"] 
                               for value in post_data.values()):
                            if post_data not in posts_data:  # Evitar duplicados
                                posts_data.append(post_data)
                                logging.info(f"Post extraído {len(posts_data)}/{num_posts}")
                                logging.info(f"Autor: {author}")
                                logging.info(f"Fecha: {date}")
                                logging.info(f"Link: {link}")
                                logging.info("-" * 50)

                    except Exception as e:
                        logging.error(f"Error extrayendo post individual: {e}")
                        continue

                # Scroll down para cargar más posts
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                scroll_attempts += 1

                # Hacer clic en "Ver más" si está presente
                try:
                    ver_mas = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Ver más')]")
                    ver_mas.click()
                    time.sleep(2)
                except NoSuchElementException:
                    pass

        except Exception as e:
            logging.error(f"Error en extracción de posts: {e}")

        return posts_data

    def save_to_csv(self, data, filename: str):
        """
        Guarda los datos extraídos en un archivo CSV.

        Args:
            data (list): Datos a guardar.
            filename (str): Nombre del archivo CSV.
        """
        if data:
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            logging.info(f"Datos guardados en {filename}")
            logging.info(f"Total de posts extraídos: {len(data)}")
        else:
            logging.warning("No hay datos para guardar")

    def close(self):
        """Cierra el navegador."""
        self.driver.quit()


def main():
    """
    Función principal para ejecutar el scraper.
    Requiere que se configuren las variables de entorno:
      - DRIVER_PATH: Ruta al driver de Edge.
      - FACEBOOK_EMAIL: Correo electrónico de Facebook.
      - FACEBOOK_PASSWORD: Contraseña de Facebook.
      - SEARCH_TERM: Término de búsqueda (por defecto "aluvión baños").
    """
    driver_path = os.getenv("DRIVER_PATH", "C:\\msedgedriver.exe")
    email = os.getenv("FACEBOOK_EMAIL", "tu_email@ejemplo.com")
    password = os.getenv("FACEBOOK_PASSWORD", "tu_contraseña")
    search_term = os.getenv("SEARCH_TERM", "aluvión baños")
    
    scraper = FacebookScraper(driver_path, email, password)
    
    try:
        if scraper.login():
            time.sleep(3)
            if scraper.search_term(search_term):
                time.sleep(5)
                posts = scraper.extract_posts(num_posts=20)
                scraper.save_to_csv(posts, "facebook_posts.csv")
    finally:
        scraper.close()


if __name__ == "__main__":
    main()
