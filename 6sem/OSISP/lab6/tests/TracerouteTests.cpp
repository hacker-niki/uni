//
// Created by nikita on 27.06.24.
//

#include "../Traceroute.h"
#include <gtest/gtest.h>

TEST(TracerouteTest, IpFromName) {
    std::string hostname = "localhost";
    std::string expected_ip = "127.0.0.1";
    EXPECT_EQ(Traceroute::ip_from_name(hostname), expected_ip);
}

TEST(TracerouteTest, IpFromNOName) {
    std::string hostname = "somenonamesite.ks.go";
    std::string expected_ip = "";
    EXPECT_EQ(Traceroute::ip_from_name(hostname), expected_ip);
}

TEST(TracerouteTest, NameFromIp) {
    std::string ip = "127.0.0.1";
    std::string expected_name = "localhost";
    EXPECT_EQ(Traceroute::name_from_ip(ip), expected_name);
}

TEST(TracerouteTest, NameFromIncorrectIp) {
    std::string ip = "127.0.0.1.1";
    std::string expected_name = "";
    EXPECT_EQ(Traceroute::name_from_ip(ip), expected_name);
}

TEST(TracerouteTest, InternetChecksum) {
    const char data[] = "test data";
    size_t len = sizeof(data);
    uint16_t checksum = Traceroute::internet_checksum(data, len);
    EXPECT_NE(checksum, 0);
}

TEST(TracerouteTest, InternetChecksumEmpty) {
    const char data[] = "";
    uint16_t checksum = Traceroute::internet_checksum(data, sizeof(data) - 1);
    EXPECT_EQ(checksum, 0xFFFF);
}

TEST(TracerouteTest, InternetChecksumVector) {
    const uint8_t data[20] = {
            0x45, 0x00, 0x00, 0x73, 0x00, 0x00, 0x40, 0x00,
            0x40, 0x11, 0xB8, 0x61, 0xC0, 0xA8, 0x00, 0x01,
            0xC0, 0xA8, 0x30, 0xC7
    };
    auto data_array = reinterpret_cast<const uint16_t *>(data);
    int32_t sum = 0;
    int len = 20;
    while (len > 1) {
        sum = sum + *data_array++;
        len -= 2;
    }
    sum += Traceroute::internet_checksum(data, sizeof(data));

    while (sum >> 16) {
        sum = (sum & 0x0000ffff) + (sum >> 16);
    }

    EXPECT_EQ(~static_cast<int8_t>(sum), 0);
}

TEST(TracerouteTest, Run) {
    Traceroute traceroute;
    std::string ip = "127.0.0.1";
    int max_hops = 30;
    int timeout = 1;
    int start_ttl = 1;
    int retries = 3;

    EXPECT_NO_THROW(traceroute.run(ip, max_hops, timeout, start_ttl, retries));
}

int main(int argc, char **argv) {
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}