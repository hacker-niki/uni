#include <iostream>
#include <string>
#include <getopt.h>
#include "Traceroute.h"

#define no_argument            0
#define required_argument      1

void print_help(const char *program_name) {
    std::cout << "Usage: " << program_name << " <hostname> [options]\n"
              << "Options:\n"
              << "  -h, --help           Show this help message and exit\n"
              << "  -m, --max-hops N     Set the max number of hops (default: 30)\n"
              << "  -t, --timeout N      Set the timeout in seconds (default: 1)\n"
              << "  -f, --start-ttl N    Set the initial TTL value (default: 1)\n"
              << "  -r, --retries N      Set the retries count (default: 1)" << std::endl;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        print_help(argv[0]);
        return 1;
    }

    int max_hops = 30;
    int timeout = 1;
    int start_ttl = 1;
    int retries = 1;

    int option_index = 0;
    int c;

    const char *short_options = "hm:t:f:r:";

    const option long_options[] = {
            {"help",      no_argument,       nullptr, 'h'},
            {"max-hops",  required_argument, nullptr, 'm'},
            {"timeout",   required_argument, nullptr, 't'},
            {"start-ttl", required_argument, nullptr, 'f'},
            {"retries",   required_argument, nullptr, 'r'},
            {nullptr, 0,                     nullptr, 0}
    };

    while ((c = getopt_long(argc, argv, short_options, long_options, &option_index)) != -1) {
        try {
            switch (c) {
                case 'h':
                    print_help(argv[0]);
                    return 0;
                case 'm':
                    max_hops = std::stoi(optarg);
                    if (max_hops <= 0) {
                        std::cout << "\033[1;31mError: number of hops must be greater than 0\033[0m\n";
                        return 1;
                    }
                    break;
                case 't':
                    timeout = std::stoi(optarg);
                    if (timeout <= 0) {
                        std::cout << "\033[1;31mError: the timeout must be greater than 0\033[0m\n";
                        return 1;
                    }
                    break;
                case 'f':
                    start_ttl = std::stoi(optarg);
                    if (start_ttl <= 0) {
                        std::cout << "\033[1;31mError: time to live must be greater than 0\033[0m\n";
                        return 1;
                    }
                    break;
                case 'r':
                    retries = std::stoi(optarg);
                    if (retries <= 0) {
                        std::cout << "\033[1;31mError: number of retries must be greater than 0\033[0m\n";
                        return 1;
                    }
                    break;
                default:
                    print_help(argv[0]);
                    return 1;
            }
        } catch (...) {
            std::cout << "\033[1;31mInvalid argument\033[0m\n";
            print_help(argv[0]);
            return 1;
        }
    }

    if (optind >= argc) {
        std::cout << "\033[1;31mError: hostname or ip is required\033[0m\n";
        print_help(argv[0]);
        return 1;
    }

    std::string destination_address = argv[optind];

    Traceroute traceroute;
    traceroute.run(destination_address, max_hops, timeout, start_ttl, retries);

    return 0;
}