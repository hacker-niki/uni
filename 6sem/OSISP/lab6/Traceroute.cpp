//
// Created by nikita on 26.06.24.
//

#include "Traceroute.h"

std::string Traceroute::ip_from_name(const std::string& address)
{
    addrinfo address_of_service_provider = {};
    address_of_service_provider.ai_flags = AI_CANONNAME;
    address_of_service_provider.ai_family = AF_UNSPEC;
    address_of_service_provider.ai_socktype = SOCK_RAW;
    address_of_service_provider.ai_protocol = IPPROTO_ICMP;

    struct hostent* he = gethostbyname(address.c_str());
    if (he == nullptr)
    {
        return {};
    }

    char* ip = new char[1024];
    strcpy(ip, inet_ntoa(*(struct in_addr*)he->h_addr));
    return ip;
}

std::string Traceroute::name_from_ip(const std::string& ip)
{
    struct in_addr ipaddr{};

    if (inet_pton(AF_INET, ip.c_str(), &ipaddr) != 1)
    {
        return {};
    }

    struct hostent* he = gethostbyaddr(&ipaddr, sizeof(ipaddr), AF_INET);

    if (he == nullptr)
    {
        return {};
    }

    char* hostname = new char[strlen(he->h_name) + 1];
    strcpy(hostname, he->h_name);
    return hostname;
}


void Traceroute::run(const std::string& host, int max_hops, int timeout, int start_ttl, int retries)
{
    std::string ip = Traceroute::ip_from_name(host);
    if (ip == "")
    {
        std::cout << "\033[1;31mHost error\033[0m\n";
        exit(1);
    }

    std::cout << "Traceroute to " << "\033[1;33m" << ip << "\033[0m" << std::endl;
    std::cout << "Max hops: " << "\033[1;33m" << max_hops << "\033[0m" << std::endl << std::endl;

    struct sockaddr_in socket_address{};

    socket_address.sin_family = AF_INET;
    socket_address.sin_addr.s_addr = inet_addr(ip.c_str());
    sock = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);

    if (sock < 0)
    {
        std::cout << "\033[1;31mSocket error\033[0m\n";
        return;
    }

    struct icmp_header icmp_packet{};

    for (int i = start_ttl, j = 0; j < max_hops; i++, j++)
    {
        std::cout << i;
        for (int k = 0; k < retries; k++)
        {
            icmp_packet.type = 8;
            icmp_packet.code = 0;
            icmp_packet.checksum = 0;
            icmp_packet.identifier = ppid;
            icmp_packet.sequence = j;
            icmp_packet.checksum = internet_checksum(&icmp_packet, sizeof(icmp_packet));

            int ttl = i;

            setsockopt(sock, IPPROTO_IP, IP_TTL, &ttl, sizeof(ttl));

            auto send_flag = sendto(sock, &icmp_packet, sizeof(icmp_packet), 0, (struct sockaddr*)&socket_address,
                                    socklen_t(sizeof(socket_address)));

            if (send_flag < 0)
            {
                std::cout << "\033[1;31mSend error\033[0m\n";
                return;
            }

            struct iphdr ip_response_header{};

            struct timeval tv{};
            tv.tv_sec = timeout;
            tv.tv_usec = 0;

            setsockopt(sock, SOL_SOCKET, SO_SNDTIMEO, &tv, sizeof(tv));
            setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));

            auto start = std::chrono::high_resolution_clock::now();

            auto data_length_byte = recv(sock, &ip_response_header, sizeof(ip_response_header), 0);

            auto end = std::chrono::high_resolution_clock::now();
            auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);

            if (data_length_byte == -1)
            {
                std::cout << "\033[1;35m" << " * * *" << "\033[0m";
                continue;
            }

            struct sockaddr_in src_addr{};
            src_addr.sin_addr.s_addr = ip_response_header.saddr;

            std::cout << " " << name_from_ip(inet_ntoa(src_addr.sin_addr)) << " " << "\033[1;35m"
                << inet_ntoa(src_addr.sin_addr) << "\033[0m " << duration.count() << "ms";

            if (strcmp(inet_ntoa(src_addr.sin_addr), ip.c_str()) == 0)
            {
                std::cout << std::endl << std::endl << std::endl << "\033[1;35m" << ttl << "\033[0m"
                    << " hops between you and " << ip << " "
                    << duration.count() << "ms" << std::endl;
                return;
            }
        }
        std::cout << std::endl;
    }
}

uint16_t Traceroute::internet_checksum(const void* data, size_t len)
{
    auto data_array = reinterpret_cast<const uint16_t*>(data);

    uint32_t sum = 0;

    while (len > 1)
    {
        sum = sum + *data_array++;
        len -= 2;
    }

    if (len > 0)
    {
        sum = sum + *(reinterpret_cast<const uint8_t*>(data_array));
    }

    while (sum >> 16)
    {
        sum = (sum & 0x0000ffff) + (sum >> 16);
    }

    return (~sum);
}
