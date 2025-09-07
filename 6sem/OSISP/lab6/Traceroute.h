//
// Created by nikita on 26.06.24.
//

#ifndef OATPP_TEST_TRACEROUTE_H
#define OATPP_TEST_TRACEROUTE_H

#include <iostream>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <cstring>
#include <unistd.h>
#include <chrono>
#include <netinet/ip.h>
#include <netdb.h>
#include <cstdint>



class Traceroute {
public:
    void run(const std::string& host, int max_hops = 32, int timeout = 5,
             int start_ttl = 1, int retries = 3);

    static std::string ip_from_name(const std::string& address);
    static std::string name_from_ip(const std::string& ip);
    static uint16_t internet_checksum(const void* data, size_t len);

private:
    struct icmp_header {
        uint8_t type;
        uint8_t code;
        uint16_t checksum;
        uint16_t identifier;
        uint16_t sequence;
        uint32_t payload;
    };

    int sock;
    pid_t ppid = getppid();
};



#endif //OATPP_TEST_TRACEROUTE_H
