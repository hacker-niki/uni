CC = gcc
CFLAGS = -Wall -Wextra -Werror
TARGET = morse_filter
SRC = main.c morse.c
OBJ = $(SRC:.c=.o)

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(CFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJ) $(TARGET)

test: $(TARGET)
	@echo "Тестирование программы:"
	@echo "SOS" | ./$(TARGET) > output.txt
	@echo "Ожидаемый результат: ... --- ..."
	@cat output.txt
