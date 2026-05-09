// -----------------------------------------------------------------------------
// Hecho por: Mehdi Iabouten
// DNI: K568645
// -----------------------------------------------------------------------------



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
  num_filo_ten  = 2*num_filosofos , // número de filósofos y tenedores 
  num_procesos  = num_filo_ten+1 ,   // número de procesos total (por ahora solo hay filo y ten)
  etiq_solic    = 0 ,
  etiq_solt     = 1 , 
  etiq_sent     = 2 ,
  etiq_levan    = 3 ,
  etiq_aviso    = 7 ,
  id_camarero   = 10,
  id_borrachuzo = 4;

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
  int peticion , valor, 
    id_ten_izq = (id+1)              % num_filo_ten, //id. tenedor izq.
    id_ten_der = (id+num_filo_ten-1) % num_filo_ten; //id. tenedor der.
    
   MPI_Status estado ;       // metadatos de las dos recepciones
    
  while ( true )
  {
    cout <<"Filósofo " <<id << " solicita sentarse." <<endl;
    MPI_Ssend(&peticion, 1, MPI_INT, id_camarero, etiq_sent, MPI_COMM_WORLD);
    
    if (id == id_borrachuzo){
	    MPI_Recv( &valor, 1, MPI_INT, id_camarero, etiq_aviso, MPI_COMM_WORLD, &estado );
	    
	    if (valor == 2)
	    	cout << "Gracias colegs, si no es porque sois muy formales, os invitaba a un cubata. " <<endl;
    }
    
    cout <<"Filósofo " <<id << " solicita ten. izq." <<id_ten_izq <<endl;
    MPI_Ssend(&peticion, 1, MPI_INT, id_ten_izq, etiq_solic, MPI_COMM_WORLD);

    cout <<"Filósofo " <<id <<" solicita ten. der." <<id_ten_der <<endl;
    MPI_Ssend(&peticion, 1, MPI_INT, id_ten_der, etiq_solic, MPI_COMM_WORLD);

    cout <<"Filósofo " <<id <<" comienza a comer" <<endl ;
    sleep_for( milliseconds( aleatorio<10,100>() ) );  

    cout <<"Filósofo " <<id <<" suelta ten. izq. " <<id_ten_izq <<endl;
    MPI_Ssend( &peticion, 1, MPI_INT, id_ten_izq, etiq_solt, MPI_COMM_WORLD );

    cout<< "Filósofo " <<id <<" suelta ten. der. " <<id_ten_der <<endl;
    MPI_Ssend( &peticion, 1, MPI_INT, id_ten_der, etiq_solt, MPI_COMM_WORLD );

    cout<< "Filósofo " <<id <<" se levanta. " <<endl;
    MPI_Ssend( &peticion, 1, MPI_INT, id_camarero, etiq_levan, MPI_COMM_WORLD );
    
    if (id == id_borrachuzo)
	    MPI_Send( &valor, 1, MPI_INT, id_camarero, etiq_aviso, MPI_COMM_WORLD);
	    
    cout << "Filosofo " << id << " comienza a pensar" << endl;
    sleep_for( milliseconds( aleatorio<10,100>() ) );
   }
}
// ---------------------------------------------------------------------

void funcion_tenedores( int id )
{
  int valor, id_filosofo ;  // valor recibido, identificador del filósofo
  MPI_Status estado ;       // metadatos de las dos recepciones

  while ( true )
  {
    MPI_Recv( &valor, 1, MPI_INT, MPI_ANY_SOURCE, etiq_solic, MPI_COMM_WORLD, &estado );
     
    id_filosofo = estado.MPI_SOURCE;
     
    cout <<"Ten. " <<id <<" ha sido cogido por filo. " <<id_filosofo <<endl;

    MPI_Recv( &valor, 1, MPI_INT, id_filosofo, etiq_solt, MPI_COMM_WORLD, &estado );
    cout <<"Ten. "<< id<< " ha sido liberado por filo. " <<id_filosofo <<endl ;
  }
}
// ---------------------------------------------------------------------

void funcion_camarero(){
  int valor, id_filosofo, etiq_emisor_aceptable;  // valor recibido, identificador del filósofo
  int s = 0, sentados = 0; 
  MPI_Status estado ;      // metadatos de las dos recepciones
  
  while(true){
    if ( s == 0 )                 // si buffer vacío
      etiq_emisor_aceptable = etiq_sent ;         // solo prod.
      
    else if ( s == 4 )   // si buffer lleno
      etiq_emisor_aceptable = etiq_levan ;        // solo cons.
      
    else                                            // si no vacío ni lleno
      etiq_emisor_aceptable = MPI_ANY_TAG ;
    
    MPI_Recv( &valor, 1, MPI_INT, MPI_ANY_SOURCE, etiq_emisor_aceptable, MPI_COMM_WORLD, &estado );
    id_filosofo = estado.MPI_SOURCE;

    switch( estado.MPI_TAG ) // leer emisor del mensaje en metadatos
    {
      case etiq_sent:
      	if (id_filosofo == id_borrachuzo){
      		int sillas = 0;
      		if (s<=2){
      			cout <<"Filósofo " <<id_filosofo << " se sienta." <<endl;
        		s+=2;	
      			sillas = 2;
      		}
      		
      		else{
      			cout <<"Filósofo borrachuzo sentado en una sola silla." <<endl;
        		s++;
        		sillas = 1;
        	}
        	
        	MPI_Send( &sillas, 1, MPI_INT, id_borrachuzo, etiq_aviso, MPI_COMM_WORLD );
        }
        
        else{	
        	cout <<"Filósofo " <<id_filosofo << " se sienta." <<endl;
        	s++;
        }
        
        sentados++;
        cout << "Número de filósofos sentados--> " << sentados <<endl;
        cout << "Número de sillas ocupadas--> " << s <<endl;
        break;
      
      case etiq_levan:
      	int sillas;
        if (id_filosofo == id_borrachuzo){
        	MPI_Recv( &sillas, 1, MPI_INT, id_borrachuzo, etiq_aviso, MPI_COMM_WORLD, &estado );
        	
        	if (sillas == 1)
        		s--;
        	else if (sillas == 2)
        		s=s-2;
        }	
        
        else{
		cout <<"Filósofo " <<id_filosofo << " se levanta." <<endl;
		s--;
	}
        sentados--;
        break;
  }
  }
}

int main( int argc, char** argv )
{
  int id_propio, num_procesos_actual ;

  MPI_Init( &argc, &argv );
  MPI_Comm_rank( MPI_COMM_WORLD, &id_propio );
  MPI_Comm_size( MPI_COMM_WORLD, &num_procesos_actual );


  if ( num_procesos == num_procesos_actual )
  {
    // ejecutar la función correspondiente a 'id_propio'
    if ( id_propio == 10)
      funcion_camarero();             // es un camarero
    else if ( id_propio % 2 == 0 )          // si es par
      funcion_filosofos( id_propio ); //   es un filósofo
    else                               // si es impar
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
