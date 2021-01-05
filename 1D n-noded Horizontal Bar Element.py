import numpy as np
import string

# 1D bar element with area of cross-section, young's modulus, force at multiple nodes, displacement constraints and length of the element given

elements = int(input("\nEnter the total number of elements in series in the system: "))

# Element stiffness matrix

A = np.array(input("Enter area of cross-section of the elements in sequence (ex. 120,140,130): ").split(","))
A = A.astype(float)

E = np.array(input("Enter the young's modulus of the elements in sequence (ex. 120,140,130): ").split(","))
E = E.astype(float)

L = np.array(input("Enter the length of the elements in sequence (ex. 120,140,130): ").split(","))
L = L.astype(float)

K = np.array([])

for a, e, l in zip(A, E, L):
    K = np.append(K, a*e/l)

#Assemblying the global stiffness matrix

global_K = np.zeros((elements+1, elements+1))

for i in range(elements):
    for row in range(2):
        for column in range(2):
            if row == column:
                global_K[row+i][column+i] += K[i]
            else:
                global_K[row + i][column + i] -= K[i]

print("\nThe global stiffness matrix is: ")
print((global_K))

# Nodal displacement matrix

Q = np.array(input("\nEnter the known nodal displacements in sequence and enter x for unknowns (ex. 120,x,130): ").split(","))
Q = Q.reshape(elements+1, 1)

X = np.where(Q != 'x')
rows = np.unique(X[0]).astype(int)

# Global force matrix

F = np.array(input("Enter the known forces in sequence (ex. 120,140,130): ").split(","))
F = F.reshape(elements+1, 1).astype(float)

print("\nThe global force matrix is:")
print((F))

for i in rows:
    for f in range(elements+1):
        F[f] -= global_K[f][i]*float(Q[i])

F = np.delete(F, rows, 0)

print("\nThe global force matrix after elimination is:")
print((F))

global_K = np.delete(global_K, rows, 0)
global_K = np.delete(global_K, rows, 1)

print("\nThe global stiffness matrix after elimination is: ")
print((global_K))

unknown_disp = np.linalg.solve(global_K,F)

i = 0

for row in range(elements+1):
    if row in rows:
        continue
    else:
        Q[row] = str(0)
        i += 1

Q = Q.astype(float)

i = 0

for row in range(elements+1):
    if row in rows:
        continue
    else:
        Q[row] = unknown_disp[i]
        i += 1

print("\n The global nodal displacement matrix with all values is:")
print(Q)

stress = np.array([])

for element in range(elements):
    stress = np.append(stress, E[element]*((Q[element+1]-Q[element])/L[element]))

stress = stress.reshape(elements, 1)

print("\nThe stress matrix is:")
print(stress)
