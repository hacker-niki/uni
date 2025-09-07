#include <iostream>
#include <chrono>
#include <fstream>
#include <valarray>
#include <random>
#include <algorithm>

using namespace std;
using namespace std::chrono;

int diff_count = 0;

int binarySearch(int arr[], int left, int right, int target) {
    while (left <= right) {
        int mid = left + (right - left) / 2;

        if (arr[mid] == target) {
//            diff_count++;
            return mid;
        }
        diff_count++; // Uncomment if diff_count is defined and needed

        if (arr[mid] < target) {
//            diff_count++;
            left = mid + 1;
        } else {
//            diff_count++;
            right = mid - 1;
        }
    }

    return -1; // If the target element is not found
}

int ternarySearch(int arr[], int left, int right, int target) {
    if (right >= left) {
        int mid1 = left + (right - left) / 3;
        int mid2 = right - (right - left) / 3;

        if (arr[mid1] == target) {
//            diff_count++;
            return mid1;
        }
        if (arr[mid2] == target) {
//            diff_count++;
            return mid2;
        }
        diff_count++; // Uncomment if diff_count is defined and needed

        if (target < arr[mid1]) {
//            diff_count++;
            return ternarySearch(arr, left, mid1 - 1, target);
        } else if (target > arr[mid2]) {
//            diff_count++;
            return ternarySearch(arr, mid2 + 1, right, target);
        } else {
//            diff_count++;
            return ternarySearch(arr, mid1 + 1, mid2 - 1, target);
        }
    }

    return -1; // If the target element is not found
}

int goldenSectionSearch(int arr[], int left, int right, int target) {
    double phi = (1 + sqrt(5)) / 2;
    int mid1, mid2;

    while (left <= right) {
        mid1 = right - (right - left) / phi;
        mid2 = left + (right - left) / phi;

        if (arr[mid1] == target) {
//            diff_count++; // Uncomment if diff_count is defined and needed
            return mid1;
        }
        if (arr[mid2] == target) {
//            diff_count++; // Uncomment if diff_count is defined and needed
            return mid2;
        }

        diff_count++; // Uncomment if diff_count is defined and needed
        if (target < arr[mid1]) {
            right = mid1 - 1;
        } else if (target > arr[mid2]) {
//            diff_count++; // Uncomment if diff_count is defined and needed
            left = mid2 + 1;
        } else {
//            diff_count++; // Uncomment if diff_count is defined and needed
            left = mid1 + 1;
            right = mid2 - 1;
        }
    }

    return -1; // If the target element is not found
}

int *generateRandomArray(int n) {
    std::random_device rd;
    std::mt19937 mt(rd());
    std::uniform_int_distribution<int> distribution(0, n);
    int *arr = new int[n];

    for (int i = 0; i < n; i++) {
        arr[i] = distribution(mt);
    }

    sort(arr, arr + n);

    return arr;
}

const int mini = 10;
const int maxi = 100'000'000;
const int l_step = 1'00;
const int m_step = 3'000;
const int h_step = 30'000;
const int mid_cnt = 100000;

void test(int (*fun)(int[], int, int, int), std::ofstream *fout, int n) {
    int mid = 0;
    std::random_device rd;
    std::mt19937 mt(rd());
    std::uniform_int_distribution<int> distribution(0, n - 1);
    for (int i = 0; i < mid_cnt; ++i) {
        int *arr = generateRandomArray(n);
        auto start = high_resolution_clock::now();
        fun(arr, 0, n, arr[distribution(mt)]);
        auto stop = high_resolution_clock::now();
        auto duration = duration_cast<nanoseconds>(stop - start);
        *fout << duration.count() << ';' << n << std::endl;
        mid += duration.count();
        delete[] arr;
    }
    mid /= mid_cnt;
    *fout << mid << ';' << n << std::endl;
    std::cout << mid << ';' << n << std::endl;
}

void count_test(int (*fun)(int[], int, int, int), std::ofstream *fout, int n) {
    int mid = 0;
    int *arr = generateRandomArray(n);
    std::random_device rd;
    std::mt19937 mt(rd());
    std::uniform_int_distribution<int> distribution(0, n - 1);
    for (int i = 0; i < mid_cnt; ++i) {
        int r = distribution(mt);
        diff_count = 0;
        fun(arr, 0, n, arr[r]);
        mid += diff_count;
    }
    delete[] arr;
    mid /= mid_cnt;
    *fout << mid << ';' << n << std::endl;
    std::cout/* << mid << ';'*/ << n << std::endl;
}

void run_tests() {
    std::ofstream binary_out("binary_search_results_not_mid.csv");
    std::ofstream ternary_out("ternary_search_results_not_mid.csv");
    std::ofstream golden_out("golden_section_search_results_not_mid.csv");

    if (!binary_out.is_open() || !ternary_out.is_open() || !golden_out.is_open()) {
        std::cerr << "Error opening output files!" << std::endl;
        return;
    }

    binary_out << "cnt;n" << std::endl;
    ternary_out << "cnt;n" << std::endl;
    golden_out << "cnt;n" << std::endl;


    for (int n = mini; n <= maxi; n += (n < 1000 ? l_step : (n < 100000 ? m_step : h_step))) {
        count_test(binarySearch, &binary_out, n);
        count_test(ternarySearch, &ternary_out, n);
        count_test(goldenSectionSearch, &golden_out, n);
    }

    binary_out.close();
    ternary_out.close();
    golden_out.close();
}

int main() {
    run_tests();
    return 0;
}