import pygame
import os # Importamos os para manejar rutas de archivos fácilmente

# 1. Inicializar Pygame
pygame.init()

# 2. Configuración de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moviendo mi personaje")

# --- SECCIÓN DE LA IMAGEN ---

# Definimos el nombre del archivo de la imagen
NOMBRE_IMAGEN = "gato.png" 

# Obtenemos la ruta absoluta de la carpeta donde está este script .py
# Esto ayuda a que Pygame encuentre la imagen sin importar desde dónde corras el script.
carpeta_actual = os.path.dirname(__file__)
ruta_imagen = os.path.join(carpeta_actual, NOMBRE_IMAGEN)

try:
    # Cargamos la imagen desde la ruta que definimos
    imagen_original = pygame.image.load(ruta_imagen)
    
    # OPCIONAL: Redimensionar la imagen si es muy grande.
    # Aquí la hacemos de 60x60 píxeles. Ajusta según necesites.
    imagen = pygame.transform.scale(imagen_original, (120, 120))
    
    # Obtenemos el rectángulo de la imagen para manejar su posición fácilmente
    rect_personaje = imagen.get_rect()
    
except pygame.error as e:
    print(f"¡ERROR! No se pudo cargar la imagen '{NOMBRE_IMAGEN}'.")
    print(f"Asegúrate de que esté en la misma carpeta que este script.")
    print(f"Detalles del error: {e}")
    pygame.quit()
    exit() # Cerramos el programa si no hay imagen

# --- FIN SECCIÓN DE LA IMAGEN ---

# 4. Posición inicial (usando el rectángulo de la imagen)
rect_personaje.center = (WIDTH // 2, HEIGHT // 2)
velocidad = 5 

# Reloj para controlar los FPS
clock = pygame.time.Clock()

run = True
while run:
    # Controlamos los FPS
    clock.tick(60)

    # A. Detectar eventos de salida
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # B. Detectar teclas presionadas (MOVIMIENTO)
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        rect_personaje.x -= velocidad
    if keys[pygame.K_RIGHT]:
        rect_personaje.x += velocidad
    if keys[pygame.K_UP]:
        rect_personaje.y -= velocidad
    if keys[pygame.K_DOWN]:
        rect_personaje.y += velocidad

    # --- LÍMITES DE PANTALLA (Para que no se escape) ---
    # Si la X es menor a 0, la paramos en 0
    if rect_personaje.left < 0:
        rect_personaje.left = 0
    # Si la X más el ancho es mayor al borde derecho...
    if rect_personaje.right > WIDTH:
        rect_personaje.right = WIDTH
    # Igual para arriba y abajo
    if rect_personaje.top < 0:
        rect_personaje.top = 0
    if rect_personaje.bottom > HEIGHT:
        rect_personaje.bottom = HEIGHT


    # C. Dibujar todo
    # Fondo (puedes cambiar el color R, G, B)
    screen.fill((50, 100, 150)) # Un azulito
    
    # Dibujamos la IMAGEN usando su RECTÁNGULO de posición
    screen.blit(imagen, rect_personaje)

    # Actualizar la pantalla
    pygame.display.update()

pygame.quit()
