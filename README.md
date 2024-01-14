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

# Why build this?
I loved the bhai-lang project and wanted to run how to build an interpreter. This led me to the video series, which uses typescript. But I wanted it to be available to all folks who love Python like me, so I have written the entire thing in Python. Not only that, the video series doesn't implement if-else conditionals, or while-break-continue looping construct, which I do. Enjoy learning!
