// cambio-precio.js
//import logger from '../../winston-logging/logger.js'


const cambiar_precio = (evt) => {
    const botón = evt.target

   	// identificar a que producto pertenece 
    const id = botón.dataset.id

	// identificar el <input > que le corresponde
    const input = document.querySelector(`input[data-id="${id}"]`)

 	// tomar el valor de entrada del input
    const nuevoPrecio = input.value

    if (nuevoPrecio === "" || isNaN(nuevoPrecio) || Number(nuevoPrecio) < 0) {
        input.style.border = "2px solid red";
        alert("El precio introducido no es válido.");
        //logger.error("No se puede introducir un valor negativo o nulo a un producto")

        return
    }

    fetch(`/api/productos/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json;charset=utf-8"
        },
        body: JSON.stringify({
            precio_euros: Number(nuevoPrecio),
            precio_rebajado: 0
        })
    })
    .then(res => res.json())
    .then(res => {
        console.log(res)
        //logger.info("El precio del producto ha sido actualizado")
        // poner el precio actualizado

        input.style.border = "2px solid green"
    })
    .catch(err => {
        console.error(err)
        //logger.error("El nuevo precio introducido para el producto no es correcto")
        input.style.border = "2px solid red"
    })
}

// sacar los botones_cambiar_precio aqui
const botones_cambiar_precio = document.querySelectorAll(".btn_editar_precio"); 

for (const botón of botones_cambiar_precio) {
	botón.addEventListener('click', cambiar_precio)
}