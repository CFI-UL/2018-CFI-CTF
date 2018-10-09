#include <stdio.h>
#include <stdlib.h>
int main(int argc, char *argv[]) {

  // Headers
  printf("Content-Type: image/gif\n\n");

  // Body
  char *qs = getenv("QUERY_STRING");
  FILE *f = fopen(qs, "rb");

  char output = 0;

  if (f == NULL) {
    printf("File does not exist.");
    return 0;
  }

  // Get file size
  fseek(f, 0L, SEEK_END);
  unsigned int size = ftell(f);

  rewind(f);
  for (int i = 0; i < size; ++i) {
    output = fgetc(f);
    printf("%c", output);
  }

}
