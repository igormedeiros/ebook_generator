from PIL import Image, ImageDraw, ImageFont
import os

def generate_minimalist_cover():
    # Dimensões padrão Kindle
    width, height = 1600, 2400
    bg_color = (245, 245, 245) # Off-white moderno
    accent_color = (30, 30, 30) # Cinza quase preto
    
    # Criar imagem base
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Fontes
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 55)
        author_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 70)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        author_font = ImageFont.load_default()

    # 1. Elemento Gráfico Minimalista (Asas Estilizadas de Hermes)
    # Desenhando um ícone geométrico simples
    center_x, center_y = width // 2, height // 2 - 100
    
    # Asa Esquerda
    draw.polygon([(center_x-50, center_y), (center_x-300, center_y-150), (center_x-100, center_y-50)], fill=accent_color)
    # Asa Direita
    draw.polygon([(center_x+50, center_y), (center_x+300, center_y-150), (center_x+100, center_y-50)], fill=accent_color)
    # Corpo Central (Caduceu sutil)
    draw.rectangle([center_x-5, center_y-200, center_x+5, center_y+100], fill=accent_color)

    # 2. Tipografia
    # Título
    draw.text((width//2, height - 800), "O AGENTE INVISÍVEL", fill=accent_color, font=title_font, anchor="mm")
    
    # Subtítulo
    subtitle = "Soberania Digital e Agentes Autônomos"
    draw.text((width//2, height - 680), subtitle, fill=accent_color, font=subtitle_font, anchor="mm")

    # 3. Autor (Separado por uma linha fina)
    draw.line([width//2 - 100, height - 550, width//2 + 100, height - 550], fill=accent_color, width=2)
    draw.text((width//2, height - 450), "IGOR MEDEIROS", fill=accent_color, font=author_font, anchor="mm")

    # 4. Branding Antigravity (Rodapé)
    draw.text((width//2, height - 150), "ANTIGRAVITY", fill=(180, 180, 180), font=subtitle_font, anchor="mm")

    # Salvar
    output_path = 'workspace/dominando-openclaw-guia-pratico/assets/cover.png'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    print(f"✅ Minimalist Cover generated at {output_path}")

if __name__ == "__main__":
    generate_minimalist_cover()
