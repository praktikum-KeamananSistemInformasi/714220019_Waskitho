// Fungsi untuk mengubah string ke bentuk ArrayBuffer
function strToArrayBuffer(str) {
    const encoder = new TextEncoder();
    return encoder.encode(str);
}

// Fungsi untuk mengubah ArrayBuffer ke bentuk string
function arrayBufferToStr(buffer) {
    const decoder = new TextDecoder();
    return decoder.decode(buffer);
}

// Fungsi untuk menghasilkan IV (Initialization Vector) jika dibutuhkan
function generateIV(length) {
    return window.crypto.getRandomValues(new Uint8Array(length));
}

// Fungsi utama untuk enkripsi menggunakan berbagai algoritma dan mode
async function encryptMessage(algorithm, key, message, mode = 'CBC', iv = null) {
    const encodedKey = strToArrayBuffer(key);
    const encodedMessage = strToArrayBuffer(message);
    let algo = {};

    if (algorithm === 'AES') {
        algo.name = 'AES-' + (mode === 'CBC' ? 'CBC' : 'GCM');
        algo.iv = iv || generateIV(16);  // IV untuk AES-CBC atau AES-GCM
    } else {
        throw new Error(`Algorithm ${algorithm} is not supported.`);
    }

    const cryptoKey = await crypto.subtle.importKey('raw', encodedKey, algo, false, ['encrypt']);
    return crypto.subtle.encrypt(algo, cryptoKey, encodedMessage);
}

async function decryptMessage(algorithm, key, encryptedMessage, mode = 'CBC', iv = null) {
    const encodedKey = strToArrayBuffer(key);
    let algo = {};

    if (algorithm === 'AES') {
        algo.name = 'AES-' + (mode === 'CBC' ? 'CBC' : 'GCM');
        algo.iv = iv;
    } else {
        throw new Error(`Algorithm ${algorithm} is not supported.`);
    }

    const cryptoKey = await crypto.subtle.importKey('raw', encodedKey, algo, false, ['decrypt']);
    const decrypted = await crypto.subtle.decrypt(algo, cryptoKey, encryptedMessage);
    return arrayBufferToStr(decrypted);
}


// Fungsi untuk dekripsi menggunakan berbagai algoritma dan mode
async function decryptMessage(algorithm, key, encryptedMessage, mode = 'ECB', iv = null) {
    const encodedKey = strToArrayBuffer(key);
    let algo = {};

    switch (algorithm) {
        case 'AES':
            algo.name = 'AES-' + (mode === 'CBC' ? 'CBC' : 'ECB');
            algo.iv = iv;
            break;
        case 'DES':
            algo.name = 'DES-' + (mode === 'CBC' ? 'CBC' : 'ECB');
            algo.iv = iv;
            break;
        case 'Blowfish':
            algo.name = 'Blowfish';
            algo.iv = iv;
            break;
        case 'ChaCha20':
            algo.name = 'ChaCha20';
            algo.iv = iv;
            break;
        default:
            throw new Error(`Algorithm ${algorithm} is not supported.`);
    }

    const cryptoKey = await crypto.subtle.importKey('raw', encodedKey, algo, false, ['decrypt']);
    const decrypted = await crypto.subtle.decrypt(algo, cryptoKey, encryptedMessage);
    return arrayBufferToStr(decrypted);
}

// Fungsi untuk memulai enkripsi berdasarkan input
async function handleEncryption() {
    const message = document.getElementById('message').value;
    const key = document.getElementById('key').value;
    const algorithm = document.getElementById('algorithm').value;
    const mode = document.getElementById('mode').value;
    const iv = generateIV(16); // Default IV untuk AES

    try {
        const encrypted = await encryptMessage(algorithm, key, message, mode, iv);
        document.getElementById('result').innerText = `Encrypted: ${new Uint8Array(encrypted)}`;
    } catch (err) {
        document.getElementById('result').innerText = `Error: ${err.message}`;
    }
}

// Fungsi untuk memulai dekripsi berdasarkan input
async function handleDecryption() {
    const encryptedMessage = new Uint8Array(document.getElementById('encryptedMessage').value.split(','));
    const key = document.getElementById('key').value;
    const algorithm = document.getElementById('algorithm').value;
    const mode = document.getElementById('mode').value;
    const iv = generateIV(16); // Default IV untuk AES

    try {
        const decrypted = await decryptMessage(algorithm, key, encryptedMessage, mode, iv);
        document.getElementById('result').innerText = `Decrypted: ${decrypted}`;
    } catch (err) {
        document.getElementById('result').innerText = `Error: ${err.message}`;
    }
}

let savedIV; // Variable untuk menyimpan IV
let encryptedMessageBuffer; // Variable untuk menyimpan data terenkripsi

// Fungsi untuk memulai enkripsi berdasarkan input
async function handleEncryption() {
    const message = document.getElementById('message').value;
    const key = document.getElementById('key').value;
    const algorithm = document.getElementById('algorithm').value;
    const mode = document.getElementById('mode').value;
    savedIV = generateIV(16); // Simpan IV yang digunakan

    try {
        const encrypted = await encryptMessage(algorithm, key, message, mode, savedIV);
        encryptedMessageBuffer = new Uint8Array(encrypted); // Simpan hasil enkripsi
        document.getElementById('result').innerText = `Encrypted: ${encryptedMessageBuffer}`;
    } catch (err) {
        document.getElementById('result').innerText = `Error: ${err.message}`;
    }
}

// Fungsi untuk memulai dekripsi berdasarkan input
async function handleDecryption() {
    const key = document.getElementById('key').value;
    const algorithm = document.getElementById('algorithm').value;
    const mode = document.getElementById('mode').value;

    try {
        const decrypted = await decryptMessage(algorithm, key, encryptedMessageBuffer, mode, savedIV);
        document.getElementById('result').innerText = `Decrypted: ${decrypted}`;
    } catch (err) {
        document.getElementById('result').innerText = `Error: ${err.message}`;
    }
}
