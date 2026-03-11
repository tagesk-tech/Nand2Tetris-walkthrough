The Main file in this folder is provided for testing your implementation of 
wasteful and recycling memory allocation. It tests whether 
- it is possible to allocate more memory than available on the heap, 
- your implementation does defragmentation upon deallocation, 
and it assesses the efficiency of your memory allocation function.

The file will cause an error (Heap overflow) with the standard Memory implementation, but it should not cause such an error with your implementation.

Note: there are two conventions for handling the case that there is insufficient free heap space for serving a memory allocation request. One convention is to abort the program (this is what Java and Matlab do by default). The other convention is to return 0 (often called 'null' or 'NULL'), and let the programmer handle the issue. We follow the latter convention.
