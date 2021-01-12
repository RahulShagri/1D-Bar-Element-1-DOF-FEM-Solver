# About

The solver assembles the global nodal force vector, global element stiffness matrix, and the global nodal displacement vector and uses the elimination approach on the global relationship after applying all the boundary conditions provided by the user to solve for the unknown displacements.

<b>Note: Only problems with bar elements connected in series and having 1D forces acting parallel to the axis of the bar can be analysed.</b>


# Instructions

Ensure you have the following libraries installed in python to run the solver:
    
1. NumPy 
2. DearPyGUI 
   
Then, run the 1D_Bar_Element_FEM_Solver.py file.


<H3>Example Problem 1</H3>

![Example 1 Diagram](images/Example_1_diag.png)

<H4>Step 1:</H4>
Solving for a uniform bar element that is divided into 3 elements with a force acting in the positive x direction.

Known values are:
1. Number of elements = 3
2. Area of cross section of the bar = 250 mm<sup>2</sup>
3. Modulus of elasticity = 109 GPa
4. Length of the whole bar = 1500 mm
5. Force acting on each node (separated by commas) = 0,0,0,50000


<H4>Step 2:</H4>
Enter the respective values in the text boxes provided. 

<i><b>Note: The user has to make sure the values entered have the correct units. The software does not convert any values entered.</b></i>

<H4>Step 3:</H4>
Hit the solve button.

<H4>Step 4:</H4>
Ensure no errors are shown in the log window.

<H4>Step 5:</H4>
Analyse the results in the results window.

1. Displacement values in the table are respective nodal displacements in the ascending sequence.
2. Stress values in the table are respective element stresses in the ascending sequence.
3. Strain values in the table are respective element strains in the ascending sequence.

<i><b>Note: Results are obtained based on the values that are entered without converting them to different units. In  this example, the displacements are in mm and stresses are in MPa.</b></i>

![Example 1 screenshot](images/Example_1.png)


<H3>Example Problem 2</H3>

![Example 1 Diagram](images/Example_2_diag.png)

<H4>Step 1:</H4>
Solving for multiple bar elements attached in series with two 1D forces acting.

Known values are:

| Element No. | Area of cross section | Young's modulus | Length |
| --- | ----------- | ----------- | ----------- |
| 1 | 140 mm<sup>2</sup> | 109 GPa | 100 mm |
| 2 | 100 mm<sup>2</sup> | 100 GPa | 150 mm |
| 3 | 90 mm<sup>2</sup> | 110 GPa | 300 mm |

| Node No. | Displacement | Force |
| --- | ----------- | ----------- 
| 1 | 0 (Fixed) | 0 N
| 2 | x (Unknown) | - 1000 N
| 3 | x (Unknown) | 0 N
| 4 | x (Unknown) | 15000 N

<H4>Step 2:</H4>
Enter the respective values in the text boxes provided. 

<i><b>Note: The user has to make sure the values entered have the correct units. The software does not convert any values entered.</b></i>

<H4>Step 3:</H4>
Hit the solve button.

<H4>Step 4:</H4>
Ensure no errors are shown in the log window.

<H4>Step 5:</H4>
Analyse the results in the results window.

1. Displacement values in the table are respective nodal displacements in the ascending sequence.
2. Stress values in the table are respective element stresses in the ascending sequence.
3. Strain values in the table are respective element strains in the ascending sequence.

<i><b>Note: Results are obtained based on the values that are entered without converting them to different units. In  this example, the displacements are in mm and stresses are in MPa.</b></i>

![Example 1 screenshot](images/Example_2.png)
