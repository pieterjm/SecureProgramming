#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv)  
{
  volatile int debug;
  char buffer[64];

  // change debug to enable debugging in god mode
  debug = 0x00;

  // one argument is required
  if ( argc == 2 ) {
    strcpy(buffer, argv[1]);
  } else {
    exit(-1);
  }

  fprintf(stderr,"debug = %08x\n",debug);
  
  if(debug == 0x50 ) {
    exit(2);
  } else {
    exit(1);
  }
}

