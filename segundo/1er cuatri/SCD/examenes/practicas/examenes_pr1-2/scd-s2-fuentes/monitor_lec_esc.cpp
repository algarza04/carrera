//c++ -std=c++11 -pthread -o monitor_lec_esc monitor_lec_esc.cpp scd.cpp scd.h

//prioridad a lectores (en el momento que un escritor termina, si hay escritores y lectores esperando, pasan los lectores).
#include <iostream>
#include <cassert>
#include <thread>
#include <mutex>
#include <random> // dispositivos, generadores y distribuciones aleatorias
#include <chrono> // duraciones (duration), unidades de tiempo
#include "scd.h"
#include <iomanip>

using namespace std;
using namespace scd;

constexpr int 
	num_lec = 3,
	num_esc = 3;
	 
class Lec_Esc : public HoareMonitor
{
	private:
		int n_lec;		//numero de lectores leyendo
		bool escrib;	//true si hay algun escritor escribiendo
		CondVar
			lectura,		//para esperar si hay un escritor escribiendo
			escritura;	//para esperar cuando ya haya otro escritor o haya lectores leyendo
	
	public:
		Lec_Esc();
		//invocados por lectores
		void ini_lectura();
		void fin_lectura();
		//invocados por escritores
		void ini_escritura();
		void fin_escritura();
};

Lec_Esc::Lec_Esc(){
	n_lec = 0;
	escrib = false;
	lectura = newCondVar();
	escritura = newCondVar();
}

void Lec_Esc::ini_lectura(){
	if (escrib)
		lectura.wait();
	
	n_lec++;
	cout << "+Lector comienza a leer, número de lectores: " << n_lec << endl;
	lectura.signal();
}

void Lec_Esc::fin_lectura(){
	n_lec--;
	
	cout << "-Lector termina de leer, número de lectores: " << n_lec << endl;
	
	if (n_lec == 0)	//si es el último lector desbloquear un escritor
		escritura.signal();
}

void Lec_Esc::ini_escritura(){
	if (escrib or n_lec > 0)
		escritura.wait();
		
	cout << "		+Escritor comienza a escribir" << endl;
	escrib = true;		//hay un escritor
}

void Lec_Esc::fin_escritura(){
	escrib = false;
		
	cout << "		-Escritor termina de escribir" << endl;
		
	if ( !lectura.empty() )		//al ser prioridad a lectores si hay uno lo despertamos
		lectura.signal();
	else								//si no despertamos un escritor
		escritura.signal();
}

void lector( MRef<Lec_Esc> monitor ){
	while (true){
		monitor->ini_lectura();
		this_thread::sleep_for((chrono::milliseconds) aleatorio<150,200>() );
		monitor->fin_lectura();
		this_thread::sleep_for((chrono::milliseconds) aleatorio<50,100>() );
	} 
}

void escritor( MRef<Lec_Esc> monitor ){
	while ( true ) {
		monitor->ini_escritura();
		this_thread::sleep_for((chrono::milliseconds) aleatorio<150,200>() );
		monitor->fin_escritura();
		this_thread::sleep_for((chrono::milliseconds) aleatorio<50,100>() );
	}
}

int main()
{
	// crear monitor  ('monitor' es una referencia al mismo, de tipo MRef<...>)
   MRef<Lec_Esc> monitor = Create<Lec_Esc>();
   
   thread hebras_lectoras[num_lec], hebras_escritoras[num_esc];
   
   for (int i = 0; i < num_lec; i++)
   	hebras_lectoras[i] = thread(lector, monitor);
   	
   for (int i = 0; i < num_esc; i++)
   	hebras_escritoras[i] = thread(escritor,  monitor);	
   
   for (int i = 0; i < num_lec; i++)
   	hebras_lectoras[i].join();
   
   for (int i = 0; i < num_esc; i++)
   	hebras_escritoras[i].join();
   
}
