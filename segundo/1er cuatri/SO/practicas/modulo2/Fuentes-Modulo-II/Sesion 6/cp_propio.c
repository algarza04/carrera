#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <sys/mman.h>

int main(int argc, char *argv[]){
    struct stat atributos;
    int tamanio_origen = 0;
    int fd_origen, fd_destino;
    char *ptr_origen, *ptr_destino;

    if (argc != 3){
        printf("\nParámetros incorrectos: ./cp_propio fichero_origen fichero_destino");
        exit(-1);
    }

    char *fichero_origen = argv[1];
    char *fichero_destino = argv[2];

    if ((fd_origen = open(fichero_origen, O_RDONLY))<0) {
        printf("\nError al abrir el fichero_origen %s", fichero_origen);
        perror("\nError en open");
        exit(-1);
    }
    if ((fd_destino = open(fichero_destino, O_CREAT|O_TRUNC|O_RDWR, 0644))<0) {
        printf("\nError al abrir el fichero_destino %s", fichero_destino);
        perror("\nError en open");
        exit(-1);
    }
    if (fstat(fd_origen, &atributos) < 0){
        printf("\nError al intentar acceder a los atributos de %s", fichero_origen);
        perror("\nError en lstat");
        exit(-1);
    }

    tamanio_origen = atributos.st_size;
    ftruncate(fd_destino, tamanio_origen);
    printf("\nTam origen %d", tamanio_origen);
    ptr_origen = (char *) mmap(0,atributos.st_size,PROT_READ,MAP_SHARED,fd_origen,0);
    ptr_destino = (char *) mmap(0,atributos.st_size,PROT_WRITE,MAP_SHARED,fd_destino,0);

    if (ptr_origen == MAP_FAILED) {
        perror("\nFallo la proyeccion1");
        exit(-1);
    }
    if (ptr_destino == MAP_FAILED) {
        perror("\nFallo la proyeccion2");
        exit(-1);
    }

    memcpy(ptr_destino, ptr_origen, tamanio_origen);

    munmap(ptr_origen, tamanio_origen);
    munmap(ptr_destino, tamanio_origen);

    close(fd_origen);
    close(fd_destino);

    return 0;

}
