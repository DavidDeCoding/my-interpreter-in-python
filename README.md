# my-interpreter-in-python

This implements the interpreter from the video series: https://www.youtube.com/playlist?list=PL_2VhOvlMk4UHGqYCLWc6GO8FaPl8fQTh but in Python.

But it also adds if-else conditionals and while-break-continue looping.

# To run the interpreter - REPL mode
It comes with its REPL. Just run the main.py with:

```
$ python3 main.py
```

# To run the interpreter - File mode
It can also run a file with the code for the language. You just create a file called *object.txt* and replace the **repl()** with **run()** in the main.py. And run:

```
$ python3 main.py
```
# Using the Language

## Binary Operations
Here are examples of binary operations:

**Addition, Subtraction, Multiplication, Division, Modulus:**
```
> 1 + 1
{ value: 2 }
> 1 - 1
{ value: 0 }
> 1 * 1
{ value: 1 }
> 1 / 1
{ value: 1 }
> 1 % 1
{ value: 0 }
```
**Mixing it up:**
```
> 2 * 1 - 1 * 1
{ value: 1 }
```
**Comparison:**
```
> 2 > 1
{ value: "true" }
> 2 == 2
{ value: "true" }
> 2 != 1
{ value: "true" }
```
**Logical:**
```
> 2 > 1 && 1 > 2
{ value: "false" }
```

**String Addition:**
```
> let x = "Hello";
{ type: "string", value: "Hello" }
> x = x + ", World!"
{ type: "string", value: "Hello, World!" }
```

## Declare Variable
We can declare a variable and then reassign it
**Declare Mutable Variable as a primitive and reassign:**
```
> let x = 1;
{ value: 1 }
> x = 2
{ value: 2 }
```
**Declare Constants:**
```
> const x = 1;
{ value: 1 }
```
**Declare Mutable Variable as an object:**
```
> let x = { a: 1, b: 2 };
```
**Reassign member value:**
```
> x.a = 2
```

## Declare Function
We can declare a function
**Declare a function:**
```
> fn add(x, y) { x + y }
> add(1, 2)
{ value: 3 }
```

## Conditionals
We can use if-else statements
**If-Else:**
```
let x = 1;
> if (1 > 2) { x = 2 } else { x = 1 }
```

## Loops
We can use while-break-continue statements
**While-Break-Continue:**
```
> let x = 2;
{ value: 2 }
> while (x > 1) { x = x - 1 }
> while (1 == 1) { break }
```

# Why build this?
I loved the bhai-lang project and wanted to run how to build an interpreter. This led me to the video series, which uses typescript. But I wanted it to be available to all folks who love Python like me, so I have written the entire thing in Python. Not only that, the video series doesn't implement if-else conditionals, or while-break-continue looping construct, which I do. Enjoy learning!
