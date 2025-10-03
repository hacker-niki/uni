import cv2
import struct
import bitstring
import numpy  as np
import zigzag as zz
import image_preparation as img
import data_embedding as stego

NUM_CHANNELS = 3

if __name__=='__main__':
    image_filepath  = "lr8/image.jpg"
    stego_image_filepath  = "lr8/stego_image.jpg"
    test_message = "Love. Calm. Kidness. Kinship."
    
    #--------Вставка--------
    raw_cover_image = cv2.imread(image_filepath, flags=cv2.IMREAD_COLOR)
    height, width   = raw_cover_image.shape[:2]
    while(height % 8): height += 1
    while(width  % 8): width  += 1
    valid_dim = (width, height)


    padded_image = cv2.resize(raw_cover_image, valid_dim)
    #переводим картинку RGB в float32
    cover_image_f32 = np.float32(padded_image)
    #переводим их RGB в YCbCr и сохраняем в классе YCC_Image
    cover_image_YCC = img.YCC_Image(cv2.cvtColor(cover_image_f32, cv2.COLOR_BGR2YCrCb))

    #пустое место под будующую картинку
    stego_image = np.empty_like(cover_image_f32)



    for chan_index in range(NUM_CHANNELS):
        #DCT
        dct_blocks = [cv2.dct(block) for block in cover_image_YCC.channels[chan_index]]

        # квантование, необходимо чтобы перейти от fl32 к int так как в int проще вставлять данные
        dct_quants = [np.around(np.divide(item, img.JPEG_STD_LUM_QUANT_TABLE)) for item in dct_blocks]
        #переставляем коэффициенты зигзагом
        sorted_coefficients = [zz.zigzag(block) for block in dct_quants]

        #вставляем в Y слой
        if (chan_index == 0):
            secret_data = ""
            for char in test_message.encode('ascii'): 
                secret_data += bitstring.pack('uint:8', char)
            embedded_dct_blocks   = stego.embed_data_into_DCT(secret_data, sorted_coefficients)
                #переставляем коэффициенты зигзагом обратно
            desorted_coefficients = [zz.inverse_zigzag(block, vmax=8,hmax=8) for block in embedded_dct_blocks]
        else:
            #переставляем коэффициенты зигзагом обратно без вставки данных в Cb и Cr
            desorted_coefficients = [zz.inverse_zigzag(block, vmax=8,hmax=8) for block in sorted_coefficients]

        # Обратная квантоыизация
        dct_dequants = [np.multiply(data, img.JPEG_STD_LUM_QUANT_TABLE) for data in desorted_coefficients]

        #обратный DCT
        idct_blocks = [cv2.idct(block) for block in dct_dequants]

        # склеиваем изображение
        stego_image[:,:,chan_index] = np.asarray(img.stitch_8x8_blocks_back_together(cover_image_YCC.width, idct_blocks))

    # обратно в RGB
    stego_image_BGR = cv2.cvtColor(stego_image, cv2.COLOR_YCR_CB2BGR)
    # обрезаем значение цвета от 0-255
    final_stego_image = np.uint8(np.clip(stego_image_BGR, 0, 255))
    cv2.imwrite(stego_image_filepath, final_stego_image)
    print("Embeded message: ", test_message)

    #--------Извлечение--------
    stego_image = cv2.imread(stego_image_filepath, flags=cv2.IMREAD_COLOR)
    stego_image_f32 = np.float32(stego_image)
    stego_image_YCC = img.YCC_Image(cv2.cvtColor(stego_image_f32, cv2.COLOR_BGR2YCrCb))
    # DCT
    dct_blocks = [cv2.dct(block) for block in stego_image_YCC.channels[0]] 

    # квантовизация
    dct_quants = [np.around(np.divide(item, img.JPEG_STD_LUM_QUANT_TABLE)) for item in dct_blocks]

    # зигзаг
    sorted_coefficients = [zz.zigzag(block) for block in dct_quants]

    # извлечение данных
    recovered_data = stego.extract_data_from_DCT(sorted_coefficients)
    recovered_data.pos = 0

    # определение длинны
    data_len = int(recovered_data.read('uint:32') / 8)

    extracted_data = bytes()
    for _ in range(data_len):
        extracted_data += struct.pack('>B', recovered_data.read('uint:8'))
    decoded_message=extracted_data.decode('ascii')

    print("Extracted message: ",extracted_data.decode('ascii'))