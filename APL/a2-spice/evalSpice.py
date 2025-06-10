import numpy as np
from numpy.linalg import solve
import os

def evalSpice(filename):
    #filename = './custom_testdata/' + filename
    if os.path.exists(filename):
        #parsing the circuit
        def parse_circuit_file(file_path):
            with open(file_path, 'r') as file:
                lines = file.readlines()

            circuit_lines = []
            in_circuit = False

            for line in lines:
                line = line.split('#')[0].strip()

                if '.circuit' in line:
                    in_circuit = True
                    continue
                elif '.end' in line:
                    in_circuit = False
                    break

                if in_circuit and line:
                    circuit_lines.append(line)
            else:
                #no content then raise error
                raise ValueError('Malformed circuit file')

            if in_circuit == True:
                #no .end then raise error
                raise ValueError('Malformed circuit file')
            return circuit_lines
    else:
        #raise error if file not found
        raise FileNotFoundError('Please give the name of a valid SPICE file as input')
    
    lines = parse_circuit_file(filename)

    dct = {}
    def is_convertible_to_float(s):
        try:
            # Try to convert the string to a float
            np.float64(s)
            return True
        except ValueError:
            # If conversion fails, return False
            return False
        
    for line in lines:
        dum_l = line.split()
        #checks if the values have been given and if they are proper (like float-convertible and not alpha-type strings)
        if not ((is_convertible_to_float(dum_l[-1]))and (dum_l[1][-1].isdigit() or dum_l[1] == 'GND') and (dum_l[2][-1].isdigit() or dum_l[2] == 'GND')):
            raise ValueError('Circuit error: no solution')
        #takes in the component as the key, the value as the quantity and position of the nodes
        dct[dum_l[0]] = [np.float64(dum_l[-1]), [dum_l[1], dum_l[2]]]

    for k, v in dct.items():
        #checks if only voltage, current sources and resistors are there
        if k[0].upper() not in ['V', 'R', 'I']:
            raise ValueError('Only V, I, R elements are permitted')
    
    #get the total nodes along with the gnd -> determines the shape of matrices
    node_set = sorted(list(set([i[1][0] for i in dct.values()] + [i[1][1] for i in dct.values()])))
    voltage_nodes = []  #gets set of voltage nodes
    voltage_nodes_with_pos = {} #maps voltages with the nodes (or positions)

    def matrix_generation(dt):
        stat = set([True for k in dt.keys() if k[0].upper() == 'I'])
        stat = len(stat) == 0   #checks if there are any current sources

        #uses to get the sizes of the matrices
        length = len(set([i[1][0] for i in dt.values()] + [i[1][1] for i in dt.values()])) - 1

        #initialize the matrices
        init_matrix_A = np.zeros((length, length))
        init_matrix_B = np.zeros((length, 1))

        #keep track of voltage and current sources
        voltage_src_count = 0
        current_src_count = 0
        
        #if there is no current source
        if stat:
            #keeps track of polarity
            old_volt_node_positive = ''
            is_negative = False
            #convert to int/float which can be used for indexing
            for k, v in dt.items():
                if v[1][1] == 'GND':
                    v[1][1] = '0'    
                elif v[1][0] == 'GND':
                    v[1][0] = '0'
                v[1][1] = v[1][1][-1]
                v[1][0] = v[1][0][-1]
                
                if 'V' == k[0].upper():   
                    #raises error if voltage sources are connected in a loop 
                    if voltage_src_count >= length:
                        raise ValueError('Circuit error: no solution') 
                    voltage_nodes.append(k)
                    voltage_nodes_with_pos[k] = v[1]   
                    #if the source is the first source (need not take into account the polarity)               
                    if voltage_src_count < 1:
                        #set the positive polarity direction
                        old_volt_node_positive = v[1][0]
                        if old_volt_node_positive == '0':
                            is_negative = True
                        #update the matrices
                        init_matrix_B[voltage_src_count, :] = v[0]
                        init_matrix_A[voltage_src_count, voltage_src_count] = 1
                    else:
                        #if the voltage source is not the first then take account its polarity wrt to the positive direction
                        #and update the matrices accordingly
                        if old_volt_node_positive == v[1][1]:
                            init_matrix_B[voltage_src_count, :] = v[0]
                            old_volt_node_positive = v[1][1]
                        else:
                            init_matrix_B[voltage_src_count, :] = - v[0]
                            old_volt_node_positive = v[1][0]
                        init_matrix_A[voltage_src_count, voltage_src_count] = 1
                        #if there are other sources in the same branch, then need to take into account the potential difference
                        #rather than the absolute potential of the source
                        #and update the matrix A suitably
                        ref_node = int(v[1][0]) if int(v[1][1]) == voltage_src_count + 1 else int(v[1][1])
                        init_matrix_A[voltage_src_count , ref_node - 1] = -1
                    #increment the voltage_source count
                    voltage_src_count += 1

                if 'R' == k[0].upper():
                    #update the off-diagonal elements
                    if int(v[1][0]) - 1 > voltage_src_count - 1:
                        init_matrix_A[int(v[1][0]) - 1, int(v[1][0]) - 1] += 1/v[0]
                    if int(v[1][1]) - 1 > voltage_src_count - 1:
                        init_matrix_A[int(v[1][1]) - 1, int(v[1][1]) - 1] += 1/v[0]
                    if int(v[1][0]) - 1 >= voltage_src_count - 1 and int(v[1][1]) - 1 > voltage_src_count - 1:
                        init_matrix_A[int(v[1][1]) - 1, int(v[1][0]) - 1] -= (1/v[0])
                    if int(v[1][0]) - 1 > voltage_src_count - 1 and int(v[1][1]) - 1 >= voltage_src_count - 1:
                        init_matrix_A[int(v[1][0]) - 1, int(v[1][1]) - 1] -= (1/v[0])
        else:
            ##if there is current source
            #keeps track of polarity
            old_volt_node_positive = ''
            is_negative = False
            #convert to int/float which can be used for indexing
            for k, v in dt.items():
                if v[1][1] == 'GND':
                    v[1][1] = '0'    
                elif v[1][0] == 'GND':
                    v[1][0] = '0'
                v[1][1] = v[1][1][-1]
                v[1][0] = v[1][0][-1]

                if 'V' == k[0].upper(): 
                    #raises error if voltage sources are connected in a loop 
                    if voltage_src_count >= length:
                        raise ValueError('Circuit error: no solution') 
                    voltage_nodes.append(k)
                    voltage_nodes_with_pos[k] = v[1]
                    #if the source is the first source (need not take into account the polarity) 
                    if voltage_src_count < 1:
                        #set the positive polarity direction
                        old_volt_node_positive = v[1][0]
                        if old_volt_node_positive == '0':
                            is_negative = True
                        #update the matrices
                        init_matrix_B[voltage_src_count, :] = v[0]
                        init_matrix_A[voltage_src_count, voltage_src_count] = 1
                    else:
                        #if the voltage source is not the first then take account its polarity wrt to the positive direction
                        #and update the matrices accordingly
                        if old_volt_node_positive == v[1][1]:
                            init_matrix_B[voltage_src_count, :] = v[0]
                            old_volt_node_positive = v[1][1]
                        else:
                            init_matrix_B[voltage_src_count, :] =  -v[0]
                            old_volt_node_positive = v[1][0]
                        init_matrix_A[voltage_src_count, voltage_src_count] = 1
                        #if there are other sources in the same branch, then need to take into account the potential difference
                        #rather than the absolute potential of the source
                        #and update the matrix A suitably
                        ref_node = int(v[1][0]) if int(v[1][1]) == voltage_src_count + 1 else int(v[1][1])
                        init_matrix_A[voltage_src_count , ref_node - 1] = -1
                    #increment the voltage source
                    voltage_src_count += 1
                        
                #update the B matrix accordingly by adding or subtracting from the B matrix value for that branch
                if 'I' == k[0].upper():
                    current_src_count += 1
                    init_matrix_B[length - current_src_count, :] = -v[0] if int(v[1][0]) > int(v[1][1]) else v[0]

                #update the off-diagonal elements
                if 'R' == k[0].upper():
                    if int(v[1][0]) - 1 > voltage_src_count - 1:
                        init_matrix_A[int(v[1][0]) - 1, int(v[1][0]) - 1] += 1/v[0]
                    if int(v[1][1]) - 1 > voltage_src_count - 1:
                        init_matrix_A[int(v[1][1]) - 1, int(v[1][1]) - 1] += 1/v[0]
                    if int(v[1][0]) - 1 >= voltage_src_count - 1 and int(v[1][1]) - 1 > voltage_src_count - 1:
                        init_matrix_A[int(v[1][1]) - 1, int(v[1][0]) - 1] -= (1/v[0])
                    if int(v[1][0]) - 1 > voltage_src_count - 1 and int(v[1][1]) - 1 >= voltage_src_count - 1:
                        init_matrix_A[int(v[1][0]) - 1, int(v[1][1]) - 1] -= (1/v[0])

        #return matrix A, B required for solving and relative polarity of the nodal voltages         
        return init_matrix_A, init_matrix_B, is_negative


    matA, matB , is_negative = matrix_generation(dct)

    #initializing the voltage currents
    voltage_current = {i:0 for i in voltage_nodes}

    if np.array_equal(matB, np.zeros_like(matB)):
        #raises error if there are no independent sources
        raise ValueError('Circuit error: no solution')
    
    if np.array_equal(matA, np.zeros_like(matA)):
        #raises error if there are no resistors, no voltage sources
        raise ValueError('Circuit error: no solution')
    
    #solving the equations
    solution = solve(matA, matB)

    #get all the nodal volatages incl. ground
    sol_arr = np.array(solution).squeeze(1)
    sol_arr = np.append(sol_arr, np.array([0.0]))
    #dictionary to store all the current through the voltage sources
    curr = {}

    #calculates the current flowing through each resistor (and therefore through that branch)
    for k, v in dct.items():
        v[1][1] = v[1][1][-1]
        v[1][0] = v[1][0][-1]
        if 'R' == k[0].upper():
            i, j = int(v[1][0]) - 1, int(v[1][1]) - 1
            curr[tuple(v[1])] = (sol_arr[i] - sol_arr[j])/v[0]
            dct[k] = v

    #assign the currents for the voltage sources depending on the branch
    for k1, v1 in voltage_nodes_with_pos.items():
        for k2, v2 in curr.items():
            if k2[0] == v1[0] and k2[1] == v1[1]:
                voltage_current[k1] -= np.abs(v2)
            elif (v1[0] == k2[1] or v1[0] == k2[0]) and v1[0] != '0':
                voltage_current[k1] -= np.abs(v2)
            elif (v1[1] == k2[0] or v1[1] == k2[1]) and v1[1] != '0':
                voltage_current[k1] -= np.abs(v2)

    #setting up the reference (as it is wrt the first voltage source's polarity)
    k0, v0 = list(voltage_current.items())[0]
    #updating the currents through the voltage sources using kcl as well as direction
    if v0 == 0:
        l1 = list(voltage_nodes_with_pos.keys())
        l2 = list(voltage_current.values())
        voltage_current[k0] = -sum(l2) if matB[int(k0[-1]) - 1, :]*matB[int(k0[-1]), :] < 0 else sum(l2)
        if voltage_current[k0] > 0:
            for k, v in voltage_current.items():
                voltage_current[k] = -v

    #polarity of nodal voltages
    solution_final = -solution.squeeze(1) if is_negative else solution.squeeze(1)

    #loading the result (nodal voltages) into dictionary
    if node_set[-1] == 'GND':
        result = {str(i+1): solution_final.tolist()[i] for i in range(solution.shape[0])}
    else:
        result = {node_set[i + 1]: solution_final.tolist()[i] for i in range(solution.shape[0])}

    #adding the ground node
    result['GND'] = np.float64(0)

    #returning the dictionaries
    return (result, voltage_current)