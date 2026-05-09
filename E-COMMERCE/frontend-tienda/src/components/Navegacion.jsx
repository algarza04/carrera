function Navegacion({ onInput }) {
    return (
        <div>
                <input
                    type="text"
                    placeholder="Escribe para buscar (mínimo 3 letras)..."
                    className="w-full pl-10 pr-4 py-2 border-2 border-green-500 rounded-full text-white-900 placeholder-gray-500 focus:outline-none focus:border-green-600 focus:ring-1 focus:ring-green-600 shadow-md"
                    autoComplete="off"
                    autoFocus
                    onInput={onInput}
                />
        </div>
    );
}

export default Navegacion;