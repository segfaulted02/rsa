# rsa
RSA key generation, encryption, and decryption implementation

Uses the Solovay-Strassen primality test to determine if a number is prime in a reasonable time, given user input of a particular bit size and number of trials to ensure high confidence of a prime number. Jacobi symbols are used to assist in determining primality.

Given a plaintext and the keys generated, can also be used to encrypt a message and decrypt a message.

Splits plaintext into 214 byte blocks, which can be adjusted, and although is not the best way to implement RSA, it is a convenient, simplistic way to implement RSA in an effective manner.

Limitations of this program stem from the size of the byte blocks. Currently, it is set to 214 byte blocks, and due to this, the program has difficulty decrypting messages with an private key of less than ~512 bits. Ensure you are creating keys of at least 512 bits so that you can successfully decode and encode your message.
