import useSWR from 'swr';
import "tailwindcss"
// obtener datos
const fetcher = (...args) => fetch(...args).then(res => res.json());

export default function Resultados({ de }) {

    if (de.length < 3) return <div> al menos 3 caractéres </div>

    const ponProductos = (data) => {
        if (data.length === 0) {
            return (
                <div>
                    <h2 className="error">
                        No se encontraron productos para "{de}"
                    </h2>
                </div>
            );
        }

        return (
            <div>
                <h2 className='text-3xl text-green-600 font-bold mb-8'>
                    Encontrados {data.length} productos
                </h2>
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {data.map((producto) => (
                        <TarjetaProducto key={producto._id} p={producto} />
                    ))}
                </div>
            </div>
        );
    };

	// hook de swr, re-rendiriza en algún cambio de las variables
    const { data, error, isLoading } = useSWR(
        `http://localhost:8000/api/productos/busqueda-anticipada/${de}`,
        fetcher
    );

	return (
		<div>
			{
				isLoading ? (
					<h1><Spinner /></h1>
				) : data ? (
					ponProductos(data)
				) : error ? (<div>{error}</div>) : (<div>...</div>)
			}
		</div>
	)
}

function TarjetaProducto({ p }) {
    const tieneOferta = p.precio_rebajado > 0;

    return (
        <div className='max-w-sm rounded overflow-hidden shadow-lg hover:shadow-xl transition-shadow duration-300 border border-gray-200 flex flex-col h-full'>
            <div>
                <img className='w-full flex items-center justify-center bg-gray-50 p-4'
                    src={p.url_img}
                    alt={p.texto_1}
                />
            </div>

            <div className='px-6 py-4 flex-grow'>
                <div className='font-bold text-xl mb-2 nombre-producto'>{p.texto_1}</div>
                <p className='text-sm descripcion-producto mb-4'>{p.texto_2}</p>
            </div>

            <div className='px-6 pb-6 mt-auto'>
                <div className='mb-4'>
                    <span className={`${tieneOferta ? 'text-2xl font-bold text-red-600' : 'text-2xl font-bold text-white-600'}`}>
                        {tieneOferta ? p.precio_rebajado : p.precio_euros} €
                    </span>
                </div>

                <a 
                	href={`http://localhost:8000/al_carrito/${p._id}`}
                	className="w-full bg-green-600 hover:bg-green-700 !text-white font-bold py-2 px-4 rounded-full transition-colors duration-200 flex items-center justify-center gap-2">
                    Añadir al carro
                </a>
            </div>
        </div>
    );
}

function Spinner() {
    return (
        <div className="flex justify-center items-center py-20">
            <div className="rounded-full h-8 w-8 border-t-8 border-b-8 border-green-600"></div>
        </div>
    );
}
