/* Ben Santos 2/27/2020 CS 208
*
*/
#include "cachelab.h"
#include <getopt.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <limits.h>


int main(int argc, char** argv)
{
  /*three things we need to know: hits, misses, evicts*/
  int hit_count = 0;
  int miss_count = 0;
  int eviction_count = 0;

  /*how we will store adresses*/
  typedef unsigned long long int mem_address;
  /*organizing all the values we have/need for easier access later on*/
  struct cache_variables{
    /*set index*/
    int s;
    /*number of sets*/
    int S;
    /*number of lines per set*/
    int E;
    /*offset bits - not really that important, but need to calcualte block size */
    int b;
    /*cache block size*/
    int B;
  };
  /*info will hold all our cache variables*/
  struct cache_variables info;

  /*get arguements from command line and store them in variables*/
  int opt, argSetBits, argLines, argOffsetBits;
  char filename[100];

  while( -1 != (opt = getopt(argc, argv, "s:E:b:t:"))){
    switch (opt) {
      case 's':
        argSetBits = atoi(optarg);
        printf("The number of set bits is: %d\n" , argSetBits);
        info.s = argSetBits;
        break;
      case 'E':
        argLines = atoi(optarg);
        printf("The number of lines is: %d\n" , argLines);
        info.E = argLines;
        break;
      case 'b':
        argOffsetBits = atoi(optarg);
        printf("The number of offset bits is: %d\n" , argOffsetBits);
        info.b = argOffsetBits;
        break;

      case 't':
        strncpy(filename, optarg, 100);
        printf("The trace file name is: %s\n", filename);

    }
  }
  /*final calculations to fill out info*/
  info.S = (1 << info.s);
  info.B = (1 << info.b);

  /*structure of a cache line */
  typedef struct{
    int valid;
    int counter;
    mem_address tag;
  } cache_line;

  /*structure of a cache set, pointer to an array of lines*/
  typedef struct{
    cache_line *lines;
  } cache_set;

  /*structure of a cache, pointer to an array of sets*/
  typedef struct {
    cache_set *sets;
  } cache_struct;

  /*allocating space for all of our elements*/
  cache_struct cache;
  cache.sets = malloc(info.S * sizeof(cache_set));
  for (int i = 0; i < info.S; i++){
    cache.sets[i].lines = malloc(info.E * sizeof(cache_line));
  }




  /*parsing text file */
  FILE * filePointer;
  filePointer = fopen (filename, "r"); /*open for reading */

  /*more utility variables for cache*/
  char operation; /*L,S,M*/
  mem_address addr;
  int size;
  int hit_boolean = 0;
  int LRUcounter = 0;
  int openLine = -1;
  int evict = 0;

  if (filePointer == NULL){
    printf("File pointer is NULL\n");
    exit(1);

  }
  while(fscanf (filePointer," %c %llx, %d", &operation, &addr, &size) > 0){
    if (operation != 'I') {
      printf("%c %llx, %d\n", operation, addr, size);
      /*get set index*/
      mem_address tag = addr >> (info.b + info.s);
      int tag_size = (64 - (info.b + info.s));
      unsigned long long temp = addr << tag_size;
      unsigned long long setindex = temp >> (tag_size + info.b);
      cache_set set = cache.sets[setindex];
      int compare = INT_MAX;

      /*iterate through each line in set and check whether or not tags match*/
      for (int i = 0; i < info.E; i++) {
        /*only perform iteration if valid bit is set*/
        if (set.lines[i].valid == 1) {
          /*if tag matches*/
          if (set.lines[i].tag == tag) {
            /*we have a hit!*/
            hit_count++;
            /*hit_boolean is true*/
            hit_boolean = 1;
            /*update counter*/
            set.lines[i].counter = LRUcounter;
            LRUcounter++;
          }
          /*valid bit is set, but none of the tags match. this means eviction*/
          else if(set.lines[i].counter < compare){
            compare = set.lines[i].counter;
            evict = i;
          }
        }
        /*found an empty line to insert address*/
        else if(openLine == -1){
          openLine = i;
        }
      }

     /*no line found with matching tag -> miss!*/
     if (hit_boolean != 1) {
       miss_count++;
       if(openLine > -1) {
        /*create entry: set valid bit, set tag, start LRUcounter*/
        set.lines[openLine].tag = tag;
        set.lines[openLine].valid = 1;
        set.lines[openLine].counter = LRUcounter;
        LRUcounter++;
       }
       /*no space, we must evict*/
       else if (openLine < 0){
         set.lines[evict].tag = tag;
         set.lines[evict].counter = LRUcounter;
         LRUcounter++;
         eviction_count++;
       }

      }
      openLine = -1;
      hit_boolean = 0;
    }

    if (operation == 'M') {
      hit_count++;
    }
  /*end of while loop*/
}

  /*freeing what was malloced*/
  for (int i = 0; i < info.S; i++){
    free(cache.sets[i].lines);
  }
  free(cache.sets);



  fclose(filePointer);
  printSummary(hit_count, miss_count, eviction_count);
}
