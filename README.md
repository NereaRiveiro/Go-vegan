# Go vegan?

## Proyecto de análisis y visualización de datos

![Alt text](images/streamlit/logof.png)

## Índice

1. [🗺️ Descripción](#descripcion)
2. [🏔️ Objetivo](#objetivo)
3. [🌀 Análisis](#analisis)
4. [🧗‍♀️ Conclusiones](#conclusion)
5. [🧊 Estructura](#estructura)


## 🗺️ Descripción:<a name="descripcion"/>

Proyecto final de análisis y visualización como Data Analyst en Ironhack. 

Con este proyecto se propone la práctica del proceso de análisis de datos. Para ello hemos creado una web interactiva mediante la que el usuario puede medir su impacto ecológico según su alimentación.

Para poder acceder a la web dejamos el siguiente enlace:

- [Mapa](https://nereariveiro-go-vegan--streamlitmain-ky4jxb.streamlit.app/)

## 🏔️ Objetivo:<a name="objetivo"/>

El cambio climático es una preocupación constante en el panorama actual, cada día vemos cómo las consecuencias marcan nuestro día a día y está en nuestras manos el cambio. Por ello, nos hemos plantea

- ¿En qué zona se encuentran las cumbres?
- ¿Cuál es la montaña con más riesgo de fallecimiento?
- ¿Según qué época es mas letal subirlas? ¿Y cada una de ellas?
- ¿Hay alguna nacionalidad que se pone más en riesgo al intentar llegar a la cumbre?
- ¿Cuáles son las causas de muerte más comunes?
- ¿Puede haber alguna relación entre la causa de muerte y la nacionalidad?


## 🌀 Análisis:<a name="analisis"/>

En primer lugar, hemos decido crear un mapa para situar cada una de las cumbres de forma directa.

![dashboard](./images/map.png)

En el siguiente dashboard podemos observar un resumen del conjunto total de los datos. Contiene un slider con el que se puede seleccionar el rango de años del cual queremos obtener la información. Según ello, se puede saber cuáles fueron los meses con más fallecimientos, las cinco causas de muerte más habituales, en qué montaña ha fallecido más gente y de qué diez nacionalidades eran esas personas.

La imagen muestra esos resultados filtrados desde el 1980 al 2003.

![dashboard](./images/5003.png)


El segundo dashboard dashboard lo hemos enfocado al análisis de cada una de las cumbres por separado. Para ello hemos creado un selector interactivo mediante el cual se puede elegir la montaña deseada. De ella obtendremos la información de su altitiud, su localización en el mapa, cuántos fallecidos hay en total, en qué meses han ocurrido los desastres y cuáles han sido las siete causas más comunes.

En esta imagen podemos ver toda esta selección de la montaña K2, conocida por ser la más peligrosa.

![dashboard](./images/k2.png)



## 🧗‍♀️ Conclusiones:<a name='conclusion'/>

Como vemos en el mapa, las 14 se concentran en las cordilleras del Himalaya y el Karakórum. 

Con el primer dashboard hemos podido observar que los meses de primavera y otoño son los que más fallecimientos registran, esto se ve directamente relacionado con la programación de las expediciones que se concentran en esos meses. 

Las avalanchas denotan ser la causa principal de muerte seguido por caídas y el llamado mal de alturas.

Sobre las muertes registradas, vemos que el Everest es el que más tiene con diferencia. Esto es debido a que es la montaña más visitada llegando a registrar hasta 800 expediciones anuales. Pero comparando las muertes con las subidas obtenemos que las más peligrosas en si son Annapurna, K2 y Nanga Parbat.

Nepal aparece como país con más registros de nacionalidades fallecidas. Es un valor adecuado ya que se cuentan en este registro tanto los fallecimientos de escaladores como de sherpas, siendo estos últimos de mayoría procedente de la misma zona. Le continuan Japón, Corea del sur y España, países con mucha tradición de montaña y escalada.

Gracias al segundo dashbord se pueden analizar más en profundidad cada una de las cumbres. De ella podemos destacar cómo las que se encuentran hacia el noroeste coinciden con el mes más mortal julio y el resto, hacia el sureste en mayo. 

También podemos observar el riesgo más común en cada una siendo casi un 50% de ellas entre avalancha y caída como la más frecuente.

En perspectiva, el proyecto consigue el objetivo de enfocarse con una funcionalidad hacia la creación de una app en la que montañistas puedan observar gráficas de su objetivo y analizar su escalada en cuestión de época, precauciones y destino. Se facilitaría así un recurso mediante el cual tener mayor acceso al análisis de la aventura de altura.


## 🧊 Estructura:<a name="estructura"/>

```
Proyecto 
|__ DATA/                         # contiene datos limpios de jupyter notebook y los csv limpios
|
|__ IMAGES/                       # contiene imagénes referentes al proyecto    
|
|___DASHBOARDS/                   # dashboards de power bi 
|
|__ .gitignore                    # archivo gitignore     
|
|__ README.md                     # información del proyecto
```
