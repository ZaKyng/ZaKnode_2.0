import pygame

# Inicializace Pygame
pygame.init()

# 1. Vytvoření okna a rendereru (vaše zadání)
window = pygame.Window(size=(800, 600), resizable=True)
renderer = pygame.Renderer(window)

# Nastavení titulku okna
window.title = "Moderní Pygame Window & Renderer"

running = True
clock = pygame.Clock()

# Hlavní herní smyčka
while running:
    # 2. Zpracování událostí (Events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # S novým API nemusíte při změně velikosti okna 
        # znovu volat set_mode(), renderer se přizpůsobí automaticky.
        elif event.type == pygame.VIDEORESIZE:
            print(f"Nová velikost okna: {event.w}x{event.h}")

    # 3. Kreslení (Rendering)
    # Nastavení barvy pozadí (černá) a vyčištění obrazovky
    renderer.draw_color = (0, 0, 0, 255)
    renderer.clear()

    # Vykreslení testovacího červeného obdélníku uprostřed okna
    # Nové API umožňuje dynamicky číst aktuální velikost okna přes window.size
    win_w, win_h = window.size
    rect_width, rect_height = 200, 150
    
    renderer.draw_color = (255, 0, 0, 255) # Červená
    renderer.fill_rect((
        (win_w - rect_width) // 2, 
        (win_h - rect_height) // 2, 
        rect_width, 
        rect_height
    ))

    # Překlopení bufferu na obrazovku (náhrada za pygame.display.flip())
    renderer.present()

    # Omezení FPS na 60
    clock.tick(60)

pygame.quit()
