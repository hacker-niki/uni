# Определяем компилятор и флаги
CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra

# Имя исполняемого файла
TARGET = console_app

# Исходные файлы
SRCS = main.cpp

# Объектные файлы
OBJS = $(SRCS:.cpp=.o)

# Правило по умолчанию
all: $(TARGET)

# Правило для создания исполняемого файла
$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^

# Правило для компиляции объектных файлов
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Правило для очистки
clean:
	rm -f $(OBJS) $(TARGET)

# Правило для запуска
run: $(TARGET)
	./$(TARGET)

.PHONY: all clean run
