#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <errno.h>
#include <dirent.h>
#include <string.h>
#define mymask(mode) ((mode) & ~S_IFMT)
// Permisos de ejecución para grupo y otros.
#define S_IFXGRPOTH 011
// Se define la macro con la regla para comprobar si tiene permiso x en grupo yotros.
#define regla1(mode) ((((mode) & ~S_IFMT) & 011) == S_IFXGRPOTH)
void busca_dir(DIR *dir_ptr, char pathname[],int *tam_arch, int *num_reg) {
    struct dirent *entry;
    char cadena[500];
    struct stat atributos;
    DIR *direct_act;

    while ((entry = readdir(dir_ptr)) != NULL) {
        if (strcmp(entry->d_name, ".") != 0 && strcmp(entry->d_name, "..") != 0){
            sprintf(cadena, "%s/%s", pathname, entry->d_name);

            if (stat(cadena, &atributos) < 0){
                printf("\nError al intentar acceder a los atributos de %s", entry->d_name);
                perror("\nError en lstat");
            }

            if(S_ISDIR(atributos.st_mode)){
                direct_act = opendir(cadena);
                if (direct_act == NULL)
                    perror("\nError al abrir el directorio");
                else
                    busca_dir(direct_act, cadena, tam_arch, num_reg);
            }
            else {
                if (S_ISREG(atributos.st_mode)){
                    if (regla1(atributos.st_mode)){
                                            printf("%s %ld \n", cadena, atributos.st_ino);

                        (*tam_arch)+= (int) atributos.st_size;
                        (*num_reg)++;
                    }
                }
            }
        }
    }

    closedir(dir_ptr);
}

int main(int argc, char *argv[]){
    DIR *dir_ptr;
    char pathname[500];
    struct stat atributos;
    int tam_arch=0, num_reg=0;

    if (argc == 2) {
        strcpy(pathname,argv[1]);
    }
    else if (argc == 1){
        strcpy(pathname,".");
    }
    else{
        printf("\nNúmero incorrecto de parámetros\n");
        return 1;
    }

    const char *directorio = pathname;

    dir_ptr = opendir(directorio);

    if (dir_ptr == NULL) {
        perror("\nError al abrir el directorio");
        return 1;
    }

    busca_dir(dir_ptr, pathname, &tam_arch, &num_reg);

    printf("\nExisten %d archivos regulares con permiso x para grupo y otros", num_reg);
    printf("\nEl tamaño total ocupado por dichos archivos es %d bytes", tam_arch);

    return 0;
}