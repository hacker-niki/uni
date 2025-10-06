import {
    createMint,
    TOKEN_PROGRAM_ID,
    createAccount,
    mintTo
} from "@solana/spl-token";
import "dotenv/config";
import { Connection, Keypair, clusterApiUrl } from "@solana/web3.js";
import { secret } from "./secret.js";


const connection = new Connection(
    clusterApiUrl('devnet'),
    {
        commitment: "confirmed"
    }
);

// Load the secret key from the env file and generate the keypair
const owner = Keypair.fromSecretKey(secret);

console.log(`Public key is: ${owner.publicKey.toBase58()}`);

const tokenMint = await createMint(
    connection,
    owner,
    owner.publicKey,
    null,
    8,
);

const tokenAccount = await createAccount(
    connection,
    owner,
    tokenMint,
    owner.publicKey,
    undefined,
    undefined,
    TOKEN_PROGRAM_ID
)

await mintTo(
    connection,
    owner,
    tokenMint,
    tokenAccount,
    owner,
    10_000_000_000,
)

console.log(`✅ Finished! Created token mint: ${tokenMint} and associated account ${tokenAccount}`);