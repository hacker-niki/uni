import json
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer
from solders.transaction import Transaction
from solana.constants import LAMPORTS_PER_SOL

RPC_URL = "http://127.0.0.1:8899" 

SENDER_KEYPAIR_PATH = './wallet-receiver.json'
RECEIVER_PUBLIC_KEY = Pubkey.from_string("Fo8zU5fKDdPDBzUmemCVDDV7YGJjfWRGGq6meWKnBmxH")

def transfer_all_sol(client, sender, receiver):
    try:
        balance_resp = client.get_balance(sender.pubkey())
        balance_lamports = balance_resp.value
        
        print(f"Текущий баланс: {balance_lamports / LAMPORTS_PER_SOL} SOL")

        if balance_lamports == 0:
            print("Баланс нулевой, перевод невозможен.")
            return

        fee = 5000 
        
        amount_to_send = balance_lamports - fee

        if amount_to_send <= 0:
            print("Недостаточно средств для оплаты комиссии.")
            return

        print(f"Сумма к отправке (за вычетом комиссии): {amount_to_send / LAMPORTS_PER_SOL} SOL")

        instruction = transfer(
            TransferParams(from_pubkey=sender.pubkey(), to_pubkey=receiver, lamports=amount_to_send)
        )
        
        recent_blockhash = client.get_latest_blockhash().value.blockhash
        
        transaction = Transaction.new_with_payer(
            instructions=[instruction],
            payer=sender.pubkey(),
        )
        
        transaction.sign([sender], recent_blockhash)
        
        resp = client.send_transaction(transaction)
        signature = resp.value
        
        print(f"Транзакция отправлена. Ожидаем подтверждения...")
        client.confirm_transaction(signature, 'confirmed')
        
        print(f"Весь баланс переведен! Сигнатура: {signature}")

    except Exception as e:
        print(f"Ошибка при переводе: {e}")

if __name__ == "__main__":
    try:
        with open(SENDER_KEYPAIR_PATH, 'r') as f:
            secret_key = bytes(json.load(f))
        sender_keypair = Keypair.from_bytes(secret_key)
        
        solana_client = Client(RPC_URL)
        
        transfer_all_sol(solana_client, sender_keypair, RECEIVER_PUBLIC_KEY)

    except FileNotFoundError:
        print(f"Ошибка: Не найден файл кошелька '{SENDER_KEYPAIR_PATH}'")
    except Exception as e:
        print(f"Произошла общая ошибка: {e}")
