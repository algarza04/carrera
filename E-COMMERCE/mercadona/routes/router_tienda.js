// ./routes/router_tienda.js
import express from "express";
import Producto from "../model/Producto.js";
const router = express.Router();

// Portada en /
router.get("/", async (req, res) => {
  try {
    //const productos = await Producto.find({})   // todos los productos
    const productos = await Producto.aggregate([{ $sample: { size: 9 } }]); // 9 productos
    res.render("../views/portada.html", { productos }); // ../views/portada.html,
  } catch (err) {
    // se le pasa { productos:productos }
    console.error(err);
    res.status(500).send({ err: err.message });
  }
});

// Ofertas en /ofertas
// Los productos cuyo precio_rebajado no sea 0 se muestran en ofertas
router.get("/ofertas", async (req, res) => {
  try {
    const productos = await Producto.find({ precio_rebajado: { $ne: 0 } });

    // devolvemos los productos en oferta.
    res.render("../views/portada.html", { productos });
  } catch (err) {
    console.error(err);
    res.status(500).send({ err: err.message });
  }
});

// nueva ruta de búsqueda
// función para que se busque el texto literal y no patrones regex(expresion regular)
function escapeRegex(text) {
  return text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

// Busqueda en /buscar?q=
router.get("/busqueda-anticipada", (req, res) => {
    // Renderizamos una nueva vista que crearemos ahora
    res.render("../views/busqueda_anticipada.html");
});

// Añadir al carrito en /al_carrito/:id
router.get("/al_carrito/:id", async (req, res) => {
  const productoId = req.params.id;

  try {
    const productoAñadir = await Producto.findById(productoId); // buscar el producto por ID

    if (productoAñadir) {
      const existeItem = req.session.carrito.find(
        (item) => item._id === productoAñadir._id.toString()
      ) // Verificar si el producto ya está en el carrito
      
      let precioUnitario

      if (productoAñadir.precio_rebajado > 0) {
        precioUnitario = parseFloat(productoAñadir.precio_rebajado) || 0 //pasar el precio a float, el 0 sirve para evitar errores si no hay precio
      } 
      else{
        precioUnitario = parseFloat(productoAñadir.precio_euros) || 0 //pasar el precio a float, el 0 sirve para evitar errores si no hay precio
      }

      // actualizar el carrito
      if (existeItem) {
        existeItem.cantidad += 1
      } else {
        req.session.carrito.push({
          _id: productoAñadir._id.toString(),
          nombre: productoAñadir.texto_1 || "Producto sin nombre",
          precio: precioUnitario,
          cantidad: 1,
        })
      }

      res.redirect("/"); // redirigimos a la pantalla principal
    } else {
      res.status(404).send("Producto no encontrado con el ID: " + productoId);
    }
  } catch (err) {
    console.error(err)
    res.status(500).send({ err: err.message })
  }
})

export default router;