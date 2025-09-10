import json
import sys
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer
from solders.transaction import Transaction 
from solana.rpc.api import Client

RPC_URL = "http://127.0.0.1:8899"

SENDER_WALLET_PATH = "wallet-sender.json"
AMOUNT_LAMPORTS = 100000
RECEIVER_PUBKEY = "9yakXJfBh2xRFheqvupjtedsbxLx7ASAbjKqiSBHg5QE"

def load_keypair_from_file(filepath: str) -> Keypair:
    with open(filepath, 'r') as f:
        secret_key_list = json.load(f)
    return Keypair.from_bytes(bytes(secret_key_list))

def main():

    try:
        receiver_pubkey = Pubkey.from_string(RECEIVER_PUBKEY)
    except ValueError:
        print(f"Неверный адрес получателя")
        sys.exit(1)
        
    try:
        sender_keypair = load_keypair_from_file(SENDER_WALLET_PATH)
        print(f"Кошелек отправителя: {sender_keypair.pubkey()}")
    except FileNotFoundError:
        print(f"Файл кошелька не найден: {SENDER_WALLET_PATH}")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при загрузке кошелька: {e}")
        sys.exit(1)

    solana_client = Client(RPC_URL)

    print(f"Перевод {AMOUNT_LAMPORTS} лампортов с {sender_keypair.pubkey()} на {receiver_pubkey}...")

    try:
        latest_blockhash = solana_client.get_latest_blockhash().value.blockhash

        transfer_instruction = transfer(
            TransferParams(
                from_pubkey=sender_keypair.pubkey(),
                to_pubkey=receiver_pubkey,
                lamports=AMOUNT_LAMPORTS
            )
        )

        transaction = Transaction.new_signed_with_payer(
            [transfer_instruction],       # Инструкции
            sender_keypair.pubkey(),      # Кто платит за транзакцию
            [sender_keypair],             # Кто подписывает
            latest_blockhash              # Последний blockhash
        )
        
        resp = solana_client.send_transaction(transaction)
        
        signature = resp.value
        print(f"Транзакция отправлена")

        solana_client.confirm_transaction(signature, "confirmed")

        print(f"Ссылка на транзакцию: https://explorer.solana.com/tx/{signature}?cluster=custom&customUrl={RPC_URL}")

    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
