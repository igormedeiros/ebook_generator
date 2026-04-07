import os
import sys
import base64
import requests
import json

def generate_flash_image():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found.")
        return False

    # Endpoint para Gemini 2.0 Flash (v1beta) - Tentando Image Generation Task
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}"
    
    prompt = "Generate a high-quality, professional, minimalist black and white line art image of Hermes wings for a book cover. White background."
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "response_mime_type": "image/png"
        }
    }

    print("Requesting image from Gemini 2.0 Flash...")
    response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
    
    if response.status_code == 200:
        # Nota: O Gemini Flash pode retornar a imagem em diferentes formatos na v1beta
        print("Success! Parsing response...")
        # (Lógica de parse simplificada para fins de teste)
        with open("raw_flash_response.json", "w") as f:
            f.write(response.text)
        return True
    else:
        print(f"Error {response.status_code}: {response.text}")
        return False

if __name__ == "__main__":
    generate_flash_image()
