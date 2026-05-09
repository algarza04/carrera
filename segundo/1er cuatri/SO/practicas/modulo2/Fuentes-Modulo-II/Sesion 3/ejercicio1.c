#include <sys/types.h>
#include <stdbool.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <errno.h>

int main(int argc, char *argv[]) {
    pid_t pid;
    if (argc != 2) {
        printf("\nNumero incorrecto de argumentos");
        return 1;
    }

    const int numero = atoi(argv[1]);
    pid = fork();
    if (pid < 0) {
        perror("\nError en fork");
        return 1;
    } else {
        if (pid == 0) {
            printf("\nProceso hijo %d calculando", getpid());
            printf("\nMi padre es %d", getppid());
            if (numero % 2 == 0)
                printf("\nEl proceso %d ha calculado que el numero %d es par", getpid(), numero);
            else
                printf("\nEl proceso %d ha calculado que el numero %d es impar", getpid(), numero);
        }
        else if (pid){
            printf("Hola , soy el proceso padre y mi pid es: %d y el de mi hijo es %d, y voy a comprobar si el numero introducido es divisible por 4 \n", getpid(), pid);
            if (numero % 4 == 0)
                printf("\nEl proceso %d ha calculado que el numero %d es multiplo de 4\n", getpid(), numero);
            else
                printf("\nEl proceso %d ha calculado que el numero %d no es multiplo de 4\n", getpid(), numero);
            
        }
    }
    
    return 0;
}
