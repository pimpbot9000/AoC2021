# Advent of Code 2021

## Python lessons learned so far

* One can iterate over string characters using for loop
* Matching parenthesis <-> stack !
* List comprehension is ofter more concise than map
* ```functool``` library has cool ```reduce``` method
* ...then again, reduce is not always the most readable implementation even though cool kids use it
* ```max``` and ```min``` takes a keyword argument ```key``` and lambda function can be passed.
* List comprehension does not work only for lists, but also for sets and even for dictionaries!
* ```numpy``` overloads methods for basic arithmetics i.e array can be multiplied by an integer.
* Even if array lookup is slightly faster, storing points (coordinates) in a set especially when bounds are undefined saves a lot of effort. Lookup for (hash)set is effectively constant time with a reasonably small multiplier.
* ```collections``` library has handy ```defaultdict``` and ```Counter```! Beware, iteration breaks down if unexisting key is accessed since
this modifies the dictionary (creates the nonexisting key-value pair)
* Numpy array can take tuple as argument to access element: one can use ```arr[coordinate]``` instead of painstaking ```arr[i, j]```
* Numpy has every method one can think of for ND arrays!
* ```PriorityQueue``` is a thread-safe wrapper for ```heapq``` making ```heapq``` faster since there's no overhead from locking
* Dijkstra is a special case of A* algorithm (I guess I knew this already)
* Keyword ```nonlocal``` can be used to access variable outside function scope (especially handy when recursion)
* Sommore recursion with memoization!

