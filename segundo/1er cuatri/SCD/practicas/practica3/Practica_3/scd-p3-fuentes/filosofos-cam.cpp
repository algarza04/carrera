//Álvaro García Zafra
/*
mpicxx -std=c++11 -o filosofos-cam filosofos-cam.cpp 
mpirun -oversubscribe -np 11 filosofos-cam
*/

#include <mpi.h>
#include <thread> // this_thread::sleep_for
#include <random> // dispositivos, generadores y distribuciones aleatorias
#include <chrono> // duraciones (duration), unidades de tiempo
#include <iostream>

using namespace std;
using namespace std::this_thread ;
using namespace std::chrono ;

const int
   num_filosofos = 5 ,              // número de filósofos 
   num_filo_ten  = 2*num_filosofos, // número de filósofos y tenedores 
   num_procesos  = num_filo_ten+1 ,   // número de procesos total (por ahora solo hay filo y ten)
   id_camarero = num_filo_ten,
   etiq_solicitar = 0,
	etiq_soltar = 1,
	etiq_sentar = 2, 
	etiq_levantar = 3;

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

void funcion_filosofos( int id )
{
  int id_ten_izq = (id+1)              % num_filo_ten, //id. tenedor izq.
      id_ten_der = (id+num_filo_ten-1) % num_filo_ten, //id. tenedor der.
 		peticion;
  
  while ( true )
  {
	 cout << "Filósofo " << id/2 << " solicita sentarse." << endl;	  
	 MPI_Ssend(&peticion, 1, MPI_INT, id_camarero, etiq_sentar, MPI_COMM_WORLD);
	 sleep_for( milliseconds( aleatorio<100,300>() ) );
	 
    cout <<"Filósofo " <<id/2 << " solicita ten. izq." <<id_ten_izq/2 <<endl;
    MPI_Ssend(&peticion, 1, MPI_INT, id_ten_izq, etiq_solicitar, MPI_COMM_WORLD);
	 sleep_for( milliseconds( aleatorio<100,300>() ) );
	
    cout <<"Filósofo " <<id/2 <<" solicita ten. der." <<id_ten_der/2 <<endl;
    MPI_Ssend(&peticion, 1, MPI_INT, id_ten_der, etiq_solicitar, MPI_COMM_WORLD);
	 sleep_for( milliseconds( aleatorio<100,300>() ) );
	
    cout <<"Filósofo " <<id/2 <<" comienza a comer" <<endl ;
    sleep_for( milliseconds( aleatorio<100,300>() ) );

    cout <<"Filósofo " <<id/2 <<" suelta ten. izq. " <<id_ten_izq/2 <<endl;
    MPI_Ssend(&peticion, 1, MPI_INT, id_ten_izq, etiq_soltar, MPI_COMM_WORLD);	
	 sleep_for( milliseconds( aleatorio<100,300>() ) );
	 
    cout<< "Filósofo " <<id/2 <<" suelta ten. der. " <<id_ten_der/2 <<endl;
    MPI_Ssend(&peticion, 1, MPI_INT, id_ten_der, etiq_soltar, MPI_COMM_WORLD);	
    sleep_for( milliseconds( aleatorio<100,300>() ) );
    
    cout << "Filósofo " << id/2 << " comienza a levantarse" << endl;
    MPI_Ssend(&peticion, 1, MPI_INT, id_camarero, etiq_levantar, MPI_COMM_WORLD);
    sleep_for( milliseconds( aleatorio<100,300>() ) );
    
    cout << "Filosofo " << id/2 << " comienza a pensar" << endl;
    sleep_for( milliseconds( aleatorio<200,400>() ) );
 }
}
// ---------------------------------------------------------------------

void funcion_tenedores( int id )
{
  int valor, id_filosofo ;  // valor recibido, identificador del filósofo
  MPI_Status estado ;       // metadatos de las dos recepciones

  while ( true )
  {
     MPI_Recv(&valor, 1, MPI_INT, MPI_ANY_SOURCE, etiq_solicitar, MPI_COMM_WORLD, &estado);

     id_filosofo = estado.MPI_SOURCE;
     
     cout <<"Ten. " <<id/2 <<" ha sido cogido por filo. " <<id_filosofo/2 <<endl;

     MPI_Recv(&valor, 1, MPI_INT, id_filosofo, etiq_soltar, MPI_COMM_WORLD, &estado);
     cout <<"Ten. "<< id/2<< " ha sido liberado por filo. " <<id_filosofo/2 <<endl ;
  }
}
// ---------------------------------------------------------------------
void funcion_camarero(){
	int valor, sentados = 0, etiq_aceptable;
	MPI_Status estado;
	
	while (true){
		if ( sentados == 0 )	
			etiq_aceptable = etiq_sentar;		//solo sentar
		else if ( sentados == num_filosofos-1)
			etiq_aceptable = etiq_levantar;	//solo levantar
		else{
			etiq_aceptable = MPI_ANY_TAG;
			
			if (etiq_aceptable % 2 == 0)	//los pares equivalen a la etiqueta sentar 
				etiq_aceptable = etiq_sentar;
			else if (etiq_aceptable % 2 == 1)	//los impares equivalen a la etiqueta levantar
				etiq_aceptable = etiq_levantar;
		}
		
		MPI_Recv(&valor, 1, MPI_INT, MPI_ANY_SOURCE, etiq_aceptable, MPI_COMM_WORLD, &estado);
		
		if ( estado.MPI_TAG == etiq_levantar ){
			sentados--;
			cout << "Filósofo " << estado.MPI_SOURCE/2 << " termina de levantarse" << endl;
		}
		else if ( estado.MPI_TAG == etiq_sentar ){
			sentados++;
			cout << "Filósofo " << estado.MPI_SOURCE/2 << " se sienta" << endl;
		}
		
	}
}
// ---------------------------------------------------------------------
int main( int argc, char** argv )
{
   int id_propio, num_procesos_actual ;

   MPI_Init( &argc, &argv );
   MPI_Comm_rank( MPI_COMM_WORLD, &id_propio );
   MPI_Comm_size( MPI_COMM_WORLD, &num_procesos_actual );


   if ( num_procesos == num_procesos_actual )
   {
      // ejecutar la función correspondiente a 'id_propio'
      if ( id_propio == id_camarero )
      	funcion_camarero();
      else if ( id_propio % 2 == 0 )          // si es par
         funcion_filosofos( id_propio ); //   es un filósofo
      else                         // si es impar
         funcion_tenedores( id_propio ); //   es un tenedor
   }
   else
   {
      if ( id_propio == 0 ) // solo el primero escribe error, indep. del rol
      { cout << "el número de procesos esperados es:    " << num_procesos << endl
             << "el número de procesos en ejecución es: " << num_procesos_actual << endl
             << "(programa abortado)" << endl ;
      }
   }

   MPI_Finalize( );
   return 0;
}

// ---------------------------------------------------------------------
