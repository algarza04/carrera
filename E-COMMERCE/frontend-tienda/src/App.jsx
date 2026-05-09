import { useState } from 'react'
import Navegacion from "./components/Navegacion"
import Resultados from "./components/Resultados"
import './App.css'

function App() {

  const [busqueda, setBusqueda] = useState('')

  const handleInput = (evt) => {
    const value = evt.target.value
    // comprobar que funciona
    console.log(value)
    setBusqueda(value)
  }

  return (
    <>
      <h1>Búsqueda Anticipada</h1>        
      <Navegacion onInput={handleInput} />
      <Resultados de={busqueda} />
    </>
  )
}
export default App