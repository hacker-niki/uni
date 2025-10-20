import {
  Connection,
  Keypair,
  LAMPORTS_PER_SOL,
  SystemProgram,
  Transaction,
} from "@solana/web3.js";
import {
  getOrCreateAssociatedTokenAccount,
  createSyncNativeInstruction,
  NATIVE_MINT,
} from "@solana/spl-token";
import { secret } from "./secret.js";

const connection = new Connection("https://api.devnet.solana.com", "confirmed");
const owner = Keypair.fromSecretKey(secret);

async function wrapSol() {
  const amount = 0.5 * LAMPORTS_PER_SOL;
  

  const tokenAccount = await getOrCreateAssociatedTokenAccount(
    connection,
    owner,
    NATIVE_MINT,
    owner.publicKey
  );

  const ata = tokenAccount.address;

  const tx = new Transaction().add(
    SystemProgram.transfer({
      fromPubkey: owner.publicKey,
      toPubkey: ata,
      lamports: amount,
    }),
    
    createSyncNativeInstruction(ata),
  );

  tx.feePayer = owner.publicKey;
  tx.recentBlockhash = (await connection.getLatestBlockhash()).blockhash;
  tx.sign(owner);

  try {
    const sig = await connection.sendRawTransaction(tx.serialize());
    console.log("Wrapped SOL tx:", sig);
    console.log("WSOL ATA:", ata.toBase58());
    console.log(`Транзакция отправлена: https://explorer.solana.com/tx/${sig}?cluster=devnet`);

    await connection.confirmTransaction(sig);
    const balance = await connection.getTokenAccountBalance(ata);
    console.log(`Баланс WSOL: ${balance.value.uiAmount}`);
  } catch (error) {
    console.error("Ошибка при выполнении транзакции:", error);
  }
}

wrapSol();
