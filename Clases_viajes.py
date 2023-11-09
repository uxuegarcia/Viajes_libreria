import requests
from termcolor import colored
import re
import math



class DestinoInfo:
    def __init__(self):
        self.api_key = 'f7798c316c84f5f6cfb22b5c09464ecc'

    def obtener_coordenadas(self, ciudad):
        try:
            url = f'https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={self.api_key}'
            response = requests.get(url)
            data = response.json()
            coordenadas = data['coord']
            return coordenadas
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error al obtener coordenadas: {e}")

    def obtener_datos_meteorologicos(self, ciudad):
        try:
            url = f'https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={self.api_key}'
            response = requests.get(url)
            if response.status_code == 200:
                datos = response.json()
                descripcion = datos['weather'][0]['description']
                temp_min = datos['main']['temp_min']
                temp_max = datos['main']['temp_max']
                humedad = datos['main']['humidity']
                velocidad_viento = datos['wind']['speed']

                informacion = colored("Información Meteorológica:", 'green', attrs=['bold'])
                descripcion = colored(f'Tipo de tiempo: {descripcion}', 'blue')
                temp_min = colored(f'Temperatura mínima: {temp_min} K', 'blue')
                temp_max = colored(f'Temperatura máxima: {temp_max} K', 'blue')
                humedad = colored(f'Humedad: {humedad}%', 'blue')
                velocidad_viento = colored(f'Velocidad del viento: {velocidad_viento} m/s', 'blue')

                texto = f"{informacion}\n{descripcion}\n{temp_min}\n{temp_max}\n{humedad}\n{velocidad_viento}"
                return texto  # información meteorológica
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error al obtener datos meteorológicos: {e}")


    def obtener_informacion_turistica(self, ciudad, query):
            try:
                coordenadas = self.obtener_coordenadas(ciudad)
                latitud = coordenadas['lat']
                longitud = coordenadas['lon']

                url = "https://api.foursquare.com/v3/places/search"
                params = {
                    "query": f"{query}",
                    "ll": f"{latitud},{longitud}",
                    "open_now": "true",
                    "sort": "DISTANCE"
                }
                headers = {
                    "Accept": "application/json",
                    "Authorization": "fsq3I2mQyodMw6hvp10dHnfQ9qQTmxKzt/po8Q3Vzf2tzfg=" 
                }
                response = requests.get(url, params=params, headers=headers)
                data = response.json()
                results = data.get('results', [])
                if not results:
                    raise KeyError("No se encontraron lugares de interés cercanos.")

                informacion_turistica = colored("Información Turística:", attrs=['bold'])
                lugares_interes = []
                for result in results[:7]:  # Tomamos los primeros 7 resultados
                    categories = result.get('categories', [])
                    formatted_address = result.get('location', {}).get('formatted_address', 'Dirección no disponible')
                    formatted_address = re.sub(r',[^,]*$', '', formatted_address)
                    for category in categories:
                        category_name = category['name']
                        category_name = colored(category_name, attrs=['bold'])
                        lugar_info = f'{category_name}, Dirección: {formatted_address}'
                        lugares_interes.append(lugar_info)

                lugares_interes_texto = "\n".join(lugares_interes)
                print(f"{informacion_turistica}\n{lugares_interes_texto}")
                return lugares_interes
            except requests.exceptions.RequestException as e:
                raise Exception(f"Error al obtener información turística: {e}")
            

class CalculadoraDeDistancia(DestinoInfo):
    def __init__(self, lugar1, lugar2):
        self.lugar1 = lugar1
        self.lugar2 = lugar2
        self.earth_radius = 6371  # Radio promedio de la Tierra en kilómetros
        super().__init__(api_key)

    def validar_coordenadas(self, lat, lon):
        try:
            lat = float(lat)
            lon = float(lon)
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                return lat, lon
            else:
                raise ValueError("Las coordenadas deben estar dentro de los rangos válidos.")
        except ValueError:
            raise ValueError("Las coordenadas deben ser valores numéricos válidos.")

    def haversine_distance(self, ciudad):
        try:
            coordenadas = super().obtener_coordenadas(ciudad)

            latitud = coordenadas['lat']
            longitud = coordenadas['lon']
            latitud, longitud = self.validar_coordenadas(latitud, longitud)
            return latitud, longitud
        except (ValueError, Exception) as e:
            raise ValueError(f"Error al obtener coordenadas del {ciudad}: {e}")

    def calcular_distancia(self):
        try:
            lat1, lon1 = self.haversine_distance(self.lugar1)
            lat2, lon2 = self.haversine_distance(self.lugar2)

            # Convertir grados a radianes
            lat1_rad = math.radians(lat1)
            lon1_rad = math.radians(lon1)
            lat2_rad = math.radians(lat2)
            lon2_rad = math.radians(lon2)

            # Diferencia en latitud y longitud
            dlat = lat2_rad - lat1_rad
            dlon = lon2_rad - lon1_rad

            # Fórmula de Haversine
            a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            distance = self.earth_radius * c

            return distance
        except ValueError as e:
            raise ValueError(f"Error al calcular la distancia: {e}")
        
class ConversorDeMoneda:
    def __init__(self):
        self.api_key = '5d62ec629d544bd89f8cd6ac75196b8b'

    def cambio_moneda(self, base_currency, target_currency, cantidad=1):
        if not isinstance(base_currency, str) or not isinstance(target_currency, str):
            raise TypeError("Los acrónimos de moneda deben ser cadenas de texto.")

        url = f'https://openexchangerates.org/api/latest.json?app_id={self.api_key}&base={base_currency}'

        try:
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            exchange_rate = data['rates'][target_currency]
            converted_amount = cantidad * exchange_rate
            return f'{cantidad} {base_currency} equivale a {converted_amount} {target_currency}'

        except requests.exceptions.RequestException as e:
            return f"Error en la solicitud a la API. Código de respuesta: {response.status_code}"
