#include <boost/asio.hpp>
#include <chrono>
#include <iostream>
#include <unordered_set>

using boost::asio::ip::tcp;
using namespace std::chrono;

constexpr bool PROTECTION_ENABLED = true;
constexpr int MAX_HALF_OPEN_CONNECTIONS = 10;
constexpr int ACK_THRESHOLD = 20;
constexpr int DATA_THRESHOLD = 1024;

std::unordered_set<std::string> half_open_connections;

std::string generate_token() {
    static const char alphanum[] = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    std::string token(6, '\0');
    for (int i = 0; i < 6; ++i) {
        token[i] = alphanum[rand() % (sizeof(alphanum) - 1)];
    }
    return token;
}

class session : public std::enable_shared_from_this<session> {
public:
    session(tcp::socket socket) : socket_(std::move(socket)), data_count_(0) {}

    void start() {
        if (PROTECTION_ENABLED && half_open_connections.size() >= MAX_HALF_OPEN_CONNECTIONS) {
            std::cerr << "Слишком много полуоткрытых соединений. Возможная SYN Flood атака.\n";
            socket_.close();
            return;
        }

        auto self(shared_from_this());
        peername_ = socket_.remote_endpoint().address().to_string() + ":" +
                    std::to_string(socket_.remote_endpoint().port());
        half_open_connections.insert(peername_);

        token_ = generate_token();
        std::string secret = "SECRETTOK " + token_ + "\n";
        async_write(socket_, boost::asio::buffer(secret),
            [this, self](boost::system::error_code ec, std::size_t) {
                if (!ec) {
                    do_read();
                } else {
                    half_open_connections.erase(peername_);
                }
            });
    }

private:
    void do_read() {
        auto self(shared_from_this());
        socket_.async_read_some(boost::asio::buffer(data_, max_length),
            [this, self](boost::system::error_code ec, std::size_t length) {
                if (!ec) {
                    std::string response(data_, length);
                    if (response.find("RESPONSE " + token_) != std::string::npos) {
                        std::cerr << "Успешное рукопожатие с " << peername_ << "\n";
                        half_open_connections.erase(peername_);
                        async_write(socket_, boost::asio::buffer("Успешное рукопожатие\n"),
                            [this, self](boost::system::error_code ec, std::size_t) {
                                if (!ec) {
                                    do_echo();
                                }
                            });
                    } else {
                        std::cerr << "Неверный токен от " << peername_ << ". ACK flood атака.\n";
                        socket_.close();
                        half_open_connections.erase(peername_);
                    }
                } else {
                    half_open_connections.erase(peername_);
                }
            });
    }

    void do_echo() {
        auto self(shared_from_this());
        socket_.async_read_some(boost::asio::buffer(data_, max_length),
            [this, self](boost::system::error_code ec, std::size_t length) {
                if (!ec) {
                    data_count_ += length;
                    if (PROTECTION_ENABLED && data_count_ > DATA_THRESHOLD) {
                        std::cerr << "Data Flood обнаружен от " << peername_ << ". Соединение закрыто.\n";
                        socket_.close();
                        return;
                    }

                    std::string message(data_, length);

                    auto now = steady_clock::now();
                    if (now - last_ack_time_ > milliseconds(100)) {
                        ack_count_ = 0;
                        last_ack_time_ = now;
                    }
                    ack_count_++;
                    if (PROTECTION_ENABLED && ack_count_ > ACK_THRESHOLD) {
                        std::cerr << "ACK Flood обнаружен от " << peername_ << ". Соединение закрыто.\n";
                        socket_.close();
                        return;
                    }

                    if (message == "quit") {
                        socket_.close();
                    } else {
                        boost::asio::async_write(socket_, boost::asio::buffer("ECHO: " + message),
                            [this, self](boost::system::error_code ec, std::size_t) {
                                if (!ec) {
                                    do_echo();
                                }
                            });
                    }
                }
            });
    }

    tcp::socket socket_;
    enum { max_length = 1024 };
    char data_[max_length];
    std::string token_;
    std::string peername_;
    int ack_count_ = 0;
    steady_clock::time_point last_ack_time_ = steady_clock::now();
    size_t data_count_;
};

class server {
public:
    server(boost::asio::io_context& io_context, short port)
        : acceptor_(io_context, tcp::endpoint(tcp::v4(), port)) {
        do_accept();
    }

private:
    void do_accept() {
        acceptor_.async_accept([this](boost::system::error_code ec, tcp::socket socket) {
            if (!ec) {
                std::make_shared<session>(std::move(socket))->start();
            }
            do_accept();
        });
    }

    tcp::acceptor acceptor_;
};

constexpr int port = 777;

int main() {
    try {
        boost::asio::io_context io_context;
        server s(io_context, port);
        io_context.run();
    } catch (std::exception& e) {
        std::cerr << "Исключение: " << e.what() << "\n";
    }
    return 0;
}