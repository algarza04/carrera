// seed.js
import mongoose from 'mongoose'
import fs from 'fs'

import connectDB from './db.js'
import Producto from './Producto.js'
	
await connectDB()
	
const datos_productos = Lee_archivo('datos_mercadona.json')
const lista_productos = JSON.parse(datos_productos)
	
await Guardar_en_modelo(Producto, lista_productos)
	
mongoose.connection.close()
		
// https://mongoosejs.com/docs/api/model.html#Model.insertMany()
// devuelve una 'Promise', por tanto asíncrono
	
async function Guardar_en_modelo(modelo, lista) {
	try {
		await modelo.deleteMany()                             // borrar todo lo que hubiera
		const insertados = await modelo.insertMany(lista)           // await siempre en funciones async
		console.log(`Insertados ${insertados.length} documentos`)
	} catch (error) {
		console.error(`Error guardando lista ${error.message}`)
	}
}

// Lee_archivo: lee un archivo y devuelve su contenido como string
function Lee_archivo(ruta) {
	try {
		return fs.readFileSync(ruta, 'utf8');
	} catch (error) {
		console.error(`Error leyendo archivo ${ruta}: ${error.message}`);
	}
}