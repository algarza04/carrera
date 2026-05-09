#include <sys/types.h>
#include <stdbool.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <errno.h>


int main(int argc, char *argv[]){
	pid_t pid,pid_terminado;
	int estado, num_hijos=5,hijos_vivos=0;
	
	
	for (int i = 0; i < num_hijos; i++) {
		hijos_vivos++;
		printf("		Tengo %d hijos vivos\n", hijos_vivos);
		if ((pid=fork()) == -1) {
			printf("\nError en la creación del hijo");
			exit(-1);
		}
		if (pid == 0)	break;
	}
	if (pid == 0){
		printf("Soy el hijo %d y mi padre es %d\n", getpid(), getppid());
		exit(0);
	}
	
	while (hijos_vivos!=0){
		pid_terminado = wait(&estado);
		
		hijos_vivos--;
		printf("	Acabo de finalizar mi hijo con PID %d Sólo me quedan %d hijos vivos\n", pid_terminado,hijos_vivos);
		
	}
	return 0;
}

/*


































int main(int argc, char *argv[]) {
	int hijos_vivos=0, estado;
	
	printf("\nSoy el proceso padre %d\n", getpid());
	pid_t pid;
	pid_t pid_terminado;
	
    for (int i = 1; i <= 5; i++) {
        pid = fork();
    	hijos_vivos++;
		
        if (pid < 0) {
            printf("\nError en el fork\n");
            exit(-1);
        }
        if (pid == 0){

        	printf("Soy el hijo %d, y he sido creado %d\n", getpid(), i);
        	exit(0);	
        }
    }
    
    while (hijos_vivos > 0){
    	pid_terminado = wait(&estado);
		hijos_vivos--;
    	printf("Acaba de finalizar mi hijo %d\n", pid_terminado);
    	printf("Sólo me quedan %d hijos vivos\n", hijos_vivos); 
    }
    
    return 0;
}*/
