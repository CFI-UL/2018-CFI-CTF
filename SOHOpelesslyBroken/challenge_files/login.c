#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ToHex(Y) (Y>='0'&&Y<='9'?Y-'0':Y-'A'+10)

const char *html = "<html><body><h1>%s</h1></body></html>";
char query_string[4096] = { 0 };
int login_enabled = 0;


void getParam(const char *name, char *value) {
  char *pos1 = strstr(query_string, name);

  if (pos1) {
    pos1 += strlen(name);

    if (*pos1 == '=') { // Make sure there is an '=' where we expect it
      pos1++;

      while (*pos1 && *pos1 != '&') {

        // Convert it to a single ASCII character and store at our Valueination
        if (*pos1 == '%') {
          *value++ = (char)ToHex(pos1[1]) * 16 + ToHex(pos1[2]);
          pos1 += 3;
        } else if ( *pos1=='+' ) {
          // If it's a '+', store a space at our Valueination
          *value++ = ' ';
          pos1++;
        } else {
          // Otherwise, just store the character at our Valueination
          *value++ = *pos1++; }
      }

      *value++ = '\0';
      return;
    }
  }
  strcpy(value, "undefined"); // If param not found, then use default parameter
return;
}


int main(int argc, char *argv[]) {

  int is_valid = 0;
  char username[0x20] = { 0 };
  char password[0x20] = { 0 };

  // Headers
  printf("Content-Type: text/html\n\n");

  strncpy(query_string, getenv("QUERY_STRING"), 4095);
  getParam("username", username);
  getParam("password", password);

  if (login_enabled == 1) {
    if (strcmp(username, "admin") == 0 && strcmp(password, "password") == 0) {
      is_valid = 0x41424344;
    }
  }

  if (is_valid == 0x41424344) {
    printf(html, "Login successful. Here is your flag : ");
    fflush(stdout);
    system("/print_flag");
  } else {
    printf(html, "Login incorrect.");
  }

  return 0;
}
