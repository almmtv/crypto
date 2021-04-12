# функция, преобразующая hex в бинарный вид
def hex_to_binary(string):
    result_s_16 = ''
    result_string = ''
    for i in string.split():
        try:
            letter = int(i, base=16)
        except ValueError:
            print('Введено неверное значение')
            break
        letter = format(letter, 'b')
        while len(letter) < 8:
            letter = '0' + letter
        result_string += letter
    return result_string


# функция, выполняющая перестановку
def permutation(string, table):
    result_string = ''
    for i in range(len(table)):
        result_string += string[table[i] - 1]
    return result_string


# функция, выполняющая побитовое сложение по модулю 2
def xor_func(first_string, second_string):
    result_string = ''
    for i in range(len(first_string)):
        result_string += str(int(first_string[i]) ^ int(second_string[i]))
    return result_string


# функция преобразования S
def transformation_s(string):
    b = []
    result_string = ''
    for num in range(8):
        sta = int((string[num * 6] + string[(num + 1) * 6 - 1]), base=2)
        stb = int(string[num * 6 + 1:(num + 1) * 6 - 1], base=2)
        b += [S[num][sta][stb]]
    for num in b:
        num = format(num, 'b')
        while len(num) < 4:
            num = '0' + num
        result_string += num
    return result_string


# функция циклического сдвига
def shift(string, steps):
    result_string = string[steps:] + string[:steps]
    return result_string


# Блоки, необходимые для шифрования сообщения
T0 = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]

T1 = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
      38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
      36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
      34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]

E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

S1 = [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
      [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
      [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
      [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]]

S2 = [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
      [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
      [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
      [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]]

S3 = [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
      [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
      [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
      [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]]

S4 = [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
      [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
      [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
      [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]]

S5 = [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
      [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
      [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
      [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]]

S6 = [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
      [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
      [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
      [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]]

S7 = [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
      [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
      [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
      [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]]

S8 = [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
      [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
      [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
      [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]

S = [S1, S2, S3, S4, S5, S6, S7, S8]

P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

C = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
     10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36]

D = [63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
     14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]

Sdv = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

K = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4,
     26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40,
     51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]

encrypt_decrypt = str(input('Если вы хотите расшифровать сообщение - введите 0\nЕсли хотите зашифровать сообщение - '
                            'введите 1\n'))
while (encrypt_decrypt != '0') and (encrypt_decrypt != '1'):
    print('Неправильно введён режим шифрования')
    encrypt_decrypt = str(input('Если вы хотите расшифровать сообщение - введите 0\nЕсли хотите зашифровать сообщение '
                                '- введите 1\n'))
message = input('Введите сообщение ')
key = input('Введите ключ ')
message = hex_to_binary(message)
key = hex_to_binary(key)
while len(key) != 64:
    print(len(key))
    print('Неверная длина ключа')
    key = input('Введите ключ ')
    key = hex_to_binary(key)
number_of_segments = len(message) // 64
length_of_the_last_one = len(message) % 64
list_of_segments = []
# Разбиваем сообщение на блоки, для шифрования в режиме электронной кодовой книги
for number in range(number_of_segments):
    segment = message[number*64: (number+1)*64]
    list_of_segments += [segment]
# последний блок, в котором меньше 64 бит, заполняем нулями
if length_of_the_last_one != 0:
    last_segment = message[-length_of_the_last_one:] + (64 - length_of_the_last_one) * '0'
    list_of_segments += [last_segment]
# Производим генерацию ключей
list_of_keys = []
extension_key = key
c = []
c += [permutation(extension_key, C)]
d = []
d += [permutation(extension_key, D)]
for key_i in range(16):
    c += [shift(c[key_i], Sdv[key_i])]
    d += [shift(d[key_i], Sdv[key_i])]
    key_0 = c[key_i + 1] + d[key_i + 1]
    key_1 = permutation(key_0, K)
    list_of_keys += [key_1]
# Шифруем сообщение
list_of_encrypted_segments = []
for segment in list_of_segments:
    t = permutation(segment, T0)
    L = []
    L += [t[0:32]]
    R = []
    R += [t[32:]]
    for cycle in range(16):
        if encrypt_decrypt == '0':
            current_key = list_of_keys[15 - cycle]
        else:
            current_key = list_of_keys[cycle]
        e = permutation(R[cycle], E)
        B = xor_func(e, current_key)
        s = transformation_s(B)
        p = permutation(s, P)
        L += [R[cycle]]
        R += [xor_func(L[cycle], p)]
    encrypted_segment = R[16] + L[16]
    t = permutation(encrypted_segment, T1)
    list_of_encrypted_segments += [t]
# Выводим сообщение
result = []
for segment in list_of_encrypted_segments:
    for j in range(8):
        result += [segment[:8]]
        segment = segment[8:]
result_16 = ''
for element in result:
    element = str(hex(int(element, base=2)))[2:].upper()
    while len(element) != 2:
        element = '0' + element
    result_16 += element + ' '
print('Результат:', result_16)