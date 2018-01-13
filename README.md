
# Random Art
A Python implementation of Random Art as described in Perrig & Song 1999.

## Grammar
```
E := (C,C,C)

A := rand in [-1,1]   (1/3)
  |  x                (1/3)
  |  y                (1/3)
  
C := A                (1/4)
  |  add(C,C)         (3/8)
  |  mult(C,C)        (3/8)
```


## Reference
Perrig, Adrian, and Dawn Song. "Hash visualization: A new technique to improve real-world security." International Workshop on Cryptographic Techniques and E-Commerce. 1999.
