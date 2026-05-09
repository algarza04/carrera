#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <string.h>
#include <fcntl.h>
#include <dirent.h>
#include <sys/stat.h>
#include <time.h>
#include <errno.h>

int MAX = 300;
int total = 0;
int duplicar(const char *orig, const char *dest)
{
DIR *orig_ptr = opendir(orig);
if (orig_ptr == NULL){
perror("No existe el directorio de origen");
exit(1);
}
DIR *dest_ptr = opendir(dest);
if (dest_ptr == NULL){
// No existe: lo creamos
if (mkdir(dest, 0777) < 0){
perror("mkdir destino");
exit(1);
}} else {
// Existe: comprobamos que sea directorio
struct stat st_aux;
lstat(dest, &st_aux);
if (!S_ISDIR(st_aux.st_mode)) {
perror("Existe pero NO es un directorio");
exit(1);
}
closedir(dest_ptr);
}
struct dirent *dir;
while ((dir = readdir(orig_ptr)) != NULL){
char *name = dir->d_name;
/* Saltamos . y .. */
if (strcmp(name, ".") == 0 || strcmp(name, "..") == 0)
continue;
char o_path[MAX];
char d_path[MAX];
snprintf(o_path, sizeof(o_path), "%s/%s", orig, name);
snprintf(d_path, sizeof(d_path), "%s/%s", dest, name);

struct stat st;
lstat(o_path, &st);
if (S_ISDIR(st.st_mode)) {
mkdir(d_path, st.st_mode & 0777); // umask=0  permisos exactos
total++;
duplicar(o_path, d_path);
}
}
closedir(orig_ptr);
return 0;
}
int main(int argc, char *argv[])
{
if (argc != 3){
fprintf(stderr, "Uso: %s <dir_orig> <dir_dst>\n", argv[0]);
return 1;
}

char *orig=argv[1];
char *dest=argv[2];
umask(0); // Eliminamos umask para conservar permisos
duplicar(orig, dest);
printf("%d\n", total);
return 0;
}
