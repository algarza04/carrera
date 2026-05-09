 // ./model/Usuarios.js 
import mongoose from 'mongoose';

const usuarioSchema = new mongoose.Schema({
    username: {
        type: String,
        required: true,
        trim: true,   // Removes whitespace
    },
    password: {
        type: String,
        required: true,
        trim: true,
    },
    admin: {
        type: Boolean,
        default: false,
        required: false
}
    
})
const Usuario = mongoose.model('Usuario', usuarioSchema);
export default Usuario