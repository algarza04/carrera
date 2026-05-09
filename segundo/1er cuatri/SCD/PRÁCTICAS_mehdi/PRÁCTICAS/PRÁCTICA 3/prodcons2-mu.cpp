// -----------------------------------------------------------------------------
//
// Sistemas concurrentes y Distribuidos.
// Práctica 3. Implementación de algoritmos distribuidos con MPI
//
// Archivo: prodcons_mu.cpp
// Implementación del problema del productor-consumidor con
// un proceso intermedio que recibe mensajes síncronos de forma alterna 
// con selección no determinista.
// (versión con múltiples productores y consumidores)
//
// Hecho por: Mehdi Iabouten
// DNI: K568645
// -----------------------------------------------------------------------------


#include <iostream>
#include <thread> // this_thread::sleep_for
#include <random> // dispositivos, generadores y distribuciones aleatorias
#include <chrono> // duraciones (duration), unidades de tiempo
#include <mpi.h>  // includes de MPI

using namespace std;
using namespace std::this_thread ;
using namespace std::chrono ;

// ---------------------------------------------------------------------
// constantes que determinan la asignación de identificadores a roles:
const int
   tam_vector            = 10 , //tamaño vector
   np                    = 4 , //número productores
   nc                    = 5 , //número consumidores
   min_id_productor          = 0 , // identificador del proceso productor
   max_id_productor          = np - 1 ,
   id_buffer             = np , // identificador del proceso buffer
   min_id_consumidor         = np + 1 , // identificador del proceso consumidor
   max_id_consumidor         = np + nc ,
   num_procesos_esperado = np + nc +1 , // número total de procesos esperado
   num_items             = np * nc , // numero de items producidos o consumidos
   etiq_prod             = 50 ,
   etiq_cons             = 100 ;

//**********************************************************************
// plantilla de función para generar un entero aleatorio uniformemente
// distribuido entre dos valores enteros, ambos incluidos
// (ambos tienen que ser dos constantes, conocidas en tiempo de compilación)
//----------------------------------------------------------------------

template< int min, int max > int aleatorio()
{
  static default_random_engine generador( (random_device())() );
  static uniform_int_distribution<int> distribucion_uniforme( min, max ) ;
  return distribucion_uniforme( generador );
}
// ---------------------------------------------------------------------
// produce los numeros en secuencia (1,2,3,....)

int producir( const int prod )
{
   static const int k = num_items/np;
   static int contador = prod * k;
   sleep_for( milliseconds( aleatorio<10,200>()) );
   contador++ ;
   cout << "Productor ha producido valor " << contador << endl << flush;
   return contador ;
}
// ---------------------------------------------------------------------

void funcion_productor( const int productor )
{
   for ( unsigned int i= 0 ; i < num_items/np ; i++ )
   {
      // producir valor
      int valor_prod = producir( productor );
      // enviar valor
      cout << "Productor va a enviar valor " << valor_prod << endl << flush;
      MPI_Ssend( &valor_prod, 1, MPI_INT, id_buffer, etiq_prod, MPI_COMM_WORLD );
   }
}
// ---------------------------------------------------------------------

void consumir( int valor_cons, const int cons )
{
   // espera bloqueada
   sleep_for( milliseconds( aleatorio<10,200>()) );
   cout << "Consumidor " << cons << " ha consumido valor " << valor_cons << endl << flush ;
}
// ---------------------------------------------------------------------

void funcion_consumidor( const int consumidor )
{
   int         peticion,
               valor_rec = 1 ;
   MPI_Status  estado ;

   for( unsigned int i=0 ; i < num_items/nc; i++ )
   {
      MPI_Ssend( &peticion,  1, MPI_INT, id_buffer, etiq_cons, MPI_COMM_WORLD);
      MPI_Recv ( &valor_rec, 1, MPI_INT, id_buffer, etiq_cons, MPI_COMM_WORLD,&estado );
      cout << "Consumidor " << consumidor << " ha recibido valor " << valor_rec << endl << flush ;
      consumir( valor_rec , consumidor );
   }
}
// ---------------------------------------------------------------------

void funcion_buffer()
{
    int buffer[tam_vector],         // buffer con celdas ocupadas y vacías
        valor,                      // valor recibido o enviado
        primera_libre = 0,          // índice de primera celda libre
        primera_ocupada = 0,        // índice de primera celda ocupada
        num_celdas_ocupadas = 0,    // número de celdas ocupadas
        etiq_emisor_aceptable ;       // identificador de emisor aceptable
    MPI_Status estado ;             // metadatos del mensaje recibido

   for ( unsigned int i = 0 ; i < num_items*2 ; i++ )
   {
      // 1. determinar si puede enviar solo prod., solo cons, o de ambos
      if ( num_celdas_ocupadas == 0 )                 // si buffer vacío
         etiq_emisor_aceptable = etiq_prod ;         // solo prod.
      
      else if ( num_celdas_ocupadas == tam_vector )   // si buffer lleno
         etiq_emisor_aceptable = etiq_cons ;        // solo cons.
      
      else                                            // si no vacío ni lleno
         etiq_emisor_aceptable = MPI_ANY_TAG ;

      // 2. recibir un mensaje del emisor o emisores aceptables:
      MPI_Recv( &valor, 1, MPI_INT, MPI_ANY_SOURCE, etiq_emisor_aceptable, MPI_COMM_WORLD, &estado );
      
      // 3. procesar el mensaje recibido
      switch( estado.MPI_TAG ) // leer emisor del mensaje en metadatos
      {
         case etiq_prod: // si ha sido el productor: insertar en buffer
            buffer[primera_libre] = valor ;
            primera_libre = (primera_libre+1) % tam_vector ;
            num_celdas_ocupadas++ ;
            cout << "Buffer ha recibido valor " << valor << endl ;
            break;

         case etiq_cons: // si ha sido el consumidor: extraer y enviarle
            valor = buffer[primera_ocupada] ;
            primera_ocupada = (primera_ocupada+1) % tam_vector ;
            num_celdas_ocupadas-- ;
            cout << "Buffer va a enviar valor " << valor << endl ;
            MPI_Ssend( &valor, 1, MPI_INT, estado.MPI_SOURCE, etiq_cons, MPI_COMM_WORLD);
            break;
      }
   }
}

// ---------------------------------------------------------------------

int main( int argc, char *argv[] )
{
  int id_propio, num_procesos_actual; // ident. propio, núm. de procesos

  MPI_Init( &argc, &argv );
  MPI_Comm_rank( MPI_COMM_WORLD, &id_propio );
  MPI_Comm_size( MPI_COMM_WORLD, &num_procesos_actual );

  if ( num_procesos_esperado == num_procesos_actual )
  {
    if ( (id_propio >= min_id_productor) && (id_propio <= max_id_productor) )  // si mi ident. es el del productor
      funcion_productor(id_propio);            //    ejecutar función del productor
    else if ( id_propio == id_buffer )// si mi ident. es el del buffer
      funcion_buffer();               //    ejecutar función buffer
    else                              // en otro caso, mi ident es consumidor
      funcion_consumidor(id_propio-(np+1));           //    ejecutar función consumidor
  }
  else if ( id_propio == 0 )  // si hay error, el proceso 0 informa
    cerr << "error: número de procesos distinto del esperado." << endl ;

  MPI_Finalize( );
  return 0;
}
// ---------------------------------------------------------------------
