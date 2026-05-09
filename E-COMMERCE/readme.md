# PRACTICA 6 DAI
## Álvaro García Zafra

## Funcionalidades implementadas
He seguido los pasos de instalación incluidos en la documentación (cors, vite...)
Una vez tenía todo instalado he pasado a realizar las funcionalidades, para ello he modificado el archivo `app.jsx` para la nueva funcionalidad(busquedas y mostrar resultados) y cree los dos archivos que utiliza para esto `/components/Navegacion.jsx` y `/components/Resultados.jsx`.
En el archivo de navegación está implementada la barra de búsqueda y en resultados la lógica de funcionamiento y como se deben mostrar los productos encontrados.
Además he implementado el spinner para que cuando este cargando aparezca eso y sepas que este buscando.

## Ejecución

Iniciamos nuestro contenedor, que poseerá la BD mongo
    `docker compose up -d`

Obtenciónn del archivo json que contiene los datos que vamos a pasarle a la BD
    `node parser.js`

Pasamos los datos de nuestro json a la BD
    `npm run seed`  

Si accedemos a nuestra BD podemos comprobar que es correcto: `http://localhost:8081/db/DAI/productos`

Iniciamos el servidor desde la carpeta mercadona
    `npm run dev`

Accedemos a nuestra página
    `http://localhost:8000/`

Iniciamos el frontend react desde la carpeta frontend-tienda
    `npm run dev`

Accedemos a nuestra página
    `http://localhost:5173/`
