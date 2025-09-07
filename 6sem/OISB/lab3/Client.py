import requests
import time
from common import encrypt, decrypt

SERVER_URL = {
    "AS": "http://localhost:8080",
    "TGS": "http://localhost:8081",
    "SS": "http://localhost:8082"
}

SERVER_ID = {
    "SS": "ss"
}


def main():
    username = input("Enter username: ")
    password = input("Enter password (8 symbols): ")

    while len(password) != 8:
        print("Password must be 8 symbols long.")
        password = input("Enter password (8 symbols): ")

    # 1
    print('#1============================================================')

    as_request_url = f"{SERVER_URL['AS']}/{username}"
    print(f'{as_request_url=}')

    response = requests.get(as_request_url)
    if response.status_code != 200:
        print("AS server answered with:", response.status_code)
        exit(-1)

    # 2
    print('#2============================================================')
    print("AS server response (enctryped):", response.text)

    response = decrypt(response.text, password)
    print("AS server response (decrypted):", response, f"| decrypted with K_c={password}")

    TGT_encrypted, K_c_tgs = response.split(';')
    print(f'{TGT_encrypted=}, {K_c_tgs=}')

    # 3
    print('#3============================================================')

    aut1 = f"{username};{int(time.time())}"
    print(f'{aut1=}')

    aut1_encrypted = encrypt(aut1, K_c_tgs)
    print(f'{aut1_encrypted=} | encrypted with {K_c_tgs=}')

    tgs_request_data = f"{TGT_encrypted};{aut1_encrypted};{SERVER_ID['SS']}"
    print(f'tgs_request_url={SERVER_URL["TGS"]}')
    print(f'{tgs_request_data=}')

    response = requests.post(SERVER_URL["TGS"], data=tgs_request_data)
    if response.status_code != 200:
        print("TGS server answered with:", response.status_code)
        exit(-1)

    # 4
    print('#4============================================================')
    print("TGS server response (enctryped):", response.text)

    response = decrypt(response.text, K_c_tgs)
    print("TGS server response (decrypted):", response, f"| decrypted with {K_c_tgs=}")

    TGS_encrypted, K_c_ss = response.split(';')
    print(f'{TGS_encrypted=}')
    print(f'{K_c_ss=}')

    # 5
    print('#5============================================================')

    t4 = int(time.time())
    aut2 = f"{username};{t4}"
    aut2_encrypted = encrypt(aut2, K_c_ss)
    print(f'{t4=}')
    print(f'{aut2=}')
    print(f'{aut2_encrypted=}', f'| encrypted with {K_c_ss=}')

    ss_request_data = f"{TGS_encrypted};{aut2_encrypted}"
    print(f'ss_request_url={SERVER_URL["SS"]}')
    print(f'{ss_request_data=}')

    response = requests.post(SERVER_URL["SS"], data=ss_request_data)
    if response.status_code != 200:
        print("SS server answered with:", response.status_code)
        exit(-1)

    # 6
    print('#6============================================================')
    print("SS server response (enctryped):", response.text)

    response = decrypt(response.text, K_c_ss)
    print("SS server response (decrypted):", response, f'| decrypted with {K_c_ss=}')

    if int(response.split(';')[0]) != t4 + 1:
        print("SS server verification failed!")
        exit(1)

    print("OK!")


if __name__ == '__main__':
    main()