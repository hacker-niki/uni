#include <iostream>
#include <fstream>
#include <chrono>
#include <vector>
#include <cmath>
#include <CL/cl2.hpp>

const char *kernel_source = R"(
    #define M_PI 3.14159265358979323846
    __kernel void test(__global double* result, __global int* counts, double a, double b, double h, double eps)
    {
        int idx = get_global_id(0);
        double i = a + idx * h;
        double y = M_PI*M_PI/8-M_PI/4*fabs(i);
        double sum = 0;
        int n = 1;

        while(fabs(sum - y) > eps) {
            sum += cos((2*n -1)*i)/(2*i-1)/(2*i-1);
            n++;
        }
        result[idx] = sum;
        counts[idx] = n;
    }
)";

void GPU(double a, double b, double h, double eps, const char *kernel_source, const std::string &str) {
    int upper_bound = static_cast<int>((b - a) / h) / 100000;

    std::vector<cl::Platform> platforms;
    cl::Platform::get(&platforms);

    cl::Device device;
    for (const auto &platform: platforms) {
        std::vector<cl::Device> devices;
        platform.getDevices(CL_DEVICE_TYPE_GPU, &devices);
        if (!devices.empty()) {
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

    try {
        program.build();
    } catch (...) {
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

    for (int k = 0; k < upper_bound; k++) {
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

int main() {
    double a, b, h, eps;
    std::ifstream fin("input.txt", std::ios::in);
    fin >> a >> b >> h >> eps;
    fin.close();
    std::string filename = "";
    if (a <= 0 || b <= 0 || a > 3 || b > 3 || a >= b) {
        return -1;
    }

    auto str = "data/" + filename + "ONLY_GPU_asm_res_lab2.csv";
    GPU(a, b, h, eps, kernel_source, str);

    std::cout << "SUCCESS";
    return 0;
}