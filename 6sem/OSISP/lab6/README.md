# Traceroute

Этот проект реализует утилиту для выполнения traceroute.

## Сборка

 ```sh
 git clone https://github.com/hacker-niki/traceroute.git
 cd traceroute

 mkdir build
 cd build

 cmake ..

 make
 ```

После успешной сборки в каталоге `build` появится исполняемый файл `Traceroute`.

## Запуск

Для запуска утилиты необходимы права администратора:

```sh
sudo ./Traceroute <host> 
```

## Опции

    -h, --help: Показать это сообщение и выйти.
    -m, --max-hops N: Установить максимальное количество хопов (по умолчанию: 30).
    -t, --timeout N: Установить таймаут в секундах (по умолчанию: 1).
    -f, --start-ttl N: Установить начальное значение TTL (по умолчанию: 1).
    -r, --retries N: Установить количество повторных попыток (по умолчанию: 1).

## Тестирование

```sh
sudo ./TracerouteTests
```