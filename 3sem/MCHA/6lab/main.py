import numpy as np
from conf import test_count
from task import task
def main():
    points = np.genfromtxt("dataset/points.csv")
    for i in range(test_count):
        print("--------------------------------------------")
        print(f"................TEST #{i}................")
        task(i, points[i])

if __name__ == "__main__":
    main()
