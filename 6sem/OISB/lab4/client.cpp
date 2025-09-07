#include <boost/asio.hpp>
#include <iostream>
#include <string>

using boost::asio::ip::tcp;

constexpr std::string host = "localhost";
constexpr std::string port = "777";

int main()
{
    try
    {
        boost::asio::io_context io_context;
        tcp::resolver resolver(io_context);
        tcp::resolver::results_type endpoints = resolver.resolve(host, port);
        tcp::socket socket(io_context);
        boost::asio::connect(socket, endpoints);

        std::string data;
        read_until(socket, boost::asio::dynamic_buffer(data), '\n');
        std::cout << "Получено: " << data;

        if (data.find("SECRETTOK") != std::string::npos)
        {
            std::string token = data.substr(10, 6);
            std::string response = "RESPONSE " + token + "\n";
            boost::asio::write(socket, boost::asio::buffer(response));
            data.clear();
            read_until(socket, boost::asio::dynamic_buffer(data), '\n');
            std::cout << "Результат рукопожатия: " << data;
        }

        while (true)
        {
            std::cout << "Сообщение: ";
            std::string message;
            std::getline(std::cin, message);
            boost::asio::write(socket, boost::asio::buffer(message + "\n"));

            data.clear();
            read_until(socket, boost::asio::dynamic_buffer(data), '\n');
            std::cout << "Ответ от сервера: " << data;
        }
    }
    catch (std::exception& e)
    {
        std::cerr << "Исключение: " << e.what() << "\n";
    }

    return 0;
}
