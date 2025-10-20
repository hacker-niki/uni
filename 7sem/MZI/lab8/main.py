import streamlit as st
import cv2
import numpy as np
import itertools
from PIL import Image

# Таблица квантования для DCT
quant = np.array([[16,11,10,16,24,40,51,61],
                    [12,12,14,19,26,58,60,55],
                    [14,13,16,24,40,57,69,56],
                    [14,17,22,29,51,87,80,62],
                    [18,22,37,56,68,109,103,77],
                    [24,35,55,64,81,104,113,92],
                    [49,64,78,87,103,121,120,101],
                    [72,92,95,98,112,100,103,99]])

class DCT():
    def __init__(self):
        self.message = None
        self.bitMess = None
        self.oriCol = 0
        self.oriRow = 0
        self.numBits = 0

    def encode_image(self,img,secret_msg):
        secret=secret_msg
        self.message = str(len(secret))+'*'+secret
        self.bitMess = self.toBits()
        row,col = img.shape[:2]
        self.oriRow, self.oriCol = row, col
        if((col/8)*(row/8)<len(secret)):
            st.error("Ошибка: Сообщение слишком велико для кодирования в изображении")
            return None

        if row%8 != 0 or col%8 != 0:
            img = self.addPadd(img, row, col)

        row,col = img.shape[:2]
        bImg,gImg,rImg = cv2.split(img)
        bImg = np.float32(bImg)
        imgBlocks = [np.round(bImg[j:j+8, i:i+8]-128) for (j,i) in itertools.product(range(0,row,8),
                                                                       range(0,col,8))]
        dctBlocks = [np.round(cv2.dct(img_Block)) for img_Block in imgBlocks]
        quantizedDCT = [np.round(dct_Block/quant) for dct_Block in dctBlocks]
        messIndex = 0
        letterIndex = 0
        for quantizedBlock in quantizedDCT:
            DC = quantizedBlock[0][0]
            DC = np.uint8(DC)
            DC = np.unpackbits(DC)
            DC[7] = self.bitMess[messIndex][letterIndex]
            DC = np.packbits(DC)
            DC = np.float32(DC)
            DC= DC-255
            quantizedBlock[0][0] = DC
            letterIndex = letterIndex+1
            if letterIndex == 8:
                letterIndex = 0
                messIndex = messIndex + 1
                if messIndex == len(self.message):
                    break

        sImgBlocks = [quantizedBlock *quant for quantizedBlock in quantizedDCT]
        sImgBlocks = [cv2.idct(B)+128 for B in sImgBlocks]
        sImg=[]
        for chunkRowBlocks in self.chunks(sImgBlocks, col/8):
            for rowBlockNum in range(8):
                for block in chunkRowBlocks:
                    sImg.extend(block[rowBlockNum])
        sImg = np.array(sImg).reshape(row, col)
        sImg = np.uint8(sImg)
        sImg = cv2.merge((sImg,gImg,rImg))
        return sImg

    def decode_image(self,img):
        row,col = img.shape[:2]
        messSize = None
        messageBits = []
        buff = 0
        bImg,gImg,rImg = cv2.split(img)
        bImg = np.float32(bImg)
        imgBlocks = [bImg[j:j+8, i:i+8]-128 for (j,i) in itertools.product(range(0,row,8),
                                                                       range(0,col,8))]
        dctBlocks = [cv2.dct(img_Block) for img_Block in imgBlocks]
        quantizedDCT = [dct_Block/quant for dct_Block in dctBlocks]
        i=0
        for quantizedBlock in quantizedDCT:
            DC = quantizedBlock[0][0]
            DC = np.uint8(DC)
            DC = np.unpackbits(DC)
            if DC[7] == 1:
                buff+=(0&1) << (7-i)
            elif DC[7] == 0:
                buff+=(1&1) << (7-i)
            i=1+i
            if i == 8:
                messageBits.append(chr(buff))
                buff = 0
                i =0
                if messageBits[-1] == '*' and messSize is None:
                    try:
                        messSize = int(''.join(messageBits[:-1]))
                    except:
                        pass
            if len(messageBits) - len(str(messSize)) - 1 == messSize:
                return ''.join(messageBits)[len(str(messSize))+1:]
        return ''

    def chunks(self, l, n):
        m = int(n)
        for i in range(0, len(l), m):
            yield l[i:i + m]

    def addPadd(self,img, row, col):
        img = cv2.resize(img,(col+(8-col%8),row+(8-row%8)))
        return img

    def toBits(self):
        bits = []
        for char in self.message:
            binval = bin(ord(char))[2:].rjust(8,'0')
            bits.append(binval)
        self.numBits = bin(len(bits))[2:].rjust(8,'0')
        return bits

class LSB():
    def encode_image(self,img, msg):
        length = len(msg)
        if length > 255:
            st.error("Текст слишком длинный! (не более 255 символов)")
            return None
        encoded = img.copy()
        width, height = img.size
        index = 0
        for row in range(height):
            for col in range(width):
                if img.mode != 'RGB':
                    r, g, b ,a = img.getpixel((col, row))
                elif img.mode == 'RGB':
                    r, g, b = img.getpixel((col, row))

                if row == 0 and col == 0 and index < length:
                    asc = length
                elif index <= length:
                    c = msg[index -1]
                    asc = ord(c)
                else:
                    asc = b
                encoded.putpixel((col, row), (r, g , asc))
                index += 1
        return encoded

    def decode_image(self,img):
        width, height = img.size
        msg = ""
        index = 0
        for row in range(height):
            for col in range(width):
                if img.mode != 'RGB':
                    r, g, b ,a = img.getpixel((col, row))
                elif img.mode == 'RGB':
                    r, g, b = img.getpixel((col, row))
                if row == 0 and col == 0:
                    length = b
                elif index <= length:
                    msg += chr(b)
                index += 1
        return msg

def main():
    st.title("Стеганография: DCT и LSB")

    option = st.sidebar.selectbox("Выберите опцию", ("Зашифровать", "Дешифровать"))

    if option == "Зашифровать":
        st.header("Зашифровать сообщение в изображении")
        image_file = st.file_uploader("Загрузите изображение", type=['png', 'jpg', 'jpeg', 'bmp'])
        secret_message = st.text_area("Введите секретное сообщение")
        method = st.selectbox("Выберите метод", ("LSB", "DCT"))

        if st.button("Зашифровать"):
            if image_file is not None and secret_message:
                if method == "LSB":
                    original_image = Image.open(image_file)
                    encoder = LSB()
                    encoded_image = encoder.encode_image(original_image, secret_message)
                    if encoded_image:
                        st.image(encoded_image, caption="Зашифрованное изображение", use_column_width=True)
                        encoded_image.save("encoded_lsb_image.png")
                        with open("encoded_lsb_image.png", "rb") as file:
                            st.download_button(
                                label="Скачать зашифрованное изображение",
                                data=file,
                                file_name="encoded_lsb_image.png",
                                mime="image/png"
                            )
                elif method == "DCT":
                    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
                    original_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                    encoder = DCT()
                    encoded_image = encoder.encode_image(original_image, secret_message)
                    if encoded_image is not None:
                        st.image(cv2.cvtColor(encoded_image, cv2.COLOR_BGR2RGB), caption="Зашифрованное изображение", use_column_width=True)
                        cv2.imwrite("encoded_dct_image.png", encoded_image)
                        with open("encoded_dct_image.png", "rb") as file:
                            st.download_button(
                                label="Скачать зашифрованное изображение",
                                data=file,
                                file_name="encoded_dct_image.png",
                                mime="image/png"
                            )
            else:
                st.warning("Пожалуйста, загрузите изображение и введите сообщение.")

    elif option == "Дешифровать":
        st.header("Дешифровать сообщение из изображения")
        image_file = st.file_uploader("Загрузите зашифрованное изображение", type=['png', 'jpg', 'jpeg', 'bmp'])
        method = st.selectbox("Выберите метод", ("LSB", "DCT"))

        if st.button("Дешифровать"):
            if image_file is not None:
                if method == "LSB":
                    encoded_image = Image.open(image_file)
                    decoder = LSB()
                    decoded_message = decoder.decode_image(encoded_image)
                    st.success("Извлеченное сообщение:")
                    st.write(decoded_message)
                elif method == "DCT":
                    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
                    encoded_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                    decoder = DCT()
                    decoded_message = decoder.decode_image(encoded_image)
                    st.success("Извлеченное сообщение:")
                    st.write(decoded_message)
            else:
                st.warning("Пожалуйста, загрузите изображение.")

if __name__ == "__main__":
    main()
