import numpy as np
import string

# 1D bar element with area of cross-section, young's modulus, force at multiple nodes, displacement constraints and length of the element given

elements = int(input("Enter the total number of elements in series in the system: "))

# Element stiffness matrix

A = np.array(input("Enter area of cross-section of the elements in sequence (ex. 120,140,130): ").split(","))
print(A)

E = np.array(input("Enter the young's modulus of the elements in sequence (ex. 120,140,130): ").split(","))
print(E)

L = np.array(input("Enter the length of the elements in sequence (ex. 120,140,130): ").split(","))
print(L)

K = np.array([])

for a, e, l in zip(A, E, L):
    K = np.append(K, (int(a)*int(e)/int(l)))

#Assemblying the global stiffness matrix

global_K = np.zeros((elements+1, elements+1))

print(global_K)

for i in range(elements):
    for row in range(2):
        for column in range(2):
            if row == column:
                global_K[row+i][column+i] += K[i]
            else:
                global_K[row + i][column + i] -= K[i]

print((global_K))

# Nodal displacement matrix

Q = np.array(input("Enter the known nodal displacements in sequence and enter x for unknowns (ex. 120,x,130): ").split(","))
Q = Q.reshape(elements+1, 1)
print(Q)

X = np.where(Q != 'x')
rows = np.unique(X[0]).astype(int)
#columns = np.unique(X[1])
print(X)
print(rows)

# Global force matrix

F = np.array(input("Enter the known forces in sequence (ex. 120,140,130): ").split(","))
F = F.reshape(elements+1, 1).astype(float)
print(F)

for i in rows:
    print("i = " + str(i))
    for f in range(elements+1):
        F[f] -= global_K[f][i]*int(Q[i])

print((F))

global_K = np.delete(global_K, rows, 0)
global_K = np.delete(global_K, rows, 1)

F = np.delete(F, rows, 0)

print("Unknown nodal displacements in sequence: ")

print(np.linalg.solve(global_K,F))