import numpy as np

def main():
    global hill_cipher_key
    hill_cipher_key = "REFCVMDJL" # 9 character of key for making square matrix 3x3
    # Contoh Key yang tidak memiliki multiplikasi invers (PLDKJCCMN),(AGSMNDLKK)
    # Contoh Key yang memiliki multiplikasi invers (ALPHABETA), (REFCVMDJL), (HOICVMDJL)
    determinant_value = determinant(hill_cipher_key)
    print("Determinan Key:", determinant_value)
    chooseMenu()

def chooseMenu():
    # print("Key = " + hill_cipher_key) # Command this line ini jika tidak ingin melihat key
    while True:
        determinant_value = determinant(hill_cipher_key)
        is_invertible,inverse_multiplication = checkMultiplicative(determinant_value)
        if is_invertible:
            input_menu = int(input('Masukkan Pilihan Menu (1 untuk Enkripsi dan 2 untuk Dekripsi): '))
            if input_menu == 1:
                # keyMatrix() # Command line ini jika tidak ingin melihat key
                input_plain = input('Masukkan Plain Text: ')
                input_plain = input_plain.replace(' ', '_')
                separate(input_plain, 3) # Memisahkan input (plain teks) setiap 3 karakter dengan spasi
                # print(separated_string)
                integer_list = StringToInt(separated_string) # Mengubah string input menjadi bentuk integer. A=0, Z=25, _=26
                matrix_int_list = splitIntList(integer_list, 3) # Membagi string yang sudah diubah menjadi partisi setiap 3 karakter
                # print(matrix_int_list)
                encrypted_matrix = encrypt(matrix_int_list)
                # print("Encrypted Matrix:")
                # print(encrypted_matrix)
                encrypted_text = IntToString(encrypted_matrix)
                print("Encrypted Text:")
                print(encrypted_text)
                
                break
            elif input_menu == 2:
                # keyMatrix() # Command line ini jika tidak ingin melihat key
                input_cipher = input('Masukkan Cipher Teks: ')
                separate(input_cipher, 3) # Memisahkan input (plain teks) setiap 3 karakter dengan spasi
                # print(separated_string)
                integer_list = StringToInt(separated_string)
                matrix_int_list = splitIntList(integer_list, 3)
                # print(matrix_int_list)
                determinant_value = determinant(hill_cipher_key)
                # print(determinant_value)
                adjoint_matrix = calculateAdjointMatrix()
                # print(adjoint_matrix)
                inverse_multiplication = pow(determinant_value, -1, 27)
                # print(inverse_multiplication)
                decrypted_matrix = decrypt(matrix_int_list, inverse_multiplication, adjoint_matrix)
                # print("Decrypted Matrix:")
                # print(decrypted_matrix)
                decrypted_text = IntToString(decrypted_matrix)
                decrypted_text = decrypted_text.replace("_"," ")
                print("Decrypted Text:")
                print(decrypted_text)
                break
            else:
                print("Pilihan tidak valid. Harap masukkan 1 atau 2.")
        else:
            print("Gunakan Key Lain, Key ini tidak memiliki Multiplicative Invers")
            break
        
# Optional - Untuk mengetahui bentuk integer dari key
# def keyMatrix():
#     print("KEY:")
#     key_as_int = []
#     for char in hill_cipher_key:
#         if char == ' ':
#             key_as_int.append(26)
#         else:
#             key_as_int.append(ord(char) - ord('A'))
#     for i in range(0, 9, 3):
#         print(hill_cipher_key[i:i+3] + " >>> " + str(key_as_int[i:i+3]))

# Memisahkan input menjadi beberapa bagian sesuai dengan ukuran key
def separate(string, length):
    global separated_string
    while len(string) % length != 0:
        string += '_'
    separated_string =  ' '.join(string[i:i+length] for i in range(0,len(string),length))
    
    return separated_string

def StringToInt(input_string):
    integer_list = []
    for char in input_string:
        if 'A' <= char <= 'Z':
            value = ord(char) - ord('A')
        elif 'a' <= char <= 'z':
            value = ord(char) - ord('a')
        elif char == '_':
            value = 26
        else:
            continue
        integer_list.append(value)
    return integer_list

def IntToString(int_list):
    result = ''
    for num in int_list:
        if num == 26:
            result += '_'
        else:
            result += chr(num + ord('A'))
    return result

def splitIntList(input_list, chunk_size):
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]

def encrypt(matrix_int_list):
    key_matrix = getKeyMatrix()
    encrypted_matrix = []

    for block in matrix_int_list:
        encrypted_block = np.dot(key_matrix, np.array(block).reshape(3, 1))
        encrypted_block = (encrypted_block % 27).flatten()
        encrypted_matrix.extend(encrypted_block)

    return encrypted_matrix

def decrypt(matrix_int_list, inverse_multiplication, adj_matrix):
    decrypted_matrix = []

    for block in matrix_int_list:
        decrypted_block = np.dot(inverse_multiplication, np.dot(adj_matrix, np.array(block).reshape(3, 1)))
        decrypted_block = (decrypted_block % 27).flatten()
        decrypted_matrix.extend(decrypted_block)

    return decrypted_matrix

def determinant(key_matrix):
    key_matrix = getKeyMatrix()
    determinant = np.linalg.det(key_matrix)
    return round(determinant)

def calculateAdjointMatrix():
    key_matrix = getKeyMatrix()
    cofactor_matrix = calculateCofactorMatrix(key_matrix)
    adjoint_matrix = cofactor_matrix.T 
    return adjoint_matrix

def calculateCofactorMatrix(matrix):
    n = matrix.shape[0]
    cofactor_matrix = np.zeros_like(matrix)

    for i in range(n):
        for j in range(n):
            minor = np.delete(np.delete(matrix, i, axis=0), j, axis=1)
            cofactor_matrix[i, j] = ((-1) ** (i + j)) * round(np.linalg.det(minor))

    return cofactor_matrix

def checkMultiplicative(determinant_value):
    try:
        inverse_multiplication = pow(determinant_value, -1, 27)
        return True, inverse_multiplication
    except ValueError:
        return False, None

def getKeyMatrix():
    key_matrix = []
    for char in hill_cipher_key:
        if char == ' ':
            key_matrix.append(26)
        else:
            key_matrix.append(ord(char) - ord('A'))
    return np.array(key_matrix).reshape(3, 3)

if __name__ == "__main__":
    main()

