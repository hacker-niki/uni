<?php

namespace App;

class GostEncrypt
{
    private const DEFAULT_S_BOXES = [
        [4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3],
        [14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9],
        [5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11],
        [7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3],
        [6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2],
        [4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14],
        [13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12],
        [1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12]
    ];

    /**
     * @param string $key
     * @return int[]
     */
    private function prepareSubkeys(string $key): array
    {
        $subkeys = [];
        for ($i = 0; $i < 32; $i += 4) {
            $subkeys[] = unpack('N', substr($key, $i, 4))[1];
        }

        $roundSubkeys = [];
        for ($round = 0; $round < 32; $round++) {
            if ($round < 24) {
                $roundSubkeys[] = $subkeys[$round % 8];
            } else {
                $roundSubkeys[] = $subkeys[7 - ($round % 8)];
            }
        }
        return $roundSubkeys;
    }

    /**
     * @param  int|null  $data
     * @param  int  $subkey
     * @param  array  $sBoxes
     *
     * @return int
     */
    private function feistelFunction(?int $data, int $subkey, array $sBoxes): int
    {
        $temp = ($data + $subkey) & 0xFFFFFFFF;
        $result = 0;
        for ($i = 0; $i < 8; $i++) {
            $sBoxIndex = ($temp >> (4 * $i)) & 0xF;
            $sBoxValue = $sBoxes[$i][$sBoxIndex];
            $result |= ($sBoxValue << (4 * $i));
        }

        return (($result << 11) | ($result >> 21)) & 0xFFFFFFFF;
    }

    /**
     * @param string $block
     * @param string $key
     * @return string
     */
    private function gostEncryptBlock(string $block, string $key): string
    {
        $sBoxes = self::DEFAULT_S_BOXES;
        $subkeys = $this->prepareSubkeys($key);

        $parts = unpack('N2', $block);
        $left = $parts[1];
        $right = $parts[2];

        for ($round = 0; $round < 32; $round++) {
            $subkey = $subkeys[$round];
            $fResult = $this->feistelFunction($right, $subkey, $sBoxes);
            $newRight = $left ^ $fResult;
            $left = $right;
            $right = $newRight;
        }

        [$left, $right] = [$right, $left];

        return pack('NN', $left, $right);
    }

    /**
     * @param string $block
     * @param string $key
     * @return string
     */
    private function gostDecryptBlock(string $block, string $key): string
    {
        $sBoxes = self::DEFAULT_S_BOXES;
        $subkeys = $this->prepareSubkeys($key);

        $parts = unpack('N2', $block);
        $left = $parts[1];
        $right = $parts[2];

        for ($round = 31; $round >= 0; $round--) {
            $subkey = $subkeys[$round];
            $fResult = $this->feistelFunction($right, $subkey, $sBoxes);
            $newRight = $left ^ $fResult;
            $left = $right;
            $right = $newRight;
        }

        [$left, $right] = [$right, $left];

        return pack('NN', $left, $right);
    }

    /**
     * @param string $data
     * @param string $key
     * @return string
     */
    public function encrypt(string $data, string $key): string
    {
        $paddingLength = 8 - (strlen($data) % 8);
        if ($paddingLength === 0) {
            $paddingLength = 8;
        }

        $paddedData = $data . str_repeat(chr($paddingLength), $paddingLength);

        $encryptedBlocks = [];
        for ($i = 0; $i < strlen($paddedData); $i += 8) {
            $block = substr($paddedData, $i, 8);
            $encryptedBlocks[] = $this->gostEncryptBlock($block, $key);
        }

        return implode('', $encryptedBlocks);
    }

    /**
     * @param string $encryptedData
     * @param string $key
     * @return string|false
     */
    public function decrypt(string $encryptedData, string $key)
    {
        $decryptedBlocks = [];
        for ($i = 0; $i < strlen($encryptedData); $i += 8) {
            $block = substr($encryptedData, $i, 8);
            $decryptedBlocks[] = $this->gostDecryptBlock($block, $key);
        }

        $decryptedData = implode('', $decryptedBlocks);
        $lastByte = substr($decryptedData, -1);

        if ($lastByte === false) {
            return false;
        }

        $paddingLength = ord($lastByte);

        if ($paddingLength > 0 && $paddingLength <= 8) {
            $padding = substr($decryptedData, -$paddingLength);
            if ($padding === str_repeat(chr($paddingLength), $paddingLength)) {
                return substr($decryptedData, 0, -$paddingLength);
            }
        }

        return $decryptedData;
    }
}
