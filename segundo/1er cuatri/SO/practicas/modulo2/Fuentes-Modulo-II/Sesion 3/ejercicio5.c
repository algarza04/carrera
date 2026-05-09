#include <sys/types.h>
#include <stdbool.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <errno.h>


int main(int argc, char *argv[]){
	int PIDs[5];
	int estado, num_hijos=5,hijos_vivos=0;
	
	
	for (int i = 1; i <= num_hijos; i++) {
		hijos_vivos++;
		printf("		Tengo %d hijos vivos\n", hijos_vivos);
		if ((PIDs[i]=fork()) == -1) {
			printf("\nError en la creación del hijo");
			exit(-1);
		}
		if (PIDs[i] == 0){
			printf("%d Soy el hijo %d y mi padre es %d\n", i,getpid(), getppid());
			exit(0);
		}
	}
	
	for (int i = 1; i <= num_hijos;i+=2){
		waitpid(PIDs[i],&estado);
		hijos_vivos--;
		printf("	Acabo de finalizar mi hijo con PID %d Sólo me quedan %d hijos vivos\n", PIDs[i],hijos_vivos);
	}
	for (int i = 2; i < num_hijos;i+=2){
		waitpid(PIDs[i],&estado);
		hijos_vivos--;
		printf("	Acabo de finalizar mi hijo con PID %d Sólo me quedan %d hijos vivos\n", PIDs[i],hijos_vivos);
	}
	return 0;
}
