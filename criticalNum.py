import numpy as np

def find_critical_numbers(arr):
    
    ##Returns a NumPy array containing the critical numbers of the input array.
    critical_numbers = np.array([], dtype=int)
    
    for i in range(1, len(arr)-1):
        if (arr[i] < arr[i-1]) and (arr[i] < arr[i+1]):
            critical_numbers = np.append(critical_numbers, i)
        elif (arr[i] > arr[i-1]) and (arr[i] > arr[i+1]):
            critical_numbers = np.append(critical_numbers, i)
            
    return critical_numbers
