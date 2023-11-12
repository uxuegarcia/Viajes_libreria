# Viajes_libreria
Esta es una librería que proporciona información de interes de lugares. Con el objetivo de facilitar la obtencion de informacion para viajeros como informacion meteorológica, turística, monetaria y una calculadora de distancia entre dos lugares.

## Instalación
Puedes instalar la librería usando pip: pip install LibreriaViajes_UxueAinara

## Uso
from LibreriaViajes_UxueAinara import DestinoInfo, CalculadoraDeDistancia, ConversorDeMoneda

### Ejemplo de uso de la información meteorológica
info_meteorologica = DestinoInfo().obtener_datos_meteorologicos("Bilbao")

### Ejemplo de uso de la información turística
info_turistica = DestinoInfo().obtener_informacion_turistica("Bilbao", "Restaurant")

### Ejemplo de uso de la calculadora de distancia
distancia_entre_lugares = CalculadoraDeDistancia("Bilbao", "San Sebastian").calcular_distancia()

### Ejemplo de uso del conversor de moneda
cambio_moneda = ConversorDeMoneda().cambio_moneda("USD", "EUR", cantidad=100)
