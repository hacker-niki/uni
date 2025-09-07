#include <iostream>
#include <cmath>
#include <fstream>
#include <chrono>

extern "C" double *calcY(double *);

extern "C" void calcSum(double *S, double *k, double *x);

long long calcAsm(double x, double eps)
{
    double S = 0, Y;
    double x2 = x;
    Y = *calcY(&x2);
    double k = 0;
    while (fabs(S - Y) > eps) {
        k++;
        calcSum(&S, &k, &x);
    }
    return k;
}

void test(double a, double b, double h, double eps, std::string filename) {
    std::ofstream fout(filename);
    fout << "iterations;time" << std::endl;
    if (a > b) std::swap(a, b);
    double x = a;
    while (x < b) {
        long long count;
        auto start = std::chrono::high_resolution_clock::now();
        count = calcAsm(x, eps);
        auto end = std::chrono::high_resolution_clock::now();
        auto time = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start);
        fout << count << ';' << time.count() << std::endl;
        x += h;
    }
    fout.close();
}

int main() {
    double a, b, h, eps;
    std::ifstream fin("input.txt");
    fin >> a >> b >> h >> eps;
    fin.close();
    std::string filename = "HT_high_load";
    if (a <= 0 || b <= 0 || a > 3 || b > 3) {
        return -1;
    }
    for (int i = 0; i < 10; ++i) {
        test(a, b, h, eps, "data/" + filename + std::to_string(i) + "_asm_res.csv");
    }
    std::cout << "SUCCESS";
}

