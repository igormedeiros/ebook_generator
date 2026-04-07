import os
import sys
import google.generativeai as genai
from PIL import Image
import io

def generate_cover():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment.")
        sys.exit(1)

    genai.configure(api_key=api_key)
    
    # Define o modelo Imagen 3 (ajuste o nome se necessário para a versão v0.8.6)
    # Nota: Em algumas versões da SDK, a geração de imagem é feita via 
    # generativeai.ImageGenerationModel ou similar.
    
    prompt = (
        "A woodcut style engraving of Hermes, the Greek messenger god with winged sandals and a caduceus, "
        "detailed black and white lines, high contrast, minimalist white background, "
        "classic O'Reilly technical book cover style, professional and clean."
    )
    
    print(f"Generating cover with prompt: {prompt}")
    
    try:
        # Usa o modelo de geração de imagem
        model = genai.ImageGenerationModel("imagen-3.0-generate-001")
        response = model.generate_images(
            prompt=prompt,
            number_of_images=1,
            aspect_ratio="3:4"
        )
        
        if response.images:
            image_data = response.images[0]
            output_path = 'workspace/dominando-openclaw-guia-pratico/assets/cover.png'
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            image_data.save(output_path)
            print(f"✅ Cover saved to {output_path}")
            return True
        else:
            print("❌ No images generated.")

    except Exception as e:
        print(f"❌ Error generating image: {str(e)}")
    
    return False

if __name__ == "__main__":
    success = generate_cover()
    if not success:
        sys.exit(1)
