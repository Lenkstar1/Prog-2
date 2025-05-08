""" MA3.py

Student:
Mail:
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc

def approximate_pi(n): # Ex1
    #n is the number of points
    # Write your code here
    points = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(n)]
    x_in, y_in = [], []
    x_out, y_out = [], []
    for point in points:
        x, y = point
        if (x**2 + y**2) <= 1:
            x_in.append(x)
            y_in.append(y)
        else:
            x_out.append(x)
            y_out.append(y)

    pi = 4 *(len(x_in)/n)
    
    plt.scatter(x_in, y_in, marker = "o", color = "red")
    plt.scatter(x_out, y_out, marker = "o", color = "blue")
    plt.savefig(f"Prog-2\MA3 VT25 Files-1\MA3 VT25 Files\Pi approximation with {n} points")

    print(n, pi)
    return pi


def sphere_volume(n, d): #Ex2, approximation
    #n is the number of points
    # d is the number of dimensions of the sphere 
    points = [[random.uniform(-1, 1) for _ in range (d)] for _ in range (n)]
    points_in = list(filter(lambda point: sum(x**2 for x in point) <= 1, points))
    volume = 2**d*(len(points_in)/n)
    return volume

def hypersphere_exact(d): #Ex2, real value
    # d is the number of dimensions of the sphere 
    volume = (m.pi**(d/2))/m.gamma(d/2+1)
    return volume


#Ex3: parallel code - parallelize for loop
def sphere_volume_parallel1(n,d,np=10):
    #n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes
    n_lst = [n for _ in range(np)] 
    d_lst = [d for _ in range(np)] 
    with future.ProcessPoolExecutor() as ex:
        results = list(ex.map(sphere_volume, n_lst, d_lst))
    return mean(results)


#Ex4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel2(n,d,np=10):
    #n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes
    n_part = n//np
    with future.ProcessPoolExecutor() as ex:
        futures = [ex.submit(sphere_volume, n_part, d) for _ in range(np)]
        results = [f.result() for f in futures]      
    return mean(results)

    
def main():
    #Ex1
    dots = [1000, 10000, 100000]
    for n in dots:
        approximate_pi(n)
    #Ex2
    n = 100000
    d = 2
    sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)}")

    n = 100000
    d = 11
    sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)}")

    #Ex3
    sequential_ex3 = []
    n = 100000
    d = 11
    start = pc()
    for y in range (10):
        result = sphere_volume(n,d)
        sequential_ex3.append(result)
    stop = pc()
    print(f"Ex3: Sequential time of {d} and {n}: {stop-start}")
    print(f"Avg volume sequential: {mean(sequential_ex3)}")
    #print("What is parallel time?")

    start = pc()
    parallel_ex3 = sphere_volume_parallel1(n, d, 10)
    stop = pc()
    print(f"Parallel time of {d} and {n}: {stop-start}")
    print(f"Avg volume parallel: {parallel_ex3}")

    #Ex4
    n = 1000000
    d = 11
    start = pc()
    sphere_volume(n,d)
    stop = pc()
    print(f"Ex4: Sequential time of {d} and {n}: {stop-start}")
    #print("What is parallel time?")
    
    start = pc()
    parallel_ex4 = sphere_volume_parallel2(n, d, 10)
    stop = pc()
    print(f"Parallel time of {d} and {n}: {stop-start}")
    print(f"Avg volume parallel: {parallel_ex4}")


if __name__ == '__main__':
	main()
"""
Output from running on Linux machines:
leha9404@atterbom:~/Prog-2/MA3 VT25 Files-1/MA3 VT25 Files$ python MA3.py
Matplotlib is building the font cache; this may take a moment.
1000 3.152
10000 3.1344
100000 3.14076
Actual volume of 2 dimentional sphere = 3.141592653589793
Actual volume of 11 dimentional sphere = 1.8841038793898994
Ex3: Sequential time of 11 and 100000: 9.00072452519089
Avg volume sequential: 1.923072
Parallel time of 11 and 100000: 1.7028564400970936
Avg volume parallel: 1.83296
Ex4: Sequential time of 11 and 1000000: 9.680949669331312
Parallel time of 11 and 1000000: 1.679851015098393
Avg volume parallel: 1.875968

"""