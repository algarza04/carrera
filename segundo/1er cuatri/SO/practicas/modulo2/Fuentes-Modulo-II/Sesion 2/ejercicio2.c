#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <errno.h>
#include <dirent.h>

int main(int argc, char *argv[]){
    DIR *dir_ptr;
    struct dirent *entry;
    struct stat atributos;
    char path[300];

    if (argc != 3) {
        printf("\nNúmero incorrecto de parámetros\n");
        return 1;
    }

    const char *directorio = argv[1];

    dir_ptr = opendir(directorio);

    if (dir_ptr == NULL) {
        perror("Error al abrir el directorio");
        return 1;
    }

    long permisos = strtol(argv[2],NULL,8);
    printf("\nLos permisos son %ld\n", permisos);

    printf("Nombre_archivo : permisos_antiguos permisos_nuevos");
    while ((entry = readdir(dir_ptr)) != NULL){
        sprintf(path, "%s/%s", directorio, entry->d_name);

        if (lstat(path, &atributos) < 0)  {
            printf("\nError al acceder al atributo %s", entry->d_name);
            perror("\nError en lstat");
            exit(-1);
        }
        else {
            int permisos_antiguos = atributos.st_mode & 0777;
            chmod(path, permisos ) < 0;
            if (chmod(path, permisos ) < 0){
                printf("\n%s : %d %o", entry->d_name, errno, atributos.st_mode & 0777);
            } else {
            if (lstat(path, &atributos) < 0)  {
                printf("\nError al acceder al atributo %s", entry->d_name);
                perror("\nError en lstat");
                exit(-1);
            }
                printf("\n%s : %o %o", entry->d_name, permisos_antiguos,atributos.st_mode & 0777);
            }
        }
    }

    if (closedir(dir_ptr) == -1){
        perror("Error al cerrar el directorio");
        return 1;
    }

    return 0;
}
