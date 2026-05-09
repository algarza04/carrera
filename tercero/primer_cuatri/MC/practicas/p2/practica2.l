%option noyywrap
/*----- Seccion de Declaraciones ----------------*/

%{
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
using namespace std;

ifstream fichero;
ofstream salida;

string convertir_ascii(const char* texto);
%}

CORREO [a-zA-Z0-9._%+-]{3,}@[a-zA-Z0-9.-]{3,}\.[a-zA-Z]{2,}
DNI [0-9]{8}[A-Z]
IBAN ES[0-9]{22} 
TELEFONO \+34[0-9]{9}
DOMICILIO (C\/|Pza|Avda|R)[' '][a-zA-Z' ']{3,}[' '][0-9]{1,}[,][' '][0-9]{1,}[A-Z][,][' '][a-zA-Z' ']{3,}[,][' '][0-9]{5}
FECHAS [0-9]{1,2}(\/|-)[0-9]{1,2}(\/|-)[0-9]{4}
%%
	/*----- Seccion de Reglas ----------------*/
{DNI} {
	string ascii = convertir_ascii(yytext);
	salida << ascii;
}

{CORREO} {
	string ascii = convertir_ascii(yytext);
	salida << ascii;
}

{IBAN} {
	string ascii = convertir_ascii(yytext);
	salida << ascii;
}

{TELEFONO} {
	string ascii = convertir_ascii(yytext);
	salida << ascii;
}

{DOMICILIO} {
	string ascii = convertir_ascii(yytext);
	salida << ascii;
}

{FECHAS} {
	string ascii = convertir_ascii(yytext);
	salida << ascii;
}
.|\n {  
	salida << yytext;
}

%%
/*----- Seccion de Procedimientos --------*/

int main (int argc, char *argv[]){
	if (argc == 3){
		fichero.open (argv[1]);
		salida.open(argv[2]);
		if (!fichero.is_open()){	
			cout << "error de lecura" << endl;
			exit (1);
		}
	
		if (!salida.is_open()) {
			cerr << "Error al abrir el archivo de salida" << endl;
			exit(1);
		}
	}
	else exit(1);

	yyFlexLexer flujo (&fichero,0);
	flujo.yylex();

	return 0;
}

string convertir_ascii(const char* texto) {
	string resultado = "";
	
	for (int i = 0; texto[i] != '\0'; i++) {
		resultado += to_string(static_cast<int>(texto[i])) + " ";
	}
	return resultado;
}
