# функция, дописывающая нули в начало строки, пока её длина не станет равна 8
def len_8(string):
    while len(string) < 8:
        string = '0' + string
    return string


# функция, преобразующая hex в бинарный вид
def hex_to_binary(string):
    result_string = ''
    for i in string.split():
        try:
            symbol = int(i, base=16)
        except ValueError:
            print('Введено неверное значение')
            break
        symbol = format(symbol, 'b')
        symbol = len_8(symbol)
        result_string += symbol
    return result_string


# функция исключающего или
def xor_func(first_string, second_string):
    result_string = ''
    for i in range(len(first_string)):
        result_string += str(int(first_string[i]) ^ int(second_string[i]))
    return result_string


# функция, выполняющая проверку принадлежит ли многочлен полю GF(2^8) и возвращающая элемент, принадлежащий полю GF(2^8)
def mgl(byte):
    if byte[0] != '0':
        result_byte = xor_func(byte, '100011011')
    else:
        result_byte = byte
    result_byte = result_byte[1:]
    return result_byte


# функция умножения на 1
def mul_01(byte):
    return byte


# функция умножения на 2
def mul_02(byte):
    result_byte = byte + '0'
    result_byte = mgl(result_byte)
    return result_byte


# функция умножения на 3
def mul_03(byte):
    result_byte = xor_func('0' + byte, byte + '0')
    result_byte = mgl(result_byte)
    return result_byte


# функция умножения на 9
def mul_09(byte):
    result_byte = xor_func(mul_02(mul_02(mul_02(byte))), mul_01(byte))
    return result_byte


# функция умножения на b
def mul_0b(byte):
    result_byte = xor_func(mul_02(mul_02(mul_02(byte))), mul_03(byte))
    return result_byte


# функция умножения на d
def mul_0d(byte):
    result_byte = xor_func(xor_func(mul_02(mul_02(mul_02(byte))), mul_02(mul_02(byte))), mul_01(byte))
    return result_byte


# функция умножения на e
def mul_0e(byte):
    result_byte = xor_func(xor_func(mul_02(mul_02(mul_02(byte))), mul_02(mul_02(byte))), mul_02(byte))
    return result_byte


# функция, выполняющая циклический сдвиг с заданным шагом
def shift(lst, step):
    result_list = []
    result_list += lst[step:] + lst[:step]
    return result_list


# преобразование SubBytes и InvSubBytes
def sub_bytes(array, mode):
    if mode == '0':
        S = S_box
    else:
        S = InvSbox
    result_array = [[] for x in range(4)]
    for i in range(4):
        for j in range(4):
            a = int(array[i][j][:4], base=2)
            b = int(array[i][j][4:], base=2)
            num = format(int(S[a][b], base=16), 'b')
            num = len_8(num)
            result_array[i].append(num)
    return result_array


# преобразование ShiftRows
def shift_rows(array, mode):
    result_array = [[] for x in range(4)]
    for i in range(4):
        if mode == '0':
            result_array[i] += shift(array[i], i)
        else:
            result_array[i] += shift(array[i], -i)
    return result_array


# преобразование MixColumns
def mix_columns(array, mode):
    result_array = [[] for x in range(4)]
    if mode == '0':
        for i in range(4):
            result_array[0].append(xor_func(xor_func(xor_func(mul_02(array[0][i]), mul_03(array[1][i])),
                                                     mul_01(array[2][i])), mul_01(array[3][i])))
            result_array[1].append(xor_func(xor_func(xor_func(mul_01(array[0][i]), mul_02(array[1][i])),
                                                     mul_03(array[2][i])), mul_01(array[3][i])))
            result_array[2].append(xor_func(xor_func(xor_func(mul_01(array[0][i]), mul_01(array[1][i])),
                                                     mul_02(array[2][i])), mul_03(array[3][i])))
            result_array[3].append(xor_func(xor_func(xor_func(mul_03(array[0][i]), mul_01(array[1][i])),
                                                     mul_01(array[2][i])), mul_02(array[3][i])))
        else:
            for i in range(4):
                result_array[0].append(xor_func(xor_func(xor_func(mul_0e(array[0][i]), mul_0b(array[1][i])),
                                                         mul_0d(array[2][i])), mul_09(array[3][i])))
                result_array[1].append(xor_func(xor_func(xor_func(mul_09(array[0][i]), mul_0e(array[1][i])),
                                                         mul_0b(array[2][i])), mul_0d(array[3][i])))
                result_array[2].append(xor_func(xor_func(xor_func(mul_0d(array[0][i]), mul_09(array[1][i])),
                                                         mul_0e(array[2][i])), mul_0b(array[3][i])))
                result_array[3].append(xor_func(xor_func(xor_func(mul_0b(array[0][i]), mul_0d(array[1][i])),
                                                         mul_09(array[2][i])), mul_0e(array[3][i])))
        return result_array


def add_round_key(array, num):
    result_array = [[] for x in range(4)]
    for m in range(4):
        for p in range(4):
            result_array[m].append(xor_func(array[m][p], list_round_key[num][m][p]))
    return result_array


# функция, преобразующая список в строку
def list_to_string(list1):
    result_string = ''
    for i in list1:
        result_string += i
    return result_string


# функция, преобразующая строку в список с заданным количеством элементов
def string_to_list(string1, num):
    result_list = []
    step = len(string1) // num
    for i in range(num):
        result_list += [string1[0:step]]
        string1 = string1[step:]
    return result_list


# функция SubBytes для генерации раундовых ключей
def sub_bytes_key(lis):
    result_state = []
    for i in range(4):
        a = int(lis[i][:4], base=2)
        b = int(lis[i][4:], base=2)
        num = format(int(S_box[a][b], base=16), 'b')
        while len(num) < 8:
            num = '0' + num
        result_state.append(num)
    return result_state


# функция g для генерации раундовых ключей
def g(word, rnd):
    result_word = shift(word, 1)
    result_word = sub_bytes_key(result_word)
    rc = format(int(Rc[rnd], base=16), 'b')
    rc = len_8(rc)
    result_word = xor_func(rc, result_word[0]) + list_to_string(result_word)[8:]
    return result_word


# функция генерации раундовых ключей
def key_ex(words):
    for i in range(10):
        words += [string_to_list(xor_func(list_to_string(words[4*i]), g(words[4*i+3], i)), 4)]
        words += [string_to_list(xor_func(list_to_string(words[4*i+1]), list_to_string(words[4*i+4])), 4)]
        words += [string_to_list(xor_func(list_to_string(words[4*i+2]), list_to_string(words[4*i+5])), 4)]
        words += [string_to_list(xor_func(list_to_string(words[4*i+3]), list_to_string(words[4*i+6])), 4)]
    round_key = [[[] for y in range(4)] for x in range(11)]
    for i in range(11):
        for j in range(4):
            for m in range(4):
                round_key[i][m].append(words[4*i + j][m])
    return round_key


# Блоки, необходимые для шифрования сообщения
S_box = [['63', '7c', '77', '7b', 'f2', '6b', '6f', 'c5', '30', '01', '67', '2b', 'fe', 'd7', 'ab', '76'],
         ['ca', '82', 'c9', '7d', 'fa', '59', '47', 'f0', 'ad', 'd4', 'a2', 'af', '9c', 'a4', '72', 'c0'],
         ['b7', 'fd', '93', '26', '36', '3f', 'f7', 'cc', '34', 'a5', 'e5', 'f1', '71', 'd8', '31', '15'],
         ['04', 'c7', '23', 'c3', '18', '96', '05', '9a', '07', '12', '80', 'e2', 'eb', '27', 'b2', '75'],
         ['09', '83', '2c', '1a', '1b', '6e', '5a', 'a0', '52', '3b', 'd6', 'b3', '29', 'e3', '2f', '84'],
         ['53', 'd1', '00', 'ed', '20', 'fc', 'b1', '5b', '6a', 'cb', 'be', '39', '4a', '4c', '58', 'cf'],
         ['d0', 'ef', 'aa', 'fb', '43', '4d', '33', '85', '45', 'f9', '02', '7f', '50', '3c', '9f', 'a8'],
         ['51', 'a3', '40', '8f', '92', '9d', '38', 'f5', 'bc', 'b6', 'da', '21', '10', 'ff', 'f3', 'd2'],
         ['cd', '0c', '13', 'ec', '5f', '97', '44', '17', 'c4', 'a7', '7e', '3d', '64', '5d', '19', '73'],
         ['60', '81', '4f', 'dc', '22', '2a', '90', '88', '46', 'ee', 'b8', '14', 'de', '5e', '0b', 'db'],
         ['e0', '32', '3a', '0a', '49', '06', '24', '5c', 'c2', 'd3', 'ac', '62', '91', '95', 'e4', '79'],
         ['e7', 'c8', '37', '6d', '8d', 'd5', '4e', 'a9', '6c', '56', 'f4', 'ea', '65', '7a', 'ae', '08'],
         ['ba', '78', '25', '2e', '1c', 'a6', 'b4', 'c6', 'e8', 'dd', '74', '1f', '4b', 'bd', '8b', '8a'],
         ['70', '3e', 'b5', '66', '48', '03', 'f6', '0e', '61', '35', '57', 'b9', '86', 'c1', '1d', '9e'],
         ['e1', 'f8', '98', '11', '69', 'd9', '8e', '94', '9b', '1e', '87', 'e9', 'ce', '55', '28', 'df'],
         ['8c', 'a1', '89', '0d', 'bf', 'e6', '42', '68', '41', '99', '2d', '0f', 'b0', '54', 'bb', '16']]

InvSbox = [['52', '09', '6a', 'd5', '30', '36', 'a5', '38', 'bf', '40', 'a3', '9e', '81', 'f3', 'd7', 'fb'],
           ['7c', 'e3', '39', '82', '9b', '2f', 'ff', '87', '34', '8e', '43', '44', 'c4', 'de', 'e9', 'cb'],
           ['54', '7b', '94', '32', 'a6', 'c2', '23', '3d', 'ee', '4c', '95', '0b', '42', 'fa', 'c3', '4e'],
           ['08', '2e', 'a1', '66', '28', 'd9', '24', 'b2', '76', '5b', 'a2', '49', '6d', '8b', 'd1', '25'],
           ['72', 'f8', 'f6', '64', '86', '68', '98', '16', 'd4', 'a4', '5c', 'cc', '5d', '65', 'b6', '92'],
           ['6c', '70', '48', '50', 'fd', 'ed', 'b9', 'da', '5e', '15', '46', '57', 'a7', '8d', '9d', '84'],
           ['90', 'd8', 'ab', '00', '8c', 'bc', 'd3', '0a', 'f7', 'e4', '58', '05', 'b8', 'b3', '45', '06'],
           ['d0', '2c', '1e', '8f', 'ca', '3f', '0f', '02', 'c1', 'af', 'bd', '03', '01', '13', '8a', '6b'],
           ['3a', '91', '11', '41', '4f', '67', 'dc', 'ea', '97', 'f2', 'cf', 'ce', 'f0', 'b4', 'e6', '73'],
           ['96', 'ac', '74', '22', 'e7', 'ad', '35', '85', 'e2', 'f9', '37', 'e8', '1c', '75', 'df', '6e'],
           ['47', 'f1', '1a', '71', '1d', '29', 'c5', '89', '6f', 'b7', '62', '0e', 'aa', '18', 'be', '1b'],
           ['fc', '56', '3e', '4b', 'c6', 'd2', '79', '20', '9a', 'db', 'c0', 'fe', '78', 'cd', '5a', 'f4'],
           ['1f', 'dd', 'a8', '33', '88', '07', 'c7', '31', 'b1', '12', '10', '59', '27', '80', 'ec', '5f'],
           ['60', '51', '7f', 'a9', '19', 'b5', '4a', '0d', '2d', 'e5', '7a', '9f', '93', 'c9', '9c', 'ef'],
           ['a0', 'e0', '3b', '4d', 'ae', '2a', 'f5', 'b0', 'c8', 'eb', 'bb', '3c', '83', '53', '99', '61'],
           ['17', '2b', '04', '7e', 'ba', '77', 'd6', '26', 'e1', '69', '14', '63', '55', '21', '0c', '7d']]

Rc = ['01', '02', '04', '08', '10', '20', '40', '80', '1b', '36']

en_de = str(input('Если хотите зашифровать сообщение - введите 0\nЕсли вы хотите расшифровать сообщение - введите 1\n'))
while (en_de != '0') and (en_de != '1'):
    print('Неправильно введён режим шифрования')
    en_de = str(input('Если хотите зашифровать сообщение - введите 0\nЕсли вы хотите расшифровать сообщение'
                      ' - введите 1\n'))
message = input('Введите сообщение ')
key = input('Введите ключ ')
message = hex_to_binary(message)
key = hex_to_binary(key)
while len(key) != 128:
    print(len(key))
    print('Неверная длина ключа')
    key = input('Введите ключ ')
    key = hex_to_binary(key)
number_of_segments = len(message) // 128  # показывает количество целых 128-битных сегментов
length_of_the_last_one = len(message) % 128
list_of_segments = []
# Разбиваем сообщение на блоки, для шифрования в режиме электронной кодовой книги
for number in range(number_of_segments):
    segment = message[number*128: (number+1)*128]
    list_of_segments += [segment]
# Последний блок заполняем нулями, чтобы символов в блоке стало 128
if length_of_the_last_one != 0:
    last_segment = message[-length_of_the_last_one:] + (128 - length_of_the_last_one) * '0'
    list_of_segments += [last_segment]
key = string_to_list(key, 16)
key_list = []
for k in range(4):
    key_list += [key[4*k:4*k+4]]
list_round_key = key_ex(key_list)
if en_de == '1':
    list_round_key = list_round_key[::-1]
out = []
for segment in list_of_segments:
    message = string_to_list(segment, 16)
    # Записываем принятое сообщение в массив State
    state = [[] for x in range(4)]
    for r in range(4):
        for c in range(4):
            state[r].append(message[r + 4*c])
    # Выполняем преобразование AddRoundKey, используя нулевой раундовый ключ
    state = add_round_key(state, 0)
    # Выполняем 10 раундовых преобразований
    for rou in range(10):
        if en_de == '0':
            state = sub_bytes(state, en_de)
            state = shift_rows(state, en_de)
            if rou != 9:  # Особое условие для последнего раунда
                state = mix_columns(state, en_de)
            state = add_round_key(state, rou + 1)
        else:
            state = shift_rows(state, en_de)
            state = sub_bytes(state, en_de)
            state = add_round_key(state, rou + 1)
            if rou != 9:  # Особое условие для последнего раунда
                state = mix_columns(state, en_de)
    # Записываем шифротекст в out по правилу out[r+4c]=state[r][c]
    for n in range(4):
        out += [state[0][n]] + [state[1][n]] + [state[2][n]] + [state[3][n]]
# Выводим результат
result = ''
for element in out:
    element = str(hex(int(element, base=2)))[2:].upper()
    while len(element) != 2:
        element = '0' + element
    result += element + ' '
print('Результат:', result)
