#include <iostream>
#include <chrono>
#include <fstream>
#include <random>
#include <cmath>
#include <functional>

using namespace std;
using namespace std::chrono;

int diff_count = 0;

double exampleFunction1(double x) {
    return pow(x - 2, 2); // Minimum at x = 2
}

double exampleFunction2(double x) {
    return pow(x, 4) - 4 * pow(x, 3) + 4 * x * x; // Minimum at x = 1
}

double exampleFunction3(double x) {
    return sin(x) + 0.1 * pow(x, 2); // Minimum around x = 0
}

double exampleFunction4(double x) {
    return -cos(x); // Minimum at x = π
}


double binarySearch(function<double(double)> func, double left, double right, double epsilon) {
    while (right - left > epsilon) {
        double mid = left + (right - left) / 2;
        double mid1 = mid - epsilon;
        double mid2 = mid + epsilon;

        if (func(mid1) < func(mid2)) {
            right = mid;
        } else {
            left = mid;
        }
        diff_count++;
    }
    return (left + right) / 2;
}

double ternarySearch(function<double(double)> func, double left, double right, double epsilon) {
    while (right - left > epsilon) {
        double mid1 = left + (right - left) / 3;
        double mid2 = right - (right - left) / 3;

        if (func(mid1) < func(mid2)) {
            right = mid2;
        } else {
            left = mid1;
        }
        diff_count++;
    }
    return (left + right) / 2;
}

double goldenSectionSearch(std::function<double(double)> func, double left, double right, double epsilon) {
    const double phi = (1 + std::sqrt(5)) / 2;
    const double resphi = 2 - phi;

    double mid1 = left + resphi * (right - left);
    double mid2 = right - resphi * (right - left);

    double f1 = func(mid1);
    double f2 = func(mid2);

    while (std::abs(right - left) > epsilon) {
        if (f1 < f2) {
            right = mid2;
            mid2 = mid1;
            f2 = f1;
            mid1 = left + resphi * (right - left);
            f1 = func(mid1);
        } else {
            left = mid1;
            mid1 = mid2;
            f1 = f2;
            mid2 = right - resphi * (right - left);
            f2 = func(mid2);
        }
        diff_count++;

    }

    return (left + right) / 2;
}

const int mid_cnt = 100;

void count_test(function<double(function<double(double)>, double, double, double)> search_func,
                ofstream *fout, function<double(double)> func, double left, double right, double epsilon) {
    int total_diff_count = 0;

    for (int i = 0; i < mid_cnt; ++i) {
        diff_count = 0;
        search_func(func, left, right, epsilon);
        total_diff_count += diff_count;
    }

    int average_diff_count = total_diff_count / mid_cnt;
    *fout << average_diff_count << endl;
    cout << average_diff_count << endl;
}

void run_tests(std::string about) {
    std::ofstream binary_out("binary_search_results" + about + ".csv");
    std::ofstream ternary_out("ternary_search_results" + about + ".csv");
    std::ofstream golden_out("golden_section_search_results" + about + ".csv");

    if (!binary_out.is_open() || !ternary_out.is_open() || !golden_out.is_open()) {
        std::cerr << "Error opening output files!" << std::endl;
        return;
    }

    binary_out << "cnt;n" << std::endl;
    ternary_out << "cnt;n" << std::endl;
    golden_out << "cnt;n" << std::endl;

    vector<function<double(double)>> functions = {
            exampleFunction1,
            exampleFunction2,
            exampleFunction3,
            exampleFunction4 // Adding the new function
    };

    vector<pair<double, double>> bounds = {
            {0,   4},  // Bounds for exampleFunction1
            {-1,  2}, // Bounds for exampleFunction2
            {-10, 10}, // Bounds for exampleFunction3
            {0,   2 * M_PI} // Bounds for exampleFunction4
    };

    double epsilon = 1e-5;

    for (int i = 0; i < functions.size(); i++) {

        double left = bounds[i].first;
        double right = bounds[i].second;

        count_test(binarySearch, &binary_out, functions[i], left, right, epsilon);
        count_test(ternarySearch, &ternary_out, functions[i], left, right, epsilon);
        count_test(goldenSectionSearch, &golden_out, functions[i], left, right, epsilon);
        std::cout << std::endl;
    }

//    count_test(binarySearch, &binary_out, exampleFunction3, left, right, epsilon);
//    count_test(ternarySearch, &ternary_out, exampleFunction3, left, right, epsilon);
//    count_test(goldenSectionSearch, &golden_out, exampleFunction3, left, right, epsilon);

    binary_out.close();
    ternary_out.close();
    golden_out.close();
}

int main() {
    run_tests("functional_2");
    return 0;
}