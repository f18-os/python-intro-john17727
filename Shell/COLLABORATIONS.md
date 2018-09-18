#Collaborations

Most useful code was transferred over from the demo programs.

##Alan Uribe
Inspired changes in the reading and writing of a pipe.
###In child:
Was using:
```python
os.close(1)
os.dup(w)
```
Now using:
```python
os.close(r)
fd = sys.stdout.fileno()
os.dup2(w, fd)
```
###In parent:
Was using:
```python
os.close(0)
os.dup(r)
```
Now using:
```python
os.close(w)
fd = sys.stdin.fileno()
os.dup2(r, fd)
```