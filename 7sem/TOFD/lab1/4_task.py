import json
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer
from solders.transaction import Transaction
from solana.constants import LAMPORTS_PER_SOL

# --- КОНФИГУРАЦИЯ ---
RPC_URL = "http://127.0.0.1:8899"  # Локальный валидатор
# RPC_URL = "https://api.devnet.solana.com" # Solana Devnet

SENDER_KEYPAIR_PATH = './wallet-sender.json'
# ЗАМЕНИТЕ НА АДРЕС ПОЛУЧАТЕЛЯ ИЗ wallet-receiver.json
RECEIVER_PUBLIC_KEY = Pubkey.from_string("вставьте_сюда_адрес_получателя")

def transfer_all_sol(client, sender, receiver):
    try:
        # 1. Получаем текущий баланс отправителя
        balance_resp = client.get_balance(sender.pubkey())
        balance_lamports = balance_resp.value
        
        print(f"Текущий баланс: {balance_lamports / LAMPORTS_PER_SOL} SOL")

        if balance_lamports == 0:
            print("Баланс нулевой, перевод невозможен.")
            return

        # 2. Рассчитываем комиссию (для простого перевода она фиксированная)
        fee = 5000  # 5000 лампортов
        
        amount_to_send = balance_lamports - fee

        if amount_to_send <= 0:
            print("Недостаточно средств для оплаты комиссии.")
            return

        print(f"Сумма к отправке (за вычетом комиссии): {amount_to_send / LAMPORTS_PER_SOL} SOL")

        # 3. Создаем и отправляем транзакцию (аналогично скрипту 3)
        recent_blockhash = client.get_latest_blockhash().value.blockhash
        instruction = transfer(
            TransferParams(from_pubkey=sender.pubkey(), to_pubkey=receiver, lamports=amount_to_send)
        )
        transaction = Transaction([instruction], recent_blockhash, sender.pubkey())
        transaction.sign([sender])
        resp = client.send_transaction(transaction)
        signature = resp.value
        client.confirm_transaction(signature)
        
        print(f"✅ Весь баланс переведен! Сигнатура: {signature}")

    except Exception as e:
        print(f"Ошибка при переводе: {e}")

# --- Основная логика ---
if __name__ == "__main__":
    with open(SENDER_KEYPAIR_PATH, 'r') as f:
        secret_key = bytes(json.load(f))
    sender_keypair = Keypair.from_bytes(secret_key)
    
    solana_client = Client(RPC_URL)
    
    transfer_all_sol(solana_client, sender_keypair, RECEIVER_PUBLIC_KEY)
