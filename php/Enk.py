from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

# Fungsi untuk enkripsi simetris dengan padding
def encrypt_message(algorithm, key, message):
    backend = default_backend()
    if algorithm == 'AES':
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    elif algorithm == 'DES':
        cipher = Cipher(algorithms.TripleDES(key), modes.ECB(), backend=backend)
    else:
        raise ValueError(f"Algoritma {algorithm} tidak dikenali.")
    
    # Tambahkan padding pada pesan agar panjangnya kelipatan dari ukuran blok (16 byte untuk AES)
    padder = padding.PKCS7(128).padder()  # 128 bit = 16 byte
    padded_data = padder.update(message.encode()) + padder.finalize()

    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return ciphertext

# Fungsi untuk dekripsi simetris dengan padding removal
def decrypt_message(algorithm, key, ciphertext):
    backend = default_backend()
    if algorithm == 'AES':
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    elif algorithm == 'DES':
        cipher = Cipher(algorithms.TripleDES(key), modes.ECB(), backend=backend)
    else:
        raise ValueError(f"Algoritma {algorithm} tidak dikenali.")
    
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Hapus padding dari pesan yang didekripsi
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    
    return unpadded_data.decode()

# Fungsi untuk menangani input
def process_input():
    # Input pesan dan kunci dari pengguna
    message = input("Masukkan Pesan: ")
    key = input("Masukkan Kunci (16 byte untuk AES, 24 byte untuk DES): ").encode()
    algorithm = input("Pilih Algoritma (AES/DES): ").upper()  # Membuat algoritma selalu uppercase
    action = input("Pilih Aksi (Encrypt/Decrypt): ").capitalize()

    # Validasi panjang kunci
    if len(key) != 16 and algorithm == 'AES':
        print("Error: Kunci untuk AES harus 16 byte")
        return
    if len(key) != 24 and algorithm == 'DES':
        print("Error: Kunci untuk DES harus 24 byte")
        return

    # Proses enkripsi atau dekripsi
    try:
        if action == 'Encrypt':
            result = encrypt_message(algorithm, key, message)
            print(f"Hasil Enkripsi (hex): {result.hex()}")
        elif action == 'Decrypt':
            # Mengasumsikan input ciphertext dalam bentuk hex saat dekripsi
            result = decrypt_message(algorithm, key, bytes.fromhex(message))
            print(f"Hasil Dekripsi: {result}")
        else:
            print("Aksi tidak valid. Pilih 'Encrypt' atau 'Decrypt'.")
    except ValueError as e:
        print(f"Error: {e}")

# Jalankan simulasi
process_input()
