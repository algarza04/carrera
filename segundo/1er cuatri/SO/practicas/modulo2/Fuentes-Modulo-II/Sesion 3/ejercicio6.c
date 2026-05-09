#include<sys/types.h>
#include<sys/wait.h>
#include<unistd.h>
#include<stdio.h>
#include<errno.h>
#include<stdlib.h>
int main(int argc, char *argv[]){
pid_t pid;
int estado;
if(argc<2){
printf("Sintaxis incorrecta\n");
exit(-1);
}

if( (pid=fork())<0) {
perror("\nError en el fork");
exit(-1);
}
else
if(pid==0) { //proceso hijo ejecutando el programa
if( (execl(argv[1], "cat","prueba1",NULL)<0)) {
perror("\nError en el execl");
exit(-1);
}
}
wait(&estado);
printf("\nMi hijo %d ha finalizado con el estado %d\n",pid,estado);
exit(0);
}
