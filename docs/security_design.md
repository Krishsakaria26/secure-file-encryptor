# Security Design & Threat Model

## 1. Overview

This project implements a zero-knowledge, client-side file encryption tool.
All cryptographic operations are performed locally. No plaintext data or
encryption keys are stored or transmitted.

The system guarantees confidentiality and integrity of files even if the
encrypted output is leaked or stolen. 

---

## 2. Assets Protected

- File contents (confidentiality)
- File integrity (tamper detection)
- Encryption keys derived from user passwords

---

## 3. Threat Actors

| Actor | Capability |
|------|-----------|
| Casual attacker | Access to encrypted file |
| Malicious insider | Attempts file tampering |
| Offline attacker | Performs brute-force attacks |
| Malware | Reads stored encrypted data |

---

## 4. Assumptions

- Attacker does NOT have the user password
- Cryptographic primitives are secure
- Operating system provides secure randomness
- User chooses a strong password

---

## 5. Threats & Mitigations

### T1: Encrypted File Leakage
**Threat:** Attacker steals encrypted file  
**Mitigation:** AES-256 encryption with PBKDF2-derived key  

---

### T2: Brute-Force Password Attack
**Threat:** Offline password guessing  
**Mitigation:**  
- PBKDF2 with 200,000 iterations  
- Password entropy enforcement  

---

### T3: File Tampering
**Threat:** Modify encrypted data  
**Mitigation:**  
- HMAC-SHA256 with constant-time comparison  

---

### T4: Metadata Leakage
**Threat:** Filename or type inference  
**Mitigation:**  
- Fixed output filename  
- No metadata storage  

---

## 6. Out-of-Scope Threats

- Compromised operating system
- Keyloggers or screen capture malware
- Physical coercion
- Password reuse across systems

---

## 7. Cryptographic Choices

| Component | Algorithm |
|--------|----------|
| Encryption | AES-256 (Fernet) |
| Key Derivation | PBKDF2-HMAC-SHA256 |
| Integrity | HMAC-SHA256 |
| Randomness | OS CSPRNG |

---

## 8. Security Guarantees

- Zero-knowledge design
- Confidentiality against offline attackers
- Integrity verification before decryption
- No key storage

---

## 9. Future Security Improvements

- Memory zeroization
- Hardware-backed key derivation
- Rate-limited decryption attempts
- Versioned encrypted container format
