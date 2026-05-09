// ./routes/router_productos.js
import express from "express"
import Producto from "../model/Producto.js"
import logger from '../winston-logging/logger.js'

const router = express.Router()

// Obtener todos los productos GET /api/productos
/**
 * @swagger
 * /api/productos:
 *   get:
 *     summary: Devuelve la lista de productos
 *     responses:
 *       200:
 *         description: Lista de productos devuelta correctamente
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 type: object
 *                 properties:
 *                   _id:
 *                     type: string
 *       500:
 *         description: Error interno servidor
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 type: object
 *   
 */
router.get("/", async (req, res) => {
    try {
        const productos = await Producto.find({})
        res.json(productos)
    } catch (err) {
        //console.error(err)
        logger.error(err.message)
        res.status(500).json({ err: err.message })
    }
})

// Obtener un producto por ID GET /api/productos/id
/**
 * @swagger
 * /api/productos/{id}:
 *   get:
 *     summary: Devuelve un producto
 *     tags: [Productos]
 *     parameters: 
 *     - in: path
 *       name: id
 *     responses:
 *       200:
 *         description: Producto devuelto correctamente
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 type: object
 *                 properties:
 *                   _id:
 *                     type: string
 *       404:
 *         description: Producto no encontrado
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 type: object
 *       500:
 *         description: Error interno servidor
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 type: object
 *   
 */
router.get("/:id", async (req, res) => {
    try {
        const producto = await Producto.findById(req.params.id)
        if (!producto) {
            logger.warn('Producto no encontrado')
            return res.status(404).json({ err: "Producto no encontrado" })
        }
        res.json(producto)
    } catch (err) {
        //console.error(err)
        logger.error(err.message)
        res.status(500).json({ err: err.message })
    }
})

// Crear un nuevo producto POST /api/productos
/**
 * @swagger
 * /api/productos:
 *   post:
 *     summary: Crea un nuevo producto
 *     tags: [Productos]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - categoría
 *               - subcategoría
 *               - url_img
 *               - texto_1
 *               - texto_2
 *               - texto_precio
 *               - precio_euros
 *             properties:
 *               categoría:
 *                 type: string
 *                 example: snacks
 *               subcategoría:
 *                 type: string
 *                 example: galletas
 *               url_img:
 *                 type: string
 *                 example: snacks
 *               texto_1:
 *                 type: string
 *                 example: galletas choco blanco
 *               texto_2:
 *                 type: string
 *                 example: galletas recubiertas de chocolate blanco
 *               texto_precio:
 *                 type: string
 *                 example: 2.5€/pack
 *               precio_euros:
 *                 type: number
 *                 example: 2.5
 *               precio_rebajado:
 *                 type: number
 *                 nullable: true
 *                 example: 0
 *     responses:
 *       201:
 *         description: Producto creado correctamente
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 _id:
 *                   type: string
 *                 categoría:
 *                   type: string
 *                 subcategoría:
 *                   type: string
 *                 url_img:
 *                   type: string
 *                 texto_1:
 *                   type: string
 *                 texto_2:
 *                   type: string
 *                 texto_precio:
 *                   type: string
 *                 precio_euros:
 *                   type: number
 *                 precio_rebajado:
 *                   type: number
 *                   nullable: true
 *       404:
 *         description: Producto no encontrado
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 type: object
 *       500:
 *         description: Error interno servidor
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 type: object
 */
router.post("/", async (req, res) => {
    try {
        //comprobar que no existe un producto con dicho nombre
        const { texto_1 } = req.body
        const productoExistente = await Producto.findOne({ 
            texto_1: texto_1
        })
        // si existe no creamos el producot
        if (productoExistente) {
            logger.warn(`Ya hay un producto con ese nombre: ${texto_1}`);
            return res.status(400).json({ 
                error: "Ya hay un producto con ese nombre" 
            });
        }

        const nuevoProducto = new Producto(req.body)
        const productoGuardado = await nuevoProducto.save()

        res.status(201).json(productoGuardado)
        logger.info("Nuevo producto guardado")
    } catch (err) {
        //console.error(err)
        logger.error(err.message)
        res.status(500).json({ err: err.message })
    }
})

// Eliminar un producto DELETE /api/productos/id
/**
 * @swagger
 * /api/productos/{id}:
 *   delete:
 *     summary: Elimina un producto
 *     tags: [Productos]
 *     parameters: 
 *     - in: path
 *       name: id
 *     responses:
 *       200:
 *         description: Producto eliminado correctamente
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 type: object
 *                 properties:
 *                   _id:
 *                     type: string
 *       404:
 *         description: Producto no encontrado
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 type: object
 *       500:
 *         description: Error interno servidor
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 type: object
 *   
 */
router.delete("/:id", async (req, res) => {
    try {
        const productoEliminado = await Producto.findByIdAndDelete(req.params.id)
        if (!productoEliminado) {
            logger.warn("Producto no encontrado")
            return res.status(404).json({ err: "Producto no encontrado" })
        }

        logger.info('Producto eliminado')
        res.json({ msg: "Producto eliminado", producto: productoEliminado })
    } catch (err) {
        //console.error(err)
        logger.error(err.message)
        res.status(500).json({ err: err.message })
    }
})

// Actualizar un producto PUT /api/productos/id
router.put("/:id", async (req, res) => {
    try {
        const productoActualizado = await Producto.findByIdAndUpdate(
            req.params.id,
            req.body,
            { new: true }
        )
        if (!productoActualizado) {
            logger.warn('Producto no encontrado')
            return res.status(404).json({ err: "Producto no encontrado" })
        }
        logger.info('Producto actualizado')
        res.json(productoActualizado)
    } catch (err) {
        //console.error(err)
        logger.error(err.message)
        res.status(500).json({ err: err.message })
    }
})

function escapeRegex(text) {
    return text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

// Búsqueda anticipada
// GET /api/productos/busqueda-anticipada/:cadena
router.get("/busqueda-anticipada/:cadena", async (req, res) => {
    try {
        const cadena = req.params.cadena;
        // Si la cadena es menor de 3 caracteres, devolvemos array vacío (opcional, validación extra)
        if (!cadena || cadena.length < 3) {
            return res.json([]);
        }

        const regex = new RegExp(escapeRegex(cadena), "i"); 
        
        const productos = await Producto.find({
            $or: [
                { texto_1: regex },
                { texto_2: regex },
                { categoría: regex },
                { subcategoría: regex },
            ],
        });
        
        // Devolvemos solo la lista de productos en JSON
        res.json(productos);
        
    } catch (err) {
        logger.error(err.message);
        res.status(500).json({ err: err.message });
    }
});
export default router           