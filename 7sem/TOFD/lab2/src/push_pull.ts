import {
    Raydium,
    TxVersion,
    // Импортируем типы, необходимые для получения информации о пуле
    type ApiV3PoolInfoStandardItemCpmm,
} from "@raydium-io/raydium-sdk-v2";
import BN from 'bn.js'
import { clusterApiUrl, Connection, Keypair, PublicKey } from "@solana/web3.js";
import { NATIVE_MINT } from "@solana/spl-token";
import { secret } from "./secret.js";

const txVersion = TxVersion.V0

// !!! Вставьте адрес созданного ранее пула здесь !!!
const poolId = 'BNjcyQ6WgC2uHKDuzLqYY8BBJ2c8MmCFHsY85nTQsezR' 

// --- ПАРАМЕТРЫ ДОБАВЛЕНИЯ ЛИКВИДНОСТИ ---
const addTokenAAmount = new BN(10000) // Количество Токена A для добавления (пример)
// 0.1 SOL (100,000,000 лампартов, если 9 десятичных знаков)
const addTokenBAmount = new BN(1000_000_000) 

const connection = new Connection(clusterApiUrl('devnet'))
const owner = Keypair.fromSecretKey(secret);

const raydium = await Raydium.load(
    {
        owner: owner,
        connection: connection,
        cluster: "devnet",
        disableFeatureCheck: true,
        blockhashCommitment: "finalized",
        urlConfigs: {
            BASE_HOST: 'https://api-v3-devnet.raydium.io',
            OWNER_BASE_HOST: 'https://owner-v1-devnet.raydium.io',
            SWAP_HOST: 'https://transaction-v1-devnet.raydium.io',
            CPMM_LOCK: 'https://dynamic-ipfs-devnet.raydium.io/lock/cpmm/position',
        }
    }
)

async function addLiquidityToPool() {
    // 1. Получение информации о пуле
    const data = await raydium.cpmm.getPoolInfoFromRpc(poolId)
    const poolInfo: ApiV3PoolInfoStandardItemCpmm = data.poolInfo
    
    // 2. Построение транзакции добавления ликвидности
    const { execute, transaction } = await raydium.cpmm.addLiquidity({
        poolInfo,
        amountA: addTokenAAmount,
        amountB: addTokenBAmount,
        // Поскольку Token B - это WSOL (So111...), мы используем его как токен SPL,
        // поэтому useSOLBalance: false
        ownerInfo: {
            useSOLBalance: false,
        },
        txVersion,
    })

    // 3. Отправка и подтверждение транзакции
    const { txId } = await execute({ sendAndConfirm: true })
    
    console.log('Liquidity added', {
        txId: `https://explorer.solana.com/tx/${txId}?cluster=devnet`,
        poolId: poolId
    })
}

// Запуск функции
addLiquidityToPool()
