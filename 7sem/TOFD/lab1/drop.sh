#!/bin/bash

set -e

solana config set --url http://127.0.0.1:8899

echo "--- Airdrop ---"
sleep 1
solana airdrop 2 wallet-sender.json

echo ""
echo "--- балансы до перевода ---"
echo "Отправитель:"
solana balance wallet-sender.json
echo "Получатель:"
solana balance wallet-receiver.json

echo ""
echo "--- перевод ---"

# Правильный способ получить ВЫВОД команды в переменную
RECIPIENT_ADDRESS=$(solana-keygen pubkey wallet-receiver.json)
echo "получатель: $RECIPIENT_ADDRESS"

TRANSACTION_SIGNATURE=$(solana transfer "$RECIPIENT_ADDRESS" 1 --from wallet-sender.json --fee-payer wallet-sender.json --allow-unfunded-recipient | awk '{print $2}' | tr -d '\n\r')
echo "Транзакция отправлена. Сигнатура: $TRANSACTION_SIGNATURE"

echo ""
echo "--- подтверждение транзакции ---"
solana confirm -v "$TRANSACTION_SIGNATURE"

echo ""
echo "Финальные балансы:"
echo "Отправитель:"
solana balance wallet-sender.json
echo "Получатель:"
solana balance wallet-receiver.json

echo ""
echo "Profit!"

  
