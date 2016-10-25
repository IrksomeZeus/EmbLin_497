// Program to test mem speed
// ECE497 Embedded 32bit Linux @ Rose-Hulman Institute of Technology
// Austin Yates  Oct 25, 2016

#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <signal.h>
#include "beaglebone_gpio.h"

#define GPIO_IN = GPIO_17
#define GPIO_OUT = GPIO_19

int keepgoing = 1;

void signal_handler(int sig){
  printf("\nCtrl-C pressed, cleaning up and exiting...\n");
  keepgoing = 0;
}

int main(int argc, char *argv[]){

  volatile void *gpio_addr;
  volatile unsigned int *gpio_oe_addr;
  volatile unsigned int *gpio_datain;
  volatile unsigned int *gpio_setdataout_addr;
  volatile unsigned int *gpio_cleardataout_addr;

  signal(SIGINT, signal_handler);

  int fd = open("/dev/mem", O_RDWR);

  gpio_addr = mmap(0, GPIO3_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, GPIO3_START_ADDR);

  gpio_oe_addr           = gpio_addr + GPIO_OE;
  gpio_datain            = gpio_addr + GPIO_DATAIN;
  gpio_setdataout_addr   = gpio_addr + GPIO_SETDATAOUT;
  gpio_cleardataout_addr = gpio_addr + GPIO_CLEARDATAOUT;

  if(gpio_addr == MAP_FAILED) {
    printf("Unable to map GPIO\n");
    exit(1);
  }

  while(keepgoing) {
    if(*gpio_datain & GPIO_IN){
      *gpio_setdataout_addr = GPIO_OUT;
    }
    else{
      *gpio_cleardataout_addr = GPIO_OUT;
    }
  }

  munmap((void *)gpio_addr, GPIO3_SIZE);
  close(fd);
  return 0;
}
