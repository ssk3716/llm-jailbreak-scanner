import base64
import binascii
import re
import unicodedata

class DecoderLayer:
    def __init__(self):
        # Patterns for detection
        self.base64_pattern = re.compile(r'(?:[A-Za-z0-9+/]{4}){2,}(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?')
        self.hex_pattern = re.compile(r'\b(?:0x)?[0-9a-fA-F]{8,}\b')
        self.binary_pattern = re.compile(r'\b[01]{8,}\b')

    def decode_recursive(self, text: str, max_depth: int = 3) -> str:
        """Recursively decodes and cleans the input text."""
        if max_depth <= 0:
            return text

        original_text = text
        
        # 1. Unicode Normalization (convert "𝔍𝔞𝔦𝔩𝔟𝔯𝔢𝔞𝔨" to "Jailbreak")
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
        
        # 2. Invisible Character Removal
        text = re.sub(r'[\u200b-\u200d\ufeff]', '', text)
        
        # 3. Base64 Decoding
        def b64_decode(match):
            try:
                decoded = base64.b64decode(match.group(0)).decode('utf-8', errors='ignore')
                return decoded if len(decoded) > 3 else match.group(0)
            except:
                return match.group(0)
        text = self.base64_pattern.sub(b64_decode, text)

        # 4. Hex Decoding
        def hex_decode(match):
            try:
                h = match.group(0).replace('0x', '')
                decoded = binascii.unhexlify(h).decode('utf-8', errors='ignore')
                return decoded if len(decoded) > 3 else match.group(0)
            except:
                return match.group(0)
        text = self.hex_pattern.sub(hex_decode, text)

        # 5. Binary Decoding
        def bin_decode(match):
            try:
                b = match.group(0)
                n = int(b, 2)
                decoded = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode('utf-8', errors='ignore')
                return decoded if len(decoded) > 3 else match.group(0)
            except:
                return match.group(0)
        text = self.binary_pattern.sub(bin_decode, text)

        # If text changed, try another round (up to max_depth)
        if text != original_text:
            return self.decode_recursive(text, max_depth - 1)
        
        return text

    def detect_obfuscation(self, original: str, decoded: str) -> bool:
        """Returns True if significant obfuscation was found and removed."""
        # Simple heuristic: if length changed or content significantly altered
        return original.strip() != decoded.strip()
