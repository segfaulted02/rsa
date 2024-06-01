import random
import math

# performs the modular exponentiation
def encrypt_decrypt_block(block, e_d, n):
    return pow(block, e_d, n)

# function to encrypt
def encrypt_text(text, n, e, block_size):
    blocks = []
    for i in range(0, len(text), block_size):
        sub_string = text[i:i + block_size]
        byte_block = 0
        multiplier = 1
        for j in range(len(sub_string) - 1, -1, -1):
            byte_block += ord(sub_string[j]) * multiplier
            multiplier *= 256
        cypher_block = encrypt_decrypt_block(byte_block, e, n)
        blocks.append(cypher_block) 
    return blocks

# function to decrypt
def decrypt_text(blocks, d, n):
    message = ''
    for block in blocks:
        decrypted_value = encrypt_decrypt_block(block, d, n)
        sub_byte = decrypted_value.to_bytes((decrypted_value.bit_length() + 7) // 8, byteorder='big')
        message += ''.join(chr(byte) for byte in sub_byte)
    return message

def jacobi(a, m):
    result = 1
    a = a % m
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if m % 8 in [3, 5]:
                result = -result
        a, m = m, a
        if a % 4 == 3 and m % 4 == 3:
            result = -result
        a = a % m
    if m == 1:
        return result
    return 0

def solovay_strassen(n, k):
    for _ in range(k):
        a = random.randint(2, n - 1)
        x = jacobi(a, n)
        y = pow(a, (n - 1) // 2, n)
        if x == 0 or y != x % n:
            return False
    return True

def random_size_integer(bits):
    return random.getrandbits(bits)

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    gcd, x = extended_gcd(a, m)
    if gcd == 1:
        return x % m
    return None

def extended_gcd(a, m):
    old_remainder, remainder = a, m
    old_x, x = 1, 0
    old_y, y = 0, 1
    
    while remainder != 0:
        quotient = old_remainder // remainder
        old_remainder, remainder = remainder, old_remainder - quotient * remainder
        old_x, x = x, old_x - quotient * x
        old_y, y = y, old_y - quotient * y

    return old_remainder, old_x

def generate_keys(bits, k):
    p_attempts = []
    q_attempts = []
    
    p = 0
    q = 0
    
    # finds a prime p using Solovay-Strassen testing
    running = True
    while running:
        test_p = random_size_integer(bits)
        p_attempts.append(test_p)
        if (solovay_strassen(test_p, k)):
            p = test_p
            running = False
    # finds a prime q using Solovay-Strassen testing
    running = True
    while running:
        test_q = random_size_integer(bits)
        q_attempts.append(test_q)
        if (solovay_strassen(test_q, k)):
            q = test_q
            running = False
    
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random_size_integer(bits)
    while (gcd(e, phi) != 1):
        e = random_size_integer(bits)
    d = mod_inverse(e, phi)
    return (p, q, n, e, d, p_attempts, q_attempts)

def main():
    print("Ensure you have a file named 'plaintext.txt' with your text, and another file named 'publickey.txt' which has n on the first line, and e on the second line.")
    print("If you choose to decrypt, ensure there is a file named 'ciphertext.txt' with what to decrypt, and another file named 'privatekey.txt' for the value of n on the first line, and d on the second.")
    print("You may also generate a key, with given bit size, and choose number of trials for increased confidence.")
    choice = input("Decrypt, encrypt, or generate key? Input 'e' , 'd' , or 'g': ")
    
    BLOCK_SIZE = 214
    
    if choice == 'g':
        key_size = int(input("Input key size: "))
        trials = int(input("Input number of trials: "))
        
        print("Generating keys and writing them to 'privatekey.txt' and 'publickey.txt'")
        p, q, n, e, d, p_tries, q_tries = generate_keys(key_size, trials)
        print(f"Value of n: {n}\nValue of p: {p}\nValue of q: {q}")
        print(f"Value of e: {e}\nValue of d: {d}")
        print(f"Confidence level given your key size and trials: {1 - ((key_size * math.log(2) - 2)/(key_size * math.log(2) - 2 + 2 ** (trials+1)))}")
        print(f"Generated p with {len(p_tries)} attempts and q with {len(q_tries)} attempts")
        
        # writing to files
        with open('publickey.txt', 'w') as file:
            file.write('\n'.join(map(str, (n, e))))
    
        with open('privatekey.txt', 'w') as file:
            file.write('\n'.join(map(str, (n, d))))
        
    elif choice == 'e':
        plaintext = open('plaintext.txt', 'r').read()
        
        keys = open('publickey.txt', 'r').readlines()
        n = int(keys[0].strip())
        e = int(keys[1].strip())
        
        encrypted_blocks = encrypt_text(plaintext, n, e, BLOCK_SIZE)
        
        with open('ciphertext.txt', 'w') as file:
            for block in encrypted_blocks:
                file.write(f"{block}\n")
        
        print("\nEncrypted blocks:")
        for block in encrypted_blocks:
            print(f"{block}\n")
        
        print("Encryption also written to 'ciphertext.txt'")
        
    elif choice == 'd':
        with open('ciphertext.txt', 'r') as file:
            encrypted_blocks = [int(line.strip()) for line in file]
        
        keys = open('privatekey.txt', 'r').readlines()
        n = int(keys[0].strip())
        d = int(keys[1].strip())
        
        decrypted_text = decrypt_text(encrypted_blocks, d, n)
        
        print("\nDecrypted:")
        print(decrypted_text)
        
    else:
        print("Nothing was chosen")
    
if __name__ == '__main__':
    main()