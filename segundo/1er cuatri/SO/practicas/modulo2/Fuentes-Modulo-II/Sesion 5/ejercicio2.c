#include <sys/types.h> //POSIX Standard: 2.6 Primitive System Data Types 
// <sys/types.h>
#include<limits.h> //Incluye <bits/posix1_lim.h> POSIX Standard: 2.9.2 //Minimum    //Values Added to <limits.h> y <bits/posix2_lim.h>
#include <unistd.h> //POSIX Standard: 2.10 Symbolic Constants         <unistd.h>
#include <sys/stat.h>
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <errno.h>
static int recibida[35];
static void handler(int signum){
	recibida[signum]++;
	printf("Señal %d recibida %d veces\n", signum, recibida[signum]);
	//fflush(stdout);
}
int main(int argc, char *argv[])
{
	struct sigaction sa;
	
	if (setvbuf(stdout,NULL,_IONBF,0))
		perror("\nError en setvbuf\n");
		
	sa.sa_handler = handler;
	//sigemptyset(&sa.sa_mask);
	sigfillset(&sa.sa_mask);
	
	sa.sa_flags = SA_RESTART;
	
	for (int i = 1; i <= 35; i++)
		recibida[i]=0;
		
	
	for ( int i = 1 ; i<=35 ; i++){
		if (sigaction(i, &sa, NULL) == -1)
		{
			printf("No puedo caputar la señal %d\n",i);
			//fflush(stdout);
		}
	}
	
	while(1);
}
