/*
tarea3.c
Trabajo con llamadas al sistema del Sistema de Archivos ''POSIX 2.10 compliant''
Este programa fuente está pensado para que se cree primero un programa con
la parte de CREACION DE ARCHIVOS y se haga un ls -l para fijarnos en los
permisos y entender la llamada umask.
En segundo lugar (una vez creados los archivos) hay que crear un segundo programa
con la parte de CAMBIO DE PERMISOS para comprender el cambio de permisos relativo
a los permisos que actualmente tiene un archivo frente a un establecimiento de
permisos absoluto.
*/
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <errno.h>
/*
Definimos los permisos que queremos solicitar (incluyen escritura
para grupo y otros)
Permisos Solicitados: 0777 (rwxrwxrwx) - Máximo absoluto para simplificar
*/
int main(int argc, char *argv[]) {
int fd1, fd2;
struct stat atributos;
/*
1. Establecer Umask inicial a 0022 (típica) para la prueba de archivo1
Esto restringirá la escritura (w) para grupo y otros.
*/
umask(0022);
printf("--- CREACIÓN DE ARCHIVO1 con umask(0022) ---\n");
/* CREACION DE ARCHIVO1: Los permisos solicitados serán restringidos */
if ((fd1 = open("archivo1", O_CREAT | O_TRUNC | O_WRONLY,
S_IRWXU | S_IRWXG | S_IRWXO)) < 0) {
perror("Error en open(archivo1,...)");
exit(-1);
}
close(fd1); /* Cerrar para que los permisos se fijen */
/* 2. CAMBIAR Umask a 0 (CERO) */
printf("--- CAMBIANDO umask a 0 --- \n");
umask(0); /* Elimina todas las restricciones de permisos. */
/* CREACION DE ARCHIVO2: Los permisos solicitados se respetarán completamente */
if ((fd2 = open("archivo2", O_CREAT | O_TRUNC | O_WRONLY,
S_IRWXU | S_IRWXG | S_IRWXO)) < 0) {
perror("Error en open(archivo2,...)");
exit(-1);
}
close(fd2); /* Cerrar para que los permisos se fijen */
printf("--- RESULTADOS DE LOS PERMISOS DE CREACIÓN ---\n");
/* Mostrar permisos de archivo1 */
if (stat("archivo1", &atributos) == 0) {
printf("archivo1 (umask 0022): 0%o\n", atributos.st_mode & 0777);
}
/* Mostrar permisos de archivo2 */
if (stat("archivo2", &atributos) == 0) {
printf("archivo2 (umask 0000): 0%o\n", atributos.st_mode & 0777);
}
/* CAMBIO DE PERMISOS */
if (stat("archivo1",&atributos) < 0) {
printf("\nError al intentar acceder a los atributos de archivo1");
perror("\nError en lstat");
exit(-1);
}
if (chmod("archivo1", (atributos.st_mode & ~S_IXGRP) | S_ISGID) < 0) {
perror("\nError en chmod para archivo1");
exit(-1);
}
if(chmod("archivo2",S_IRWXU | S_IRGRP | S_IWGRP | S_IROTH) < 0) {
perror("\nError en chmod para archivo2");
exit(-1);
}
return 0;
}