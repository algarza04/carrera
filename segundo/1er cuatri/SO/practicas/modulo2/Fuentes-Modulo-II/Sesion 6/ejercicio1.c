#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>

/**
 * @brief Implementa un programa que ejecuta un comando y realiza redirección de E/S.
 * * Uso: ./ejercicio1 <comando> "<"|<"> <archivo>
 */
int main(int argc, char *argv[]) {
    int fd;

    if (argc != 4) {
        printf("\nParámetros incorrectos");
        return 1;
    }

    char *comando = argv[1];
    char *redireccion = argv[2];
    char *fichero = argv[3];


    if (strcmp(redireccion,"<") == 0){
        if ((fd = open(fichero,O_RDONLY)) <0) {
        	perror("Error al abrir fichero de entrada");
            exit(-1);
         }
        dup2(fd,STDIN_FILENO);
    } else if (strcmp(redireccion,">") == 0){
        if((fd = open(fichero, O_CREAT|O_TRUNC|O_WRONLY, 0644)) <0) {
        	perror("Error al abrir fichero de salida");
            exit(-1);
         }
        dup2(fd,STDOUT_FILENO);
    }else {
        printf("\nSímbolo de redireccion incorrecto");
        return 1;
    }
    close(fd);
    
    if ( execlp(comando, comando, NULL) < 0){
		perror("Error en la ejecucion de execlp");
    	exit(-1);
    }
    return 0;

}
