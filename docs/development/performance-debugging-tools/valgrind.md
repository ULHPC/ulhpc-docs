[![](https://upload.wikimedia.org/wikipedia/en/f/f9/Valgrind_logo.png){: style="width:300px;float: right;" }](https://valgrind.org/)
The [Valgrind](https://valgrind.org/) tool suite provides a number of debugging and profiling
tools that help you make your programs faster and more correct. The
most popular of these tools is called Memcheck which can detect
many memory-related errors and memory leaks.

### Prepare Your Program

Compile your program with -g to include debugging information so
that Memcheck's error messages include exact line numbers. Using
-O0 is also a good idea, if you can tolerate the slowdown. With -O1
line numbers in error messages can be inaccurate, although generally
speaking running Memcheck on code compiled at -O1 works fairly well,
and the speed improvement compared to running -O0 is quite significant.
Use of -O2 and above is not recommended as Memcheck occasionally
reports uninitialised-value errors which don't really exist.

## Environmental models for Valgrind in ULHPC


```bash
$ module purge
$ module load debugger/Valgrind/3.15.0-intel-2019a
```


## Interactive mode

Example code:
```cpp
#include <iostream>                                                                                           
using namespace std;                                                                                          
int main()                                                                                                    
{                                                                                                             
  const int SIZE = 1000;                                                                                      
  int *array = new int(SIZE);                                                                                 
                                                                                                              
  for(int i=0; i<SIZE; i++)                                                                                   
    array[i] = i+1;                                                                                           
                                                                                                              
  // delete[] array                                                                                           
                                                                                                              
  return 0;                                                                                                   
}
```

```bash
# Compilation
$ icc -g example.cc

# Code execution
$ valgrind --leak-check=full --show-leak-kinds=all ./a.out
```
Result output (with leak)

If we do not delete `delete[] array` the memory, then there will be a memory leak.
```bash
==26756== Memcheck, a memory error detector
==26756== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==26756== Using Valgrind-3.15.0 and LibVEX; rerun with -h for copyright info
==26756== Command: ./a.out
==26756== 
==26756== Invalid write of size 4
==26756==    at 0x401275: main (mem-leak.cc:10)
==26756==  Address 0x5309c84 is 0 bytes after a block of size 4 alloc'd
==26756==    at 0x402DBE9: operator new(unsigned long) (vg_replace_malloc.c:344)
==26756==    by 0x401265: main (mem-leak.cc:8)
==26756== 
==26756== 
==26756== HEAP SUMMARY:
==26756==     in use at exit: 4 bytes in 1 blocks
==26756==   total heap usage: 2 allocs, 1 frees, 72,708 bytes allocated
==26756== 
==26756== 4 bytes in 1 blocks are definitely lost in loss record 1 of 1
==26756==    at 0x402DBE9: operator new(unsigned long) (vg_replace_malloc.c:344)
==26756==    by 0x401265: main (mem-leak.cc:8)
==26756== 
==26756== LEAK SUMMARY:
==26756==    definitely lost: 4 bytes in 1 blocks
==26756==    indirectly lost: 0 bytes in 0 blocks
==26756==      possibly lost: 0 bytes in 0 blocks
==26756==    still reachable: 0 bytes in 0 blocks
==26756==         suppressed: 0 bytes in 0 blocks
==26756== 
==26756== For lists of detected and suppressed errors, rerun with: -s
==26756== ERROR SUMMARY: 1000 errors from 2 contexts (suppressed: 0 from 0)
```

Result output (without leak)

When we delete `delete[] array` the allocated memory, there will not be leaked memory.
```bash
==26172== Memcheck, a memory error detector
==26172== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==26172== Using Valgrind-3.15.0 and LibVEX; rerun with -h for copyright info
==26172== Command: ./a.out
==26172== 
==26172== 
==26172== HEAP SUMMARY:
==26172==     in use at exit: 4 bytes in 1 blocks
==26172==   total heap usage: 2 allocs, 1 frees, 72,708 bytes allocated
==26172== 
==26172== 4 bytes in 1 blocks are definitely lost in loss record 1 of 1
==26172==    at 0x402DBE9: operator new(unsigned long) (vg_replace_malloc.c:344)
==26172==    by 0x401283: main (in /mnt/irisgpfs/users/ekrishnasamy/BPG/Valgrind/a.out)
==26172== 
==26172== LEAK SUMMARY:
==26172==    definitely lost: 4 bytes in 1 blocks
==26172==    indirectly lost: 0 bytes in 0 blocks
==26172==      possibly lost: 0 bytes in 0 blocks
==26172==    still reachable: 0 bytes in 0 blocks
==26172==         suppressed: 0 bytes in 0 blocks
==26172== 
==26172== For lists of detected and suppressed errors, rerun with: -s
==26172== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
```

## Additional information 

This page is based on the "Valgrind Quick Start Page". For more
information about valgrind, please refer to
[http://valgrind.org/](http://valgrind.org/).

!!! tip
    If you find some issues with the instructions above,
    please report it to us using [support ticket](https://hpc.uni.lu/support).
