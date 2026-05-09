import express from "express";
import nunjucks from "nunjucks";
import session from "express-session";

import cookieParser from "cookie-parser"
import jwt from "jsonwebtoken"

import TiendaRouter from "./routes/router_tienda.js";
import UsuariosRouter from "./routes/router_usuario.js"
import apiProductos from "./routes/api_productos.js"

import logger from './winston-logging/logger.js'

import swaggerUi from 'swagger-ui-express';
import swaggerJsDoc from 'swagger-jsdoc';

import connectDB from "./model/db.js";

import cors from "cors"

await connectDB();

const app = express();
const PORT = process.env.PORT || 8000;

app.use(cors())

app.use(session({
	secret: process.env.SECRET_KEY,      // clave secreta para firmar la cookie de sesión
	resave: false,            // no guardar sesión si no ha habido cambios
	saveUninitialized: false  // no guardar sesiones vacías
}))

app.use((req, res, next) => {
    if (!req.session.carrito) { // crear carrito si no existe
        req.session.carrito = []; 
    }

    const carrito = req.session.carrito;

    let totalArticulos = 0;
    let precioTotal = 0.0;

    // Utilizamos reduce para un cálculo limpio y correcto
    const resultado = carrito.reduce((acc, item) => {
        const cantidad = item.cantidad || 1; // Usar la cantidad guardada
        const precio = item.precio || 0;     // Precio unitario
        
        acc.totalArticulos += cantidad;
        acc.precioTotal += precio * cantidad;
        
        return acc;
    }, { totalArticulos: 0, precioTotal: 0.0 });
    
    // asignar los resultados a res.locals para que estén disponibles en las vistas
    res.locals.totalArticulos = resultado.totalArticulos;
    res.locals.precioTotal = resultado.precioTotal;
    
    // pasar el carrito completo también
    res.locals.carrito = carrito;
    
    next();
});

app.use(cookieParser())

app.use(express.urlencoded({ extended: true }))

// middleware de
const autentificación = (req, res, next) => {
	const token = req.cookies.access_token;
	if (token) {
		const data = jwt.verify(token, process.env.SECRET_KEY);
		req.username = data.usuario                               // username en el request
		app.locals.usuario = data.usuario    
        app.locals.admin = data.admin
	} else {
		app.locals.usuario = undefined
        app.locals.admin = undefined
	}
	next()
}
app.use(autentificación)

app.use(express.json())
app.use("/api/productos", apiProductos)

const swaggerOptions = {
    swaggerDefinition: {
        myapi: '3.0.0',
        info: {
            title: 'API Tienda Mercadona',
            version: '1.0.0',
            description: 'API documentation',
        },
        servers: [
            { url: `http://localhost:${PORT}` } 
        ],
    },
    apis: ['./routes/*.js'],  // files containing annotations as above
};

const swaggerDocs = swaggerJsDoc(swaggerOptions);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocs));

app.listen(PORT, () => {
    console.log(`Swagger se está ejecutando en http://localhost:${PORT}`);
});

app.use("/", TiendaRouter);

const IN = process.env.IN || 'development';

nunjucks.configure('views', {
    autoescape: true,
    noCache: IN === 'development',
    watch: IN === 'development',
    express: app
});
app.set('view engine', 'html');

app.use('/static', express.static('public'));
app.use('/icons', express.static('icons'));

// test para el servidor
app.get("/hola", (req, res) => {
    res.send('Hola desde el servidor');
});

// test para las plantillas
app.get("/test", (req, res) => {
    res.render('test.html');
});

app.get("/carrito", (req, res) => {
    res.render('carrito.html');
});

app.use("/usuarios", UsuariosRouter); // para urls que comienzen por /usuarios

app.listen(PORT, () => {
    //console.log(`Servidor ejecutándose en http://localhost:${PORT}`);
    logger.info(`Servidor ejecutándose en http://localhost:${PORT}`)
});