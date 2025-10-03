import numpy as np
import bitstring

def extract_data_from_DCT(dct_blocks):
    extracted_data = ""
    for current_dct_block in dct_blocks:
        for i in range(1, len(current_dct_block)):
            curr_coeff = np.int32(current_dct_block[i])
            if (curr_coeff > 1):
                #извдекаем данные из младшего бити LSB коэффициента
                extracted_data += bitstring.pack('uint:1', np.uint8(current_dct_block[i]) & 0x01)
    return extracted_data

def embed_data_into_DCT(encoded_bits, dct_blocks):
    data_complete = False
    encoded_bits.pos = 0
    encoded_data_len = bitstring.pack('uint:32', len(encoded_bits))
    converted_blocks = []
    for current_dct_block in dct_blocks:
        for i in range(1, len(current_dct_block)):
            curr_coeff = np.int32(current_dct_block[i])
            #нужно работать только с коэффициентами > 1 чтобы не ломать картинку
            if (curr_coeff > 1):
                curr_coeff = np.uint8(current_dct_block[i])
                if (encoded_bits.pos == (len(encoded_bits) - 1)): 
                    data_complete = True
                    break
                pack_coeff = bitstring.pack('uint:8', curr_coeff)
                if (encoded_data_len.pos <= len(encoded_data_len) - 1):
                    #сначала длину
                    pack_coeff[-1] = encoded_data_len.read(1)
                else: 
                    #потом данные
                    pack_coeff[-1] = encoded_bits.read(1)
                #возвращаем модифицированный коэффициент в блок
                current_dct_block[i] = np.float32(pack_coeff.read('uint:8'))
        #возвращаем блок в результат
        converted_blocks.append(current_dct_block)

    if not(data_complete): 
        raise ValueError("Data didn't fully embed into cover image!")

    return converted_blocks