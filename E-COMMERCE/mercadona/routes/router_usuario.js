// ./routes/router_usuarios.js
import express from "express"
import bcrypt from 'bcrypt'
import jwt from 'jsonwebtoken'
import Usuario from "../model/Usuarios.js"
import logger from '../winston-logging/logger.js'

const router = express.Router()

// Para mostrar formulario de login              --> GET
router.get('/login', (req, res)=>{
	res.render("login.html")
})
				
// Para recoger datos del formulario de login    --> POST
router.post('/login', async (req, res)=> {
	try {
        // obtener datos del formulario, body es el cuerpo de la petición, en el que vienen los datos del formulario(asi no viajan en la url)
		const { username, password } = req.body	
		
        const usuario = await Usuario.findOne({ username })
        
        if (!usuario) { // si no existe el usuario
		    //return res.status(401).send('Usuario o contraseña incorrectos.')
            logger.warn('Usuario o contraseña incorrectos.')
            return res.render('login.html', { error: 'Usuario o contraseña incorrectos' })
        }

        //  Comparar la contraseña (forma segura con Bcrypt)
        const match = await bcrypt.compare(password, usuario.password)

        if (!match) {
            //return res.status(401).send('Usuario o contraseña incorrectos.')
            logger.warn('Usuario o contraseña incorrectos.')
			return res.render('login.html', { error: 'Usuario o contraseña incorrectos' })
        }

		// Crear token JWT
		//const token = jwt.sign({usuario: usuario.username}, process.env.SECRET_KEY)
        //const user_db = await Usuario.findOne({username:req.body.username})
        const token = jwt.sign({usuario:usuario.username, admin:usuario.admin}, process.env.SECRET_KEY)

		// Guardar el token en una cookie
		res.cookie("access_token", token, {            // cookie en el response
			httpOnly: true,
			secure: process.env.IN === 'production'      // en producción, solo con https
		}).redirect("/")
	} catch (err) {
		//console.error(err)
        logger.error(err.message)
		return res.status(500).send({ err: err.message })
	}
})
				
// Registro
router.get('/registro', (req, res) => {        // --> GET
	res.render("registro.html")
})
	
router.post('/registro', async (req, res) => {  // --> POST
	try {
        // obtenemos los datos del formulario
        const { username, password, confirmPassword } = req.body

        // comprobamos que las contraseñas coinciden
        if (password !== confirmPassword) {
            //console.log("Las contraseñas no coinciden")
            //return res.redirect('/usuarios/registro')
			return res.render('registro.html', { error: 'Las contraseñas no coinciden' })
        }

        // validamos que no haya un usuario con ese nombre
        const existingUser = await Usuario.findOne({ username : username })
        if (existingUser) {
            //console.log("El nombre de usuario ya está en uso")
            //return res.redirect('/usuarios/registro')
            logger.warn('El nombre de usuario ya está en uso')
			return res.render('registro.html', { error: 'El nombre de usuario ya está en uso' })
        }

        // hash de la contraseña
        // bcrypt añade una cadena aleatoria para evitar que dos contraseñas iguales tengan el mismo hash
        // 10 indica el coste computacional del hash, repite el proceso 2^10 veces
        const hashedPassword = await bcrypt.hash(password, 10)

        // creamos el nuevo usuario
        const newUser = new Usuario({
            username: username,
            password: hashedPassword
        })

        // añadimos el usuario a la bbdd
        await newUser.save()

        res.redirect("/")

    } catch (err) {
        //console.error(err)
        logger.error(err.message)
        return res.status(500).send({ err: err.message })
    }
})

// Salida
router.get('/logout', (req, res) => {
	res.clearCookie('access_token') // borrar la cookie del token
    req.session.destroy()          // destruir la sesión
	res.redirect('/')
})

export default router