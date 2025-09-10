import sys
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from solana.constants import LAMPORTS_PER_SOL

RPC_URL = "http://127.0.0.1:8899"  # Локальный валидатор

def get_address_from_args():
    if len(sys.argv) < 2:
        print("Пожалуйста, укажите адрес кошелька в качестве аргумента.")
        sys.exit(1)
    
    try:
        return Pubkey.from_string(sys.argv[1])
    except ValueError:
        print(f"Неверный адрес: {sys.argv[1]}")
        sys.exit(1)

def airdrop(client, public_key):
    try:
        print(f"Запрашиваем 1 SOL для {public_key}...")
        
        # Запрашиваем аирдроп
        resp = client.request_airdrop(public_key, 1 * LAMPORTS_PER_SOL)
        
        # Получаем подпись транзакции
        signature = resp.value
        
        # Ожидаем подтверждения транзакции
        client.confirm_transaction(signature)
        
        print(f"Аирдроп успешен! Транзакция: {signature}")

    except Exception as e:
        print(f"Ошибка при аирдропе: {e}")

# --- Основная логика ---
if __name__ == "__main__":
    address_to_airdrop = get_address_from_args()
    solana_client = Client(RPC_URL)
    airdrop(solana_client, address_to_airdrop)
