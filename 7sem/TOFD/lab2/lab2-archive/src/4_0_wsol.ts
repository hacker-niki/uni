import {
  Connection,
  Keypair,
  LAMPORTS_PER_SOL,
  SystemProgram,
  Transaction,
} from "@solana/web3.js";
import {
  createAssociatedTokenAccountInstruction,
  createSyncNativeInstruction,
  getAssociatedTokenAddress,
  NATIVE_MINT,
} from "@solana/spl-token";
import bs58 from "bs58";
import { secret } from "./secret.js";

const connection = new Connection("https://api.devnet.solana.com", "confirmed");
const owner = Keypair.fromSecretKey(secret);

async function wrapSol() {
  const amount = 0.5 * LAMPORTS_PER_SOL; // 1 SOL
  const ata = await getAssociatedTokenAddress(NATIVE_MINT, owner.publicKey);

  const tx = new Transaction().add(
    createAssociatedTokenAccountInstruction(
      owner.publicKey,
      ata,
      owner.publicKey,
      NATIVE_MINT,
    ),
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

  const sig = await connection.sendRawTransaction(tx.serialize());
  console.log("Wrapped SOL tx:", sig);
  console.log("WSOL ATA:", ata.toBase58());
}

wrapSol();
