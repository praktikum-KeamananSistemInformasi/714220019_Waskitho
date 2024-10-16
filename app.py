from flask import Flask, request, jsonify, send_from_directory
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

app = Flask(__name__)

# Fungsi untuk enkripsi
def encrypt_message(algorithm, key, message, mode='ECB', iv=None):
    backend = default_backend()

    # Pemilihan algoritma dan mode
    if algorithm == 'AES':
        cipher_algorithm = algorithms.AES(key)
    elif algorithm == 'DES':
        cipher_algorithm = algorithms.TripleDES(key)
    elif algorithm == 'Blowfish':
        cipher_algorithm = algorithms.Blowfish(key)
    elif algorithm == 'ChaCha20':
        if iv is None:
            raise ValueError("ChaCha20 membutuhkan nonce/iv.")
        cipher_algorithm = algorithms.ChaCha20(key, iv)
    elif algorithm == 'Camellia':
        cipher_algorithm = algorithms.Camellia(key)
    else:
        raise ValueError(f"Algoritma {algorithm} tidak dikenali.")
    
    # Pemilihan mode operasi
    if mode == 'ECB':
        cipher_mode = modes.ECB()
    elif mode == 'CBC':
        if iv is None:
            raise ValueError("CBC mode membutuhkan iv.")
        cipher_mode = modes.CBC(iv)
    else:
        raise ValueError(f"Mode {mode} tidak dikenali.")
    
    # Setup Cipher
    cipher = Cipher(cipher_algorithm, cipher_mode, backend=backend)

    # Tambahkan padding kecuali untuk ChaCha20
    if algorithm != 'ChaCha20':
        padder = padding.PKCS7(cipher_algorithm.block_size).padder()
        padded_data = padder.update(message.encode()) + padder.finalize()
    else:
        padded_data = message.encode()

    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return ciphertext.hex()

# Fungsi untuk dekripsi
def decrypt_message(algorithm, key, ciphertext, mode='ECB', iv=None):
    backend = default_backend()

    # Pemilihan algoritma dan mode
    if algorithm == 'AES':
        cipher_algorithm = algorithms.AES(key)
    elif algorithm == 'DES':
        cipher_algorithm = algorithms.TripleDES(key)
    elif algorithm == 'Blowfish':
        cipher_algorithm = algorithms.Blowfish(key)
    elif algorithm == 'ChaCha20':
        if iv is None:
            raise ValueError("ChaCha20 membutuhkan nonce/iv.")
        cipher_algorithm = algorithms.ChaCha20(key, iv)
    elif algorithm == 'Camellia':
        cipher_algorithm = algorithms.Camellia(key)
    else:
        raise ValueError(f"Algoritma {algorithm} tidak dikenali.")
    
    # Pemilihan mode operasi
    if mode == 'ECB':
        cipher_mode = modes.ECB()
    elif mode == 'CBC':
        if iv is None:
            raise ValueError("CBC mode membutuhkan iv.")
        cipher_mode = modes.CBC(iv)
    else:
        raise ValueError(f"Mode {mode} tidak dikenali.")
    
    # Setup Cipher
    cipher = Cipher(cipher_algorithm, cipher_mode, backend=backend)

    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(bytes.fromhex(ciphertext)) + decryptor.finalize()

    # Hapus padding kecuali untuk ChaCha20
    if algorithm != 'ChaCha20':
        unpadder = padding.PKCS7(cipher_algorithm.block_size).unpadder()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    else:
        unpadded_data = decrypted_data

    return unpadded_data.decode()

# Route untuk melayani file HTML
@app.route('/')
def serve_html():
    return send_from_directory(os.getcwd(), 'Enk.html')

# Route untuk enkripsi
@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    algorithm = data['algorithm']
    key = data['key'].encode()
    message = data['message']
    mode = data.get('mode', 'ECB')
    iv = data.get('iv', None)

    if algorithm == 'AES' and len(key) != 16:
        return jsonify({"error": "Kunci untuk AES harus 16 byte"}), 400
    if algorithm == 'DES' and len(key) != 24:
        return jsonify({"error": "Kunci untuk DES harus 24 byte"}), 400
    if algorithm == 'Blowfish' and len(key) < 4:
        return jsonify({"error": "Kunci untuk Blowfish minimal 4 byte"}), 400
    if algorithm == 'Camellia' and len(key) != 16:
        return jsonify({"error": "Kunci untuk Camellia harus 16 byte"}), 400

    try:
        encrypted_message = encrypt_message(algorithm, key, message, mode, iv and iv.encode())
        return jsonify({"encrypted_message": encrypted_message})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Route untuk dekripsi
@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    algorithm = data['algorithm']
    key = data['key'].encode()
    ciphertext = data['ciphertext']
    mode = data.get('mode', 'ECB')
    iv = data.get('iv', None)

    if algorithm == 'AES' and len(key) != 16:
        return jsonify({"error": "Kunci untuk AES harus 16 byte"}), 400
    if algorithm == 'DES' and len(key) != 24:
        return jsonify({"error": "Kunci untuk DES harus 24 byte"}), 400
    if algorithm == 'Blowfish' and len(key) < 4:
        return jsonify({"error": "Kunci untuk Blowfish minimal 4 byte"}), 400
    if algorithm == 'Camellia' and len(key) != 16:
        return jsonify({"error": "Kunci untuk Camellia harus 16 byte"}), 400

    try:
        decrypted_message = decrypt_message(algorithm, key, ciphertext, mode, iv and iv.encode())
        return jsonify({"decrypted_message": decrypted_message})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
