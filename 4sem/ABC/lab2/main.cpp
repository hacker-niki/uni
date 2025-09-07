#include <iostream>
#include <cmath>
#include <fstream>
#include <chrono>
#include <thread>
#include <mutex>
#include <vector>
#include <csignal>

std::mutex g_lock;
const int threads_num = sysconf(_SC_NPROCESSORS_ONLN);

extern "C" double *calcY(double *);

extern "C" void calcSum(double *S, double *k, double *x);

long long calcAsm(double x, double eps) {
    double S = 0, Y;
    double x2 = x;
    Y = *calcY(&x2);
    double k = 0;
    while (fabs(S - Y) > eps && k < 1000) {
        k++;
        calcSum(&S, &k, &x);
    }
    return k;
}

void test(double a, double b, double h, double eps, std::string filename) {

    if (a > b) std::swap(a, b);
    double x = a;
    std::ofstream fout(filename, std::ios::app | std::ios::out);
    while (x < b) {
        long long count;
        auto start = std::chrono::high_resolution_clock::now();
        count = calcAsm(x, eps);
        auto end = std::chrono::high_resolution_clock::now();
        auto time = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start);
        g_lock.lock();
        fout << count << ';' << time.count() << std::endl << std::flush;
        g_lock.unlock();
        x += h;
    }
    fout.close();
}

int main() {
    double a, b, h, eps;
    std::ifstream fin("input.txt", std::ios::in);
    fin >> a >> b >> h >> eps;
    fin.close();
    std::string filename = "NO_HT_high_load";
    if (a <= 0 || b <= 0 || a > 3 || b > 3 || a >= b) {
        return -1;
    }

    for (int i = 0; i < 10; ++i) {
        auto str = "data/" + filename + std::to_string(i) + "_NO_GPU_asm_res.csv";
        std::ofstream fout(str);
        fout << "iterations;time" << std::endl << std::flush;
        fout.close();
        std::vector<std::thread> vt;
        double x = a;
        for (int cnt = 0; cnt < threads_num; ++cnt) {
            vt.emplace_back(test, x, x + (b - a) / threads_num, h, eps, str);
            std::cerr << "Thread " << vt.size() << " started\n";
            x += (b - a) / threads_num;
        }
        for (auto &x: vt) {
            x.join();
        }
    }
    std::cout << "SUCCESS";
}