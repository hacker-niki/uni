import json
from solders.keypair import Keypair

# Генерируем новую пару ключей
keypair = Keypair()

print(f"Новая пара ключей сгенерирована!")
print(f"✅ Публичный ключ: {keypair.pubkey()}")

# Сохраняем секретный ключ в файл.
# Он должен быть преобразован в список для JSON-сериализации.
secret_key_list = list(keypair.secret())
with open('generated_wallet.json', 'w') as f:
    json.dump(secret_key_list, f)

print(f"✅ Секретный ключ сохранен в generated_wallet.json")
