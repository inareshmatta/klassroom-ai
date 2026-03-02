import os
from PIL import Image, ImageDraw, ImageFont
import math

# Try to use a better font if available, fallback to default
try:
    font_large = ImageFont.truetype("arialbd.ttf", 60)
    font_med = ImageFont.truetype("arial.ttf", 36)
    font_small = ImageFont.truetype("arial.ttf", 24)
except IOError:
    font_large = ImageFont.load_default()
    font_med = ImageFont.load_default()
    font_small = ImageFont.load_default()

def create_glass_bg(width, height):
    img = Image.new('RGBA', (width, height), (30, 30, 40, 255))
    draw = ImageDraw.Draw(img)
    # Add subtle gradient/glass effect
    for y in range(height):
        alpha = int(255 - (y/height)*150)
        draw.line([(0, y), (width, y)], fill=(40, 40, 60, alpha))
    return img

def generate_voice_interaction_gif():
    frames = []
    width, height = 800, 500
    
    # Text typing effect
    text = "Explain how a neural network learns"
    
    for i in range(40):
        img = create_glass_bg(width, height)
        draw = ImageDraw.Draw(img)
        
        # Draw UI container
        draw.rounded_rectangle([(100, 100), (700, 400)], radius=20, fill=(20, 20, 30, 200), outline=(100, 150, 250, 100), width=2)
        
        # User message typing
        char_count = min(len(text), int((i/15) * len(text)))
        current_text = text[:char_count]
        
        if i < 20: # User speaking phase
            draw.text((150, 150), "User:", font=font_small, fill=(150, 150, 150))
            draw.text((150, 190), current_text, font=font_med, fill=(255, 255, 255))
            
            # Draw mic ripple
            radius = 20 + math.sin(i * 0.5) * 10
            draw.ellipse([(600-radius, 200-radius), (600+radius, 200+radius)], fill=(250, 100, 100, 100))
            draw.ellipse([(590, 190), (610, 210)], fill=(255, 80, 80, 255)) # Mic center
            
        else: # AI responding phase
            draw.text((150, 150), "User:", font=font_small, fill=(150, 150, 150))
            draw.text((150, 190), text, font=font_med, fill=(255, 255, 255))
            
            draw.text((150, 270), "Tutor:", font=font_small, fill=(100, 200, 250))
            response = "Imagine a network of tiny judges..."
            resp_char_count = min(len(response), int(((i-20)/15) * len(response)))
            draw.text((150, 310), response[:resp_char_count], font=font_med, fill=(200, 230, 255))
            
            # AI speaking animation
            for bar in range(5):
                bar_h = abs(10 + math.sin(i * 0.8 + bar) * 15)
                draw.rectangle([(600 + bar*15, 330 - bar_h), (610 + bar*15, 330 + bar_h)], fill=(100, 200, 255))
                
        frames.append(img)
        
    frames[0].save('d:/KlassroomAI/frontend/public/assets/landing_voice.webp', format='WebP', append_images=frames[1:], save_all=True, duration=100, loop=0)

def generate_visual_generation_gif():
    frames = []
    width, height = 800, 500
    
    for i in range(40):
        img = create_glass_bg(width, height)
        draw = ImageDraw.Draw(img)
        
        # Left Panel (Chat)
        draw.rounded_rectangle([(50, 50), (350, 450)], radius=15, fill=(20, 20, 30, 200))
        draw.text((70, 70), "Tutor: Let me show you the\nstructure of an atom.", font=font_small, fill=(200, 230, 255))
        
        # Right Panel (Visuals)
        draw.rounded_rectangle([(380, 50), (750, 450)], radius=15, fill=(20, 20, 30, 200), outline=(255, 150, 200, 100), width=2)
        
        # Draw atom animation
        center_x, center_y = 565, 250
        
        if i < 10:
            # Loading ring
            arc_end = int(360 * (i/10))
            draw.arc([(500, 185), (630, 315)], 0, arc_end, fill=(255, 150, 200), width=5)
            draw.text((520, 240), "Generating...", font=font_small, fill=(150, 150, 150))
        else:
            # Nucleus
            draw.ellipse([(center_x-15, center_y-15), (center_x+15, center_y+15)], fill=(255, 100, 100))
            draw.ellipse([(center_x-5, center_y-20), (center_x+5, center_y+20)], fill=(100, 100, 255))
            
            # Electrons orbiting
            angle1 = (i * 0.2) % (2*math.pi)
            angle2 = (-i * 0.15 + math.pi/2) % (2*math.pi)
            
            r1_x, r1_y = 80, 40
            e1_x = center_x + math.cos(angle1) * r1_x
            e1_y = center_y + math.sin(angle1) * r1_y
            
            r2_x, r2_y = 40, 90
            e2_x = center_x + math.cos(angle2) * r2_x
            e2_y = center_y + math.sin(angle2) * r2_y
            
            # Orbits
            draw.ellipse([(center_x-r1_x, center_y-r1_y), (center_x+r1_x, center_y+r1_y)], outline=(100, 100, 100), width=1)
            draw.ellipse([(center_x-r2_x, center_y-r2_y), (center_x+r2_x, center_y+r2_y)], outline=(100, 100, 100), width=1)
            
            draw.ellipse([(e1_x-5, e1_y-5), (e1_x+5, e1_y+5)], fill=(255, 255, 100))
            draw.ellipse([(e2_x-5, e2_y-5), (e2_x+5, e2_y+5)], fill=(255, 255, 100))
            
            draw.text((450, 400), "Figure 1: Atomic Structure", font=font_small, fill=(255, 255, 255))

        frames.append(img)
        
    frames[0].save('d:/KlassroomAI/frontend/public/assets/landing_visuals.webp', format='WebP', append_images=frames[1:], save_all=True, duration=80, loop=0)


def generate_assessment_gif():
    frames = []
    width, height = 800, 500
    
    for i in range(30):
        img = create_glass_bg(width, height)
        draw = ImageDraw.Draw(img)
        
        # Center Modal
        draw.rounded_rectangle([(150, 80), (650, 420)], radius=20, fill=(20, 20, 30, 240), outline=(100, 250, 150, 150), width=2)
        
        draw.text((200, 110), "Assessment Center", font=font_med, fill=(255, 255, 255))
        draw.line([(200, 160), (600, 160)], fill=(100, 100, 100))
        
        # Quiz Question
        draw.text((200, 190), "Q1: What is the powerhouse of the cell?", font=font_small, fill=(200, 200, 200))
        
        # Options
        options = ["A) Nucleus", "B) Mitochondria", "C) Ribosome", "D) Endoplasmic Reticulum"]
        
        for j, opt in enumerate(options):
            y_pos = 240 + j * 40
            fill_col = (30, 30, 40)
            text_col = (150, 150, 150)
            outline_col = (60, 60, 80)
            
            # Simulate hover/selection
            if i > 10 and j == 1:
                fill_col = (50, 100, 150) if i < 20 else (50, 150, 80) # Turns green after clicking
                text_col = (255, 255, 255)
            
            draw.rounded_rectangle([(200, y_pos), (600, y_pos+30)], radius=8, fill=fill_col, outline=outline_col)
            draw.text((220, y_pos+5), opt, font=font_small, fill=text_col)
            
        if i >= 20:
            draw.text((400, 120), "✅ Correct!", font=font_med, fill=(50, 255, 100))

        frames.append(img)
        
    frames[0].save('d:/KlassroomAI/frontend/public/assets/landing_assessment.webp', format='WebP', append_images=frames[1:], save_all=True, duration=150, loop=0)

if __name__ == '__main__':
    if not os.path.exists('d:/KlassroomAI/frontend/public/assets'):
        os.makedirs('d:/KlassroomAI/frontend/public/assets')
        
    print("Generating Animations...")
    generate_voice_interaction_gif()
    generate_visual_generation_gif()
    generate_assessment_gif()
    print("Done!")
