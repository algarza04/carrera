import fs from 'node:fs'

// https://github.com/taoqf/node-html-parser
// se instala
// npm i node-html-parser
import { parse } from 'node-html-parser';


// Para acumular la informácion de los productos
const Info = []

// cambiar el programa para usar una lista de varios archivos html
// con distintas categorías
// elemento:
//<div class="grid-layout__main-container" style="height: calc(-76px + 100vh)">
// ...
// </div>
const files = ['html/aceites.html', 'html/agua.html', 'html/aceitunas.html']

for (let index = 0; index < files.length; index++) {
	const html = Lee_archivo(files[index])

	const root = parse(html)

	const categoría = root.querySelector('h1').text

	const subcategorias = root.querySelectorAll('section.section')
	
	for (const sub of subcategorias){

		const subcategoría = sub.querySelector('h2').text
		const lista_productos = sub.querySelectorAll('div.product-cell')

		for (const producto of lista_productos) {
			const img = producto.querySelector('img')
			const url_img = img.attrs.src
			const texto_1 = img.attrs.alt
			const t2 = producto.querySelector('div.product-format')
			const texto_2 = Arregla_texto(t2.text)
			const texto_precio = Arregla_texto(producto.querySelector('div.product-price').innerText)
			const r1 = texto_precio.match(/(\d+),?(\d+)?(.+)/)
			//console.log(r1)
			const precio_euros = (r1.length > 2) ? Number(r1[1] + '.' + r1[2]) : undefined

			const precio_anterior_element = producto.querySelector('.product-price__previous-unit-price')
			let precio_rebajado = 0

			if (precio_anterior_element) {
				const texto_precio_rebajado = Arregla_texto(producto.querySelector('.product-price__unit-price--discount').innerText)
				const r2 = texto_precio_rebajado.match(/(\d+),?(\d+)?(.+)/)
				//console.log(r1)
				precio_rebajado = (r2.length > 2) ? Number(r2[1] + '.' + r2[2]) : undefined
			}
			

			const info_prod = {
				categoría,
				subcategoría,
				url_img,
				texto_1,
				texto_2,
				texto_precio,
				precio_euros,
				precio_rebajado
			}
			Info.push(info_prod)	
		}
	}
}
const string_para_guardar_en_fomato_json = JSON.stringify(Info, null, 2)

try {
	fs.writeFileSync('datos_mercadona.json', string_para_guardar_en_fomato_json)
	console.log('Guardado archivo')
} catch (error) {
	console.error('Error guardando archivo: ', error)
}


function Arregla_texto(texto) {
	let arreglado = texto.replace('\n', '')
	arreglado = arreglado.replace(/\s+/g, ' ')
	return arreglado.trim()
}


function Lee_archivo(archivo) {
    try {
        return fs.readFileSync(archivo, 'utf8')
    } catch (error) {
        console.error('Error leyendo archivo: ', error);
    }
}
