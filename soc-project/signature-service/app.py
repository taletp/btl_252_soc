# Log Signature Service
# Provides HMAC and RSA Digital Signature for log integrity verification
# Flask-based microservice for SOC deployment

from flask import Flask, request, jsonify
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import hmac
import hashlib
import json
import os
import base64
from datetime import datetime

app = Flask(__name__)

# Configuration
HMAC_SECRET = os.environ.get('HMAC_SECRET', 'default-hmac-secret-change-in-production')
KEYS_DIR = os.environ.get('KEYS_DIR', '/app/keys')

class LogSigner:
    def __init__(self, keys_dir):
        self.keys_dir = keys_dir
        self.private_key = None
        self.public_key = None
        self._ensure_keys()
    
    def _ensure_keys(self):
        """Generate or load RSA key pair"""
        private_key_path = os.path.join(self.keys_dir, 'signing_key.pem')
        public_key_path = os.path.join(self.keys_dir, 'signing_key.pub')
        
        if os.path.exists(private_key_path) and os.path.exists(public_key_path):
            # Load existing keys
            with open(private_key_path, 'rb') as f:
                self.private_key = serialization.load_pem_private_key(
                    f.read(),
                    password=None,
                    backend=default_backend()
                )
            with open(public_key_path, 'rb') as f:
                self.public_key = serialization.load_pem_public_key(
                    f.read(),
                    backend=default_backend()
                )
        else:
            # Generate new RSA-2048 key pair
            self.private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            self.public_key = self.private_key.public_key()
            
            # Save keys
            os.makedirs(self.keys_dir, exist_ok=True)
            
            # Save private key
            private_pem = self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            with open(private_key_path, 'wb') as f:
                f.write(private_pem)
            
            # Save public key
            public_pem = self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            with open(public_key_path, 'wb') as f:
                f.write(public_pem)
            
            print(f"Generated new RSA-2048 key pair in {self.keys_dir}")
    
    def sign_log(self, log_entry: dict) -> str:
        """Sign a log entry with RSA-2048"""
        # Canonicalize the log entry (sort keys for consistency)
        message = json.dumps(log_entry, sort_keys=True, ensure_ascii=False).encode('utf-8')
        
        # Sign with RSA-PSS and SHA-256
        signature = self.private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        # Return base64-encoded signature
        return base64.b64encode(signature).decode('utf-8')
    
    def verify_signature(self, log_entry: dict, signature_b64: str) -> bool:
        """Verify a log entry's RSA signature"""
        try:
            message = json.dumps(log_entry, sort_keys=True, ensure_ascii=False).encode('utf-8')
            signature = base64.b64decode(signature_b64)
            
            self.public_key.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False

class HMACVerifier:
    def __init__(self, secret):
        self.secret = secret.encode('utf-8')
    
    def generate_hmac(self, message: dict) -> str:
        """Generate HMAC-SHA256 for a message"""
        msg_str = json.dumps(message, sort_keys=True, ensure_ascii=False)
        signature = hmac.new(
            self.secret,
            msg_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def verify_hmac(self, message: dict, signature: str) -> bool:
        """Verify HMAC-SHA256 signature"""
        expected = self.generate_hmac(message)
        return hmac.compare_digest(expected, signature)

# Initialize signers
log_signer = LogSigner(KEYS_DIR)
hmac_verifier = HMACVerifier(HMAC_SECRET)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'rsa_keys_loaded': log_signer.private_key is not None,
        'hmac_configured': len(HMAC_SECRET) > 0
    })

@app.route('/sign', methods=['POST'])
def sign_log():
    """Sign a log entry with both RSA and HMAC"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Add timestamp if not present
        if 'timestamp' not in data:
            data['timestamp'] = datetime.utcnow().isoformat()
        
        # Generate HMAC
        hmac_sig = hmac_verifier.generate_hmac(data)
        
        # Generate RSA signature
        rsa_sig = log_signer.sign_log(data)
        
        # Return signed log entry
        result = {
            'log_entry': data,
            'signatures': {
                'hmac_sha256': hmac_sig,
                'rsa_signature': rsa_sig,
                'algorithm': 'RSA-2048-PSS-SHA256'
            },
            'verified': True
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/verify', methods=['POST'])
def verify_log():
    """Verify a signed log entry"""
    try:
        data = request.get_json()
        if not data or 'log_entry' not in data or 'signatures' not in data:
            return jsonify({'error': 'Invalid format. Expected {log_entry, signatures}'}), 400
        
        log_entry = data['log_entry']
        signatures = data['signatures']
        
        # Verify HMAC
        hmac_valid = False
        if 'hmac_sha256' in signatures:
            hmac_valid = hmac_verifier.verify_hmac(log_entry, signatures['hmac_sha256'])
        
        # Verify RSA signature
        rsa_valid = False
        if 'rsa_signature' in signatures:
            rsa_valid = log_signer.verify_signature(log_entry, signatures['rsa_signature'])
        
        return jsonify({
            'log_entry': log_entry,
            'verification': {
                'hmac_valid': hmac_valid,
                'rsa_valid': rsa_valid,
                'overall_valid': hmac_valid and rsa_valid
            },
            'timestamp': datetime.utcnow().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/public-key', methods=['GET'])
def get_public_key():
    """Get the RSA public key for external verification"""
    try:
        public_pem = log_signer.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return jsonify({
            'public_key': public_pem.decode('utf-8'),
            'algorithm': 'RSA-2048',
            'format': 'PEM'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/sign/suricata', methods=['POST'])
def sign_suricata_event():
    """Specific endpoint for Suricata EVE events"""
    try:
        event = request.get_json()
        if not event:
            return jsonify({'error': 'No event data provided'}), 400
        
        # Add signature metadata
        event['_signature'] = {
            'timestamp': datetime.utcnow().isoformat(),
            'source': 'suricata',
            'hmac': hmac_verifier.generate_hmac(event),
            'rsa_signature': log_signer.sign_log(event)
        }
        
        return jsonify({
            'event': event,
            'signed': True
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Log Signature Service...")
    print(f"Keys directory: {KEYS_DIR}")
    print(f"RSA keys loaded: {log_signer.private_key is not None}")
    app.run(host='0.0.0.0', port=5000, debug=False)
