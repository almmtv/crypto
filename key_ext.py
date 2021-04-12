# функция, преобразующая текст в бинарный вид
def letter_to_binary(string):
    result_string = ''
    for letter in string:
        letter = format(ord(letter), 'b')
        while len(letter) < 7:
            letter = '0' + letter
        result_string += letter
    return result_string


# функция расширения ключа
def key_extension(first_key_56):
    key_64 = ''
    list_key = []
    for i in range(8):
        list_key += [first_key_56[i*7: (i+1)*7]]
    for i in list_key:
        key_64 += i
        if i.count('1') % 2 != 0:
            key_64 += '0'
        else:
            key_64 += '1'
    return key_64


key = input('Введите ключ ')
binary_key = letter_to_binary(key)
while len(binary_key) != 56:
    print('Неверная длина ключа')
    key = input('Введите ключ ')
    binary_key = letter_to_binary(key)
extension_key = key_extension(letter_to_binary(key))
result = []
for j in range(8):
    result += [extension_key[:8]]
    extension_key = extension_key[8:]
result_16 = ''
for element in result:
    element = str(hex(int(element, base=2)))[2:].upper()
    while len(element) != 2:
        element = '0' + element
    result_16 += element + ' '
print('Результат:', result_16)

