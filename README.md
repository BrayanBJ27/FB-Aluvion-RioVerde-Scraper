# Facebook Scraper

## Descripción
**Facebook Scraper** es una herramienta en Python que utiliza Selenium para automatizar la extracción de publicaciones en Facebook basadas en un término de búsqueda. El scraper realiza lo siguiente:

- Realiza login automático en Facebook.
- Busca publicaciones según un término especificado.
- Extrae datos de las publicaciones, tales como:
    - Autor
    - Link de la publicación
    - Fecha
    - Contenido
    - Número de reacciones
    - Comentarios
    - Hashtags
- Guarda los datos extraídos en un archivo CSV.

## Requisitos

- **Python 3.7+**
- **Selenium**  
    Instalarlo con:
    ```bash
    pip install selenium
    ```
- **Pandas**  
    Instalarlo con:
    ```bash
    pip install pandas
    ```
- **Driver Web** (msedgedriver o chromedriver)  
    Debes disponer de un driver compatible con el navegador que vayas a utilizar:  
    - Microsoft Edge: Descarga msedgedriver.  
    - Google Chrome: Descarga chromedriver.

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/BrayanBJ27/FB-Aluvion-RioVerde-Scraper.git
cd facebook-scraper
```

Crear un entorno virtual (opcional, pero recomendado):

```bash
python -m venv venv
```

En Linux/Mac:

```bash
source venv/bin/activate
```

En Windows:

```bash
venv\Scripts\activate
```

Instalar las dependencias:

Crea un archivo `requirements.txt` con el siguiente contenido:

```nginx
selenium
pandas
```

Luego, instala las dependencias:

```bash
pip install -r requirements.txt
```

## Configuración

Para evitar dejar tus credenciales en el código, se recomienda utilizar variables de entorno. Configura las siguientes variables:

- `DRIVER_PATH`: Ruta al driver (por ejemplo, `C:\msedgedriver.exe` o `chromedriver.exe`).
- `FACEBOOK_EMAIL`: Tu correo de Facebook.
- `FACEBOOK_PASSWORD`: Tu contraseña de Facebook.
- `SEARCH_TERM`: Término de búsqueda (por defecto "aluvión baños").

Puedes configurarlas directamente en tu sistema o crear un archivo `.env` y utilizar la librería python-dotenv para cargarlas. Ejemplo de archivo `.env`:

```ini
DRIVER_PATH=C:\msedgedriver.exe
FACEBOOK_EMAIL=tu_email@ejemplo.com
FACEBOOK_PASSWORD=tu_contraseña
SEARCH_TERM=aluvión baños
```

## Ejecución

Una vez configuradas las variables de entorno, ejecuta el script:

```bash
python facebook_scraper.py
```

## Advertencia

- **Uso Ético**: Este scraper es para fines educativos. Asegúrate de cumplir con los Términos y Condiciones de Facebook y de utilizarlo de forma responsable.
- **Manejo de Credenciales**: No compartas tus credenciales. Se recomienda utilizar variables de entorno o métodos seguros para su almacenamiento.
- **Ajuste de Tiempos**: Los `time.sleep()` en el código pueden necesitar ajustes según la velocidad de conexión y la respuesta del sitio.

## Estructura del Proyecto

```bash
facebook-scraper/
│
├── facebook_scraper.py      # Script principal del scraper.
├── requirements.txt         # Dependencias del proyecto.
└── README.md                # Documentación del proyecto.
```