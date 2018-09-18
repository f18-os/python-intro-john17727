# Shell Project

## shell.py
The program implements a shell that can do input and ouput redirects and a pipe. Mix and matching is not a feature and therefore buggy.

### Output Redirect
Closes stdout and changes it to a user defined file.
```python
os.close(1)
sys.stdout = open(args[count], "w")
fd = sys.stdout.fileno()
os.set_inheritable(fd, True)
```

### Input Redirect
Opens the file to be read and saves the contents as arguments in a list.
```python
with open(args[count], "r") as inRedir:
    for line in inRedir:
        line = line.strip()
        newArgs.append(line)
```

### Pipe
Creates a pipe and makes it inheritable. Some code inspired by in a collaboration with Alan Uribe. See COLLABORATION.md under Alan Uribe.
```python
r, w = os.pipe()

for f in (r, w):
    os.set_inheritable(f, True)
```

In child, read is closed and write is duplicated into another file descriptor.
```python
os.close(r)
fd = sys.stdout.fileno()
os.dup2(w, fd)
```

In parent, write is closed and read is duplicated.
```python
os.close(w)
fd = sys.stdin.fileno()
os.dup2(r, fd)
```