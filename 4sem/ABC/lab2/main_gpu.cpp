#define __CL_ENABLE_EXCEPTIONS

#include <iostream>
#include <tuple>
#include <cmath>
#include <fstream>
#include <chrono>
#include <vector>
#include <math.h>
#include <omp.h>
#include <CL/opencl.hpp>
#include <thread>
#include <csignal>
#include <mutex>

#define CL_TARGET_OPENCL_VERSION 300

std::mutex g_lock;
const int threads_num = sysconf(_SC_NPROCESSORS_ONLN);

extern "C" double* calcY(double*);

extern "C" void calcSum(double* S, double* k, double* x);

const char* kernel_source = R"(
    #define M_PI 3.14159265358979323846
    __kernel void test(__global double* result, __global int* counts, double a, double b, double h, double eps)
    {
        int idx = get_global_id(0);
        double i = a + idx * h;
        double y = M_PI * M_PI / 8 - M_PI / 4 * fabs(i);
        double sum = 0;
        int n = 1;

        while (fabs(sum - y) > eps) {
            sum += cos((2 * n - 1) * i) / (2 * i - 1) / (2 * i - 1);
            n++;
        }
        result[idx] = sum;
        counts[idx] = n;
    }
)";

void GPU(double a, double b, double h, double eps, const char* kernel_source, const std::string& str)
{
    int upper_bound = static_cast<int>((b - a) / h) / 100000;

    std::vector<cl::Platform> platforms;
    cl::Platform::get(&platforms);

    cl::Device device;
    for (const auto& platform : platforms)
    {
        std::vector<cl::Device> devices;
        platform.getDevices(CL_DEVICE_TYPE_GPU, &devices);
        if (!devices.empty())
        {
            device = devices.front();
            if (device.getInfo<CL_DEVICE_VERSION>() == "OpenCL 3.0 NEO")
                break;
        }
    }

    cl::Context context(device);
    cl::CommandQueue queue(context, device, CL_QUEUE_PROFILING_ENABLE);

    cl::Program::Sources sources;
    sources.emplace_back(kernel_source);
    cl::Program program(context, sources);

    try
    {
        program.build();
    }
    catch (...)
    {
        std::cout << "Error building program: " << program.getBuildInfo<CL_PROGRAM_BUILD_LOG>(device) << std::endl;
        return;
    }

    cl::Kernel kernel(program, "test");

    std::vector<double> y_values(upper_bound);
    cl::Buffer yBuffer(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, sizeof(double) * (upper_bound + 1),
                       y_values.data());

    std::vector<double> sums(upper_bound);
    cl::Buffer sumBuffer(context, CL_MEM_WRITE_ONLY, sizeof(double) * (upper_bound + 1));

    kernel.setArg(0, sumBuffer);
    kernel.setArg(1, yBuffer);
    kernel.setArg(2, a);
    kernel.setArg(3, b);
    kernel.setArg(4, h);
    kernel.setArg(5, eps);

    std::ofstream fout(str);
    fout << "iters;time" << std::endl;

    for (int k = 0; k < upper_bound; k++)
    {
        auto start_time = std::chrono::high_resolution_clock::now();
        queue.enqueueNDRangeKernel(kernel, cl::NullRange, cl::NDRange(k), cl::NullRange);
        queue.finish();
        auto end_time = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration<double, std::milli>(end_time - start_time).count();
        fout << k << ";" << duration << std::endl;
    }

    queue.enqueueReadBuffer(sumBuffer, CL_TRUE, 0, sizeof(double) * (upper_bound + 1), sums.data());
    queue.enqueueReadBuffer(yBuffer, CL_TRUE, 0, sizeof(int) * (upper_bound + 1), y_values.data());

    fout.close();
}

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
    std::string filename = "HT_high_load";
    if (a <= 0 || b <= 0 || a > 3 || b > 3 || a >= b) {
        return -1;
    }

    auto str = "data/CPU-" + filename + "_GPU_asm_res_lab2.csv";
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
    str = "data/GPU-" + filename + "_GPU_asm_res_lab2.csv";

    GPU(a, b, h, eps, kernel_source, str);
    for (auto &x: vt) {
        x.join();
    }

    std::cout << "SUCCESS";
    return 0;
}
