<?php

namespace App;

use Exception;
use GMP;

class RabinSystem
{
    /**
     * @param GMP $a
     * @param GMP $b
     * @return GMP[]
     */
    private static function extendedGcd(GMP $a, GMP $b): array
    {
        // [g, s, t], g = НОД, as + bt = g
        return gmp_gcdext($a, $b);
    }

    /**
     * r ≡ mp (mod p) и r ≡ mq (mod q).
     *
     * @param GMP $mp
     * @param GMP $p
     * @param GMP $mq
     * @param GMP $q
     * @return GMP
     */
    private static function crt(GMP $mp, GMP $p, GMP $mq, GMP $q): GMP
    {
        list($gcd, $yp, $yq) = self::extendedGcd($p, $q);
        $n = gmp_mul($p, $q);
        // Формула: (mp*yq*q + mq*yp*p) mod n
        $term1 = gmp_mul(gmp_mul($mp, $yq), $q);
        $term2 = gmp_mul(gmp_mul($mq, $yp), $p);
        return gmp_mod(gmp_add($term1, $term2), $n);
    }

    /**
     *
     * @param GMP $mp
     * @param GMP $p
     * @param GMP $mq
     * @param GMP $q
     * @return GMP
     */
    private static function mCrt(GMP $mp, GMP $p, GMP $mq, GMP $q): GMP
    {
        list($gcd, $yp, $yq) = self::extendedGcd($p, $q);
        $n = gmp_mul($p, $q);
        // Формула: (mp*yq*q - mq*yp*p) mod n
        $term1 = gmp_mul(gmp_mul($mp, $yq), $q);
        $term2 = gmp_mul(gmp_mul($mq, $yp), $p);
        return gmp_mod(gmp_sub($term1, $term2), $n);
    }

    /**
     *
     * @param int $bitLength Длина ключа в битах для каждого простого числа.
     * @return array ['public' => GMP, 'private' => ['p' => GMP, 'q' => GMP]]
     */
    public static function generateKeys(int $bitLength = 512): array
    {
        $four = gmp_init(4);
        $three = gmp_init(3);

        // Генерируем простое число p, такое что p ≡ 3 (mod 4)
        do {
            $p = gmp_nextprime(gmp_random_bits($bitLength));
        } while (gmp_cmp(gmp_mod($p, $four), $three) !== 0);

        // Генерируем простое число q, такое что q ≡ 3 (mod 4)
        do {
            $q = gmp_nextprime(gmp_random_bits($bitLength));
        } while (gmp_cmp(gmp_mod($q, $four), $three) !== 0);

        $n = gmp_mul($p, $q); // Публичный ключ

        return [
            'public' => $n,
            'private' => ['p' => $p, 'q' => $q]
        ];
    }

    /**
     *
     * @param GMP $message Сообщение (представленное как число)
     * @param GMP $publicKey Публичный ключ (N)
     * @return GMP Шифротекст
     * @throws Exception
     */
    public static function encrypt(GMP $message, GMP $publicKey): GMP
    {
        if (gmp_cmp($message, $publicKey) >= 0) {
            throw new Exception("Сообщение должно быть меньше публичного ключа N.");
        }
        // c = m^2 mod N
        return gmp_powm($message, gmp_init(2), $publicKey);
    }

    /**
     *
     * @param GMP $ciphertext Шифротекст
     * @param array $privateKey ['p' => GMP, 'q' => GMP]
     * @return GMP[] Массив из четырех возможных исходных сообщений.
     */
    public static function decrypt(GMP $ciphertext, array $privateKey): array
    {
        $p = $privateKey['p'];
        $q = $privateKey['q'];
        $n = gmp_mul($p, $q);

        $exp_p = gmp_div_q(gmp_add($p, gmp_init(1)), gmp_init(4));
        $mp = gmp_powm($ciphertext, $exp_p, $p);

        $exp_q = gmp_div_q(gmp_add($q, gmp_init(1)), gmp_init(4));
        $mq = gmp_powm($ciphertext, $exp_q, $q);

        $r1 = self::crt($mp, $p, $mq, $q);
        $r2 = gmp_sub($n, $r1);
        $s1 = self::mCrt($mp, $p, $mq, $q);
        $s2 = gmp_sub($n, $s1);

        return [$r1, $r2, $s1, $s2];
    }
}