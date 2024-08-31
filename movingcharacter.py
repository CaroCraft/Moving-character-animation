# Este código creaunpersonaje que se mueve a lo largo de la pantalla con ayuda de teclas y un regalo en random
# Cuando el personaje y el regalo chocan aparece una pantalla con tu premio de Betty la fea hasta dar clic en x

#Importamos pyagame,sys y random
import pygame,sys,random

#Aquí se dan las dimensiones de la ventana y la creamos con su título
screen_largo=960
screen_ancho=720
#Iniciamos pygame
pygame.init()
screen=pygame.display.set_mode((screen_largo,screen_ancho))
pygame.display.set_caption("Recoge tu premio")

#Aquí vamos a llamar desde los archivos de la computadora las imagenes necesarias para la animación
#También se establece para que movimiento es cada imagen
def animacion_personaje():
    imagen1_down=pygame.image.load("C:/Users/Carolina/Desktop/sprites/1.png")
    imagen2_down=pygame.image.load("C:/Users/Carolina/Desktop/sprites/2.png")
    imagen3_down=pygame.image.load("C:/Users/Carolina/Desktop/sprites/3.png")

    imagen1_left=pygame.image.load("C:/Users/Carolina/Desktop/sprites/4.png")
    imagen2_left=pygame.image.load("C:/Users/Carolina/Desktop/sprites/5.png")
    imagen3_left=pygame.image.load("C:/Users/Carolina/Desktop/sprites/6.png")

    imagen1_right=pygame.image.load("C:/Users/Carolina/Desktop/sprites/7.png")
    imagen2_right=pygame.image.load("C:/Users/Carolina/Desktop/sprites/8.png")
    imagen3_right=pygame.image.load("C:/Users/Carolina/Desktop/sprites/9.png")
    
    imagen1_up=pygame.image.load("C:/Users/Carolina/Desktop/sprites/10.png")
    imagen2_up=pygame.image.load("C:/Users/Carolina/Desktop/sprites/11.png")
    imagen3_up=pygame.image.load("C:/Users/Carolina/Desktop/sprites/12.png")

    #Añadimos las imagenes a la lista correspondiente: son 3 por cada tipo de movimiento(arriba,abajo,izquierda,derecha)
    animacion_down=[imagen1_down,imagen2_down,imagen3_down]
    animacion_left=[imagen1_left,imagen2_left,imagen3_left]
    animacion_right=[imagen1_right,imagen2_right,imagen3_right]
    animacion_up=[imagen1_up,imagen2_up,imagen3_up]
    #Regresa las imagenes para luego cargarlas en animacion_personaje()
    return animacion_right, animacion_left, animacion_up, animacion_down
    
animacion_right, animacion_left, animacion_up, animacion_down=animacion_personaje()


# Aquí se añaden las características para como va a funcionar nuestro personaje 
class personaje(pygame.sprite.Sprite):
    #Aquí se le otorga una de las listas de animacion creadas anteriormente a cada tipo de movimiento
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.animacion_RIGHT=animacion_right
        self.animacion_LEFT=animacion_left
        self.animacion_UP=animacion_up
        self.animacion_DOWN=animacion_down
        # Parámetros de animación
        self.index=0
        self.speed=6
        self.direction=""
        # Aquí da los parámetros de inicio para el personaje y se obtiene su rectángulo
        self.image=self.animacion_DOWN[0]
        self.rect=self.image.get_rect()
        self.rect.topleft=position #Pone el rectángulo en la esquina de la posición dada
    
    # Esta parte del código es lo que hace que la animación corra dependiendo de la dirección    
    def update(self):
        if self.direction=="RIGHT":
            self.image=self.animacion_RIGHT[self.index]
        elif self.direction=="LEFT":
            self.image=self.animacion_LEFT[self.index]
        elif self.direction=="UP":
            self.image=self.animacion_UP[self.index]
        elif self.direction=="DOWN":
            self.image=self.animacion_DOWN[self.index]

        # Esto es para que cuando se llegue al último sprite de la lista se regrese al primero y corra otra vez
        self.index+=1
        if self.index>=3:
            self.index=0
        #Esto es para cuando el personaje está parado y no queremos que la animación siga corriendo
        # El sprite ya no cambia y se anima y ahora se queda estático
        else:
            if self.direction=="STOP_RIGHT":
                self.image=self.animacion_RIGHT[0]
            elif self.direction=="STOP_LEFT":
                self.image=self.animacion_LEFT[0]
            elif self.direction=="STOP_UP":
                self.image=self.animacion_UP[0]
            elif self.direction=="STOP_DOWN":
                self.image=self.animacion_DOWN[0]
                
    # Aquí es donde se configura el movimiento del personaja através de la pantalla y las teclas   
    def handle_event(self):
        # Lo que hace el programa es que cuando presionamos una tecla, el personaje moverá su posición en la ventana hacia la dirección que simboliza la tecla
        # Cuando llegamos al límite de la ventana, el personaje no podrá avanzar más, ya que se configuro que solo existe movimiento cuando el límite no se ha alcanzado
        key=pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            if self.rect.left<0:
                self.rect.left=0
            self.rect.x-=self.speed
            self.direction="LEFT"
        elif key[pygame.K_RIGHT]:
            if self.rect.right>screen_largo:
                self.rect.right=screen_largo
            self.rect.x+=self.speed
            self.direction="RIGHT"
        elif key[pygame.K_UP]:
            if self.rect.top<0:
                self.rect.top=0
            self.rect.y-=self.speed
            self.direction="UP"
        elif key[pygame.K_DOWN]:
            if self.rect.bottom>screen_ancho:
                self.rect.bottom=screen_ancho
            self.rect.y+=self.speed
            self.direction="DOWN"

        # Aquí se le añaden valores al momento en que no se presionan las teclas, estos son los que usamos arriba en el código para que el sprite no se anime al no cambiar su posición
        else:
            if self.direction=="RIGHT":
                self.direction="STOP_RIGHT"
            elif self.direction=="LEFT":
                self.direction="STOP_LEFT"
            elif self.direction=="UP":
                self.direction="STOP_UP"
            elif self.direction=="DOWN":
                self.direction="STOP_DOWN"
            else:
                self.direction=""

# Aquí se establecen las características del regalo, donde se crea un rectángulo y su posición
class regalo(pygame.sprite.Sprite):
    #Se carga el regalo y se establece el rectángulo que sirve para saber su posición y tamaño (características de la imagen) y se genera el regalo en la posición establecida 
    def __init__(self,picture_path,pos_x,pos_y):
        super().__init__()
        self.image=pygame.image.load(picture_path)
        self.rect=self.image.get_rect()
        self.rect.center=[pos_x,pos_y]


# Aquí se establece una pantalla que funciona parecido a un game over, esto se activa al colisionar
# Se añade un sonido, una imagen que llena la pantalla y las condiciones de salida
# Solo se puede salir de la ventana al dar clic en la x o también se puede dejar de mostrar la imagen presionando x
# La x se estableció para que al mostrar el premio se quedara fijo en la pantalla aunque se presione cualquier tecla excepto x
def premio_novela():
    pygame.mixer.music.load("C:/Users/Carolina/Desktop/sprites/sonidoganar.mp3")
    pygame.mixer.music.play()
    background=pygame.image.load("C:/Users/Carolina/Desktop/sprites/trofeot.jpeg")
    screen.blit(background,[0,0])
    pygame.display.flip()
    waiting=True
    while waiting:
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
        

    
# Aquí se crea el grupo de sprites del personaje y la posicion de inicio del mismo
jugador=personaje([25,25])
player_group=pygame.sprite.Group()
player_group.add(jugador)
#Aquí se crea el grupo de sprites de regalo y lo posiciona en un lugar random
regalo_group=pygame.sprite.Group()
for regaloo in range(1):
    new_regalo=regalo("C:/Users/Carolina/Desktop/sprites/regalo (1).png",random.randrange(200,screen_largo-50),random.randrange(200,screen_ancho-50))
    regalo_group.add(new_regalo)

#Reloj
CLOCK=pygame.time.Clock()


game_win=False


while True:
    #Esto detecta cuando es que colisiona el personaje con el regalo y llama a la función premio_novela si esto sucede
    colision=pygame.sprite.spritecollide(jugador,regalo_group,True)
    if colision:
        game_win=True
        premio_novela()

    #Condicion de salida con QUIT
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()      

    #FPS de la animación y actualiza la pantalla además de llenarla del color cian
    CLOCK.tick(60)
    pygame.display.update()
    screen.fill((77,253,252))
    # Se dibuja y actualiza tanto el jugador como los regalos 
    jugador.handle_event()
    player_group.update()
    regalo_group.update()
    regalo_group.draw(screen)
    player_group.draw(screen)
    
    pygame.display.flip()


