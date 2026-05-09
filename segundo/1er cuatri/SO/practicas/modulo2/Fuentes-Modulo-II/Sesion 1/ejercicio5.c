#include<sys/types.h>  	//Primitive system data types for abstraction of implementation-dependent data types.
						//POSIX Standard: 2.6 Primitive System Data Types <sys/types.h>
#include<sys/stat.h>
#include<pwd.h>
#include<fcntl.h>
#include<stdlib.h>
#include<stdio.h>
#include<errno.h>
#include<unistd.h>
#include <string.h>

int main(int argc, char *argv[]) {
    int fd;
    struct stat atributos;
    struct passwd *pwd;

    if (argc != 2) {
        printf ("\nNúmero incorrecto de parámetros\n");
        exit(-1);
    }

    if (fd=open(argv[1], ENOENT) < 0){
        printf("\nError %d en open\n", errno);
        perror("\nError en open");
        exit(-1);
    }
    if (fd=open(argv[1], O_RDONLY) < 0){
        printf("\nError %d en open\n", errno);
        perror("\nError en open");
        exit(-1);
    }

    if (stat(argv[1], &atributos) < 0){
        printf("\nError %d en open\n", errno);
        perror("\nError en open");
        exit(-1);
    } else {
        pwd = getpwuid(atributos.st_uid);
        printf("\nNombre archivo: %s", argv[1]);
        printf("Tamaño en bytes: %ld", atributos.st_size);
        printf("\nPermisos: %o", atributos.st_mode & 0777);
        printf("\nPropietario: %s", pwd->pw_name);
    }

    if (close(fd) < 0){
        printf("\nError %d en open\n", errno);
        perror("\nError en open");
        exit(-1);
    } else{
        printf("\nArchivo cerrado correctamente\n\n");
        return 0;
    }
}
