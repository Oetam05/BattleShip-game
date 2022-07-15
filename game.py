import pygame
import time
import threading
import random
from menu import *


class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.MOUSE_MOVE, self.MOUSE_DOWN = False, False, False, False, False, False
        self.SOUND=True
        self.DISPLAY_W, self.DISPLAY_H = 1000, 680
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        self.ship1_img= pygame.image.load("img/ship1.png")
        self.ship2_img= pygame.image.load("img/ship2.png")
        self.ship3_img= pygame.image.load("img/ship3.png")
        self.ship4_img= pygame.image.load("img/ship4.png")
        self.sight_img= pygame.image.load("img/sight.png")
        self.successful_shot_img= pygame.image.load("img/successful_shot.png")
        self.missed_shot_img= pygame.image.load("img/missed_shot.png")        
        self.font_name = '8-BIT WONDER.TTF'
        self.mouse_position=(0,0)
        #self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.input_menu = InputDataMenu(self)
        self.curr_menu = self.main_menu        
        self.MISSED_SHOT="-"
        self.SUCCESSFUL_SHOT="*"
        self.players=[]
        self.active_player=0
        self.opposite_player=1
        self.waiting=False
        self.board_size=10        
        self.n_ship1=1
        self.n_ship2=0
        self.n_ship3=0
        self.n_ship4=0

    def game_loop(self):
        if self.playing:
            self.players.append(Jugador(0, self.board_size, self.n_ship1, self.n_ship2, self.n_ship3, self.n_ship4))
            self.players.append(Jugador(1, self.board_size, self.n_ship1, self.n_ship2, self.n_ship3, self.n_ship4))
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing= False                
            self.display.fill((202, 225, 249))            
            self.check_destroyed()
            ship_count = self.contar_barcos(self.players[self.opposite_player])
            for i in range(self.board_size):
                for j in range(self.board_size):
                    pygame.draw.rect(self.display,(253, 124, 75), [10+j*65, 20+i*65, 64.9, 64.9], 1)
                    if(self.players[self.opposite_player].matriz[i][j] == self.MISSED_SHOT):                        
                        self.draw_image(self.missed_shot_img, 10+65*j+32, 20+65*i+32)                                        
                    elif(self.players[self.opposite_player].matriz[i][j] == self.SUCCESSFUL_SHOT):
                        self.draw_image(self.successful_shot_img, 10+65*j+32, 20+65*i+32)                                   
            self.draw_image(self.sight_img,self.mouse_position[0],self.mouse_position[1])
            self.draw_text("Size 1    "+str(ship_count[0]), 13, self.DISPLAY_W-100, 100, self.BLACK)
            self.draw_text("Size 2    "+str(ship_count[1]), 13, self.DISPLAY_W-100, 200, self.BLACK)
            self.draw_text("Size 3    "+str(ship_count[2]), 13, self.DISPLAY_W-100, 300, self.BLACK)
            self.draw_text("Size 4    "+str(ship_count[3]), 13, self.DISPLAY_W-100, 400, self.BLACK)
            self.window.blit(self.display, (0,0))
            pygame.display.update()            
            self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            
            if event.type== pygame.MOUSEMOTION:
                self.mouse_position=pygame.mouse.get_pos()
                self.MOUSE_MOVE=True
                if self.playing:
                    self.sight_center=self.mouse_position
            if event.type== pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_position=pygame.mouse.get_pos()
                    self.MOUSE_DOWN=True
                    if self.playing:
                        if(self.mouse_position[0] > 10 and self.mouse_position[0] < 660 and self.mouse_position[1] > 20 and self.mouse_position[1] < 670 and not self.waiting):
                            self.shoot(self.mouse_position,self.players)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.MOUSE_MOVE, self.MOUSE_DOWN = False, False, False, False, False, False

    def check_destroyed(self):
        # Se recorren todos los barcos para ver cuales fueron destruidos y mostrarlos
        for barco in self.players[self.opposite_player].barcos:
            if barco.is_destroyed():
                # Si es un submarino no tenemos que mirar la orientacion
                if barco.tamaño == 1:
                    self.draw_image(self.ship1_img, 10+65*int(barco.get_coord()[0][4])+32, 20+65*int(barco.get_coord()[0][1])+32)
                # Si la orientacion es horizontal
                if barco.orient == 1:
                    # Si es un destructor
                    if barco.tamaño == 2:
                        self.draw_image(pygame.transform.rotate(self.ship2_img , 90), 10+65*(int(barco.get_coord()[0][4])+1), 53+65*int(barco.get_coord()[0][1]))                        
                    # Si es un crucero
                    elif barco.tamaño == 3:
                        self.draw_image(pygame.transform.rotate(self.ship3_img , 90), 10+65*(int(barco.get_coord()[2][4])+1.5), 53+65*int(barco.get_coord()[2][1]))
                    # Si es un portaaviones
                    elif barco.tamaño == 4:
                        self.draw_image(pygame.transform.rotate(self.ship4_img , 90), 10+65*(int(barco.get_coord()[2][4])+2), 53+65*int(barco.get_coord()[2][1]))                        
                # Si la orientacion es vertical
                elif barco.orient == 0:
                    # Si es un destructor
                    if barco.tamaño == 2:
                        self.draw_image(self.ship2_img, 43+65*int(barco.get_coord()[0][4]), 20+65*(int(barco.get_coord()[0][1])+1))                        
                    # Si es un crucero
                    elif barco.tamaño == 3:
                        self.draw_image(self.ship3_img, 43+65*int(barco.get_coord()[2][4]), 20+65*(int(barco.get_coord()[2][1])+1.5))
                    # Si es un portaaviones
                    elif barco.tamaño == 4:
                        self.draw_image(self.ship4_img, 43+65*int(barco.get_coord()[2][4]), 20+65*(int(barco.get_coord()[2][1])+2))                        

    def draw_text(self, text, size, x, y, color):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)
    
    def draw_image(self, image, x, y ):                
        image_rect = image.get_rect()
        image_rect.center = (x,y)
        self.display.blit(image,image_rect)    

    #Espera un segundo antes de pasar el turno al siguiente jugador
    def cedeTurno(self):
        time.sleep(1)
        self.opposite_player=self.active_player
        self.active_player = 0 if self.active_player == 1 else 1
        self.waiting=False

    # Funcion para los disparos
    def shoot(self,p, jugadores):
        pos = self.findPosition(p)        
        self.opposite_player = 0 if self.active_player == 1 else 1
        if(pos != -1):
            a = False
            b = True
            # se mira en todos los barcos sus posiciones y se compara con la posición del disparo
            while(b):
                for barco in jugadores[self.opposite_player].barcos:
                    if a:
                        break
                    for coord in barco.get_coord():
                        if(str(pos) == str(coord)):  # dispara en una posición donde hay un barco
                            a = True
                            b = False
                            barco.mod_coord(pos[0], pos[1])
                            # Se dibuja el disparo si acierta
                            jugadores[self.opposite_player].matriz[pos[0]][pos[1]] = self.SUCCESSFUL_SHOT
                            if barco.is_destroyed():  # se verifica si el barco está completamente destruido
                                barco.set_destroyed()
                                if self.players[self.opposite_player].is_lose():
                                    print("El jugador ganador fue ",self.active_player)
                                    self.waiting=True                                                                                                    
                            break
                        else:
                            a = False
                if (not a):  # si no encuentra ningún barco
                    if jugadores[self.opposite_player].matriz[pos[0]][pos[1]] != self.MISSED_SHOT:
                        b = False
                        # Se dibuja el disparo si falla
                        jugadores[self.opposite_player].matriz[pos[0]][pos[1]] = self.MISSED_SHOT
                        # se pasa el control al siguiente jugador
                        self.waiting=True
                        t = threading.Thread(target=self.cedeTurno)
                        t.start()
                return False

    # Funcion que devuelve la casilla donde se presionó el click
    def findPosition(self, p):
        for i in range(self.board_size):
            for j in range(self.board_size):
                # Se analiza si la posicion está dentro del rango de cada casilla
                if(p[0] > 10+j*65 and p[0] < 10+j*65+64.9 and p[1] > 20+i*65 and p[1] < 20+i*65+64.9):
                    return i, j
        # retorna -1 si no está en ninguna casilla
        return -1

    #Cuenta la cantidad de barcos sin destruir que quedan
    def contar_barcos(self, jugador):
        cont = [0, 0, 0, 0]
        for barco in jugador.barcos:
            if not barco.is_destroyed(): 
                if barco.tamaño == 1:
                    cont[0] = cont[0]+1
                elif barco.tamaño == 2:
                    cont[1] = cont[1]+1
                elif barco.tamaño == 3:
                    cont[2] = cont[2]+1
                elif barco.tamaño == 4:
                    cont[3] = cont[3]+1
        return cont


class Barco:
    def __init__(self, tamaño) -> None:
        self.tamaño = tamaño
        self.coord = []
        self.orient = -1
        self.destroyed = False
        # se define qué tipo de barco es según su tamaño
        self.tipo = "Submarino" if (
            self.tamaño == 1) else "Destructor" if self.tamaño == 2 else "Crucero" if self.tamaño == 3 else "Portaaviones"

    def __str__(self):
        return self.tipo

    def set_destroyed(self):
        self.destroyed = True

    def is_destroyed(self):
        destroyed = True
        for coord in self.coord:
            if str(coord[1]) == "False":
                destroyed = False
                break
        return destroyed

    def mod_coord(self, x, y):
        pos = 0
        for coord in self.coord:
            if str(coord[0]) == str(f"({x}, {y})"):
                coord = [f"{x,y}", True]
                break
            pos += 1
        self.coord[pos][1] = True

    def set_coord(self, x, y):
        self.coord.append([f"{x,y}", False])

    def get_coord(self):
        co = []
        for coord in self.coord:
            co.append(coord[0])
        return co

    def set_orient(self, o):
        self.orient = o

class Jugador:
    def __init__(self, nombre,board_size, n1, n2, n3, n4) -> None:        
        self.SPACE=" "
        self.nombre = nombre
        self.barcos = []  # arreglo de barcos del jugador
        self.board_size=board_size
        self.matriz = self.obtener_matriz()  # genera una matriz vacía para el jugador        
        # se agregan tantos barcos haya según la cantidad de cada uno
        for i in range(n1):
            self.barcos.append(Barco(1))

        for i in range(n2):
            self.barcos.append(Barco(2))

        for i in range(n3):
            self.barcos.append(Barco(3))
        for i in range(n4):
            self.barcos.append(Barco(4))
        # se ubican los barcos en la matriz del jugador
        for barco in self.barcos:
            self.ubicar_barco(self.matriz, barco)
            
            #Para imprimir las coordenadas de los barcos si desea hacer pruebas
            print(barco)
            print(barco.get_coord())

    def obtener_matriz(self):  # se inicializa una matriz vacía de acuerdo al número de filas y columnas
        matriz = []
        for i in range(self.board_size):
            matriz.append([])
            for j in range(self.board_size):
                matriz[i].append(self.SPACE)
        return matriz
    
    def __str__(self):
        return str(self.matriz)

    def is_lose(self):
        perder = True
        for barco in self.barcos:
            if barco.destroyed == False:
                perder = False
                break
        return perder

        # función que ubica aleatorialmente un barco (no se detiene hasta que logra ubicarlo en el tablero)
    def ubicar_barco(self, matriz, barco):
        while True:
            x = random.randint(0, self.board_size-1)
            y = random.randint(0, self.board_size-1)
            # variable que de forma aleatoria determina la orientación del barco
            orientacion = random.randint(0, 1)
            # se verifica que en las coordenadas obtenidas no haya ningún otro barco
            if self.is_espacio(x, y, matriz):
                if barco.tamaño == 1:  # si el barco es de tamaño 1 no importa la orientación por ende se ubica en la matriz
                    matriz[x][y] = str(barco.tamaño)
                    barco.set_coord(x, y)
                    break
                if orientacion == 1:  # Si la orientación es horizontal
                    # se valida que sea posible ubicar el barco en la matriz según su tamaño
                    if barco.tamaño == 2 and self.is_rango(x, y+1):
                        # se valida que no hayan barcos en las posiciones que se ubicará el barco
                        if self.is_espacio(x, y+1, matriz):
                            # se ubica el barco en su posición
                            matriz[x][y] = str(barco.tamaño)
                            matriz[x][y+1] = str(barco.tamaño)
                            # se asignan las coordenadas del barco
                            barco.set_coord(x, y)
                            barco.set_coord(x, y+1)
                            barco.set_orient(orientacion)
                            break
                    if barco.tamaño == 3 and self.is_rango(x, y+1) and self.is_rango(x, y-1):
                        if self.is_espacio(x, y+1, matriz) and self.is_espacio(x, y-1, matriz):
                            matriz[x][y] = str(barco.tamaño)
                            matriz[x][y+1] = str(barco.tamaño)
                            matriz[x][y-1] = str(barco.tamaño)
                            barco.set_coord(x, y)
                            barco.set_coord(x, y+1)
                            barco.set_coord(x, y-1)
                            barco.set_orient(orientacion)
                            break
                    if barco.tamaño == 4 and self.is_rango(x, y+1) and self.is_rango(x, y+2) and self.is_rango(x, y-1):
                        if self.is_espacio(x, y+1, matriz) and self.is_espacio(x, y+2, matriz) and self.is_espacio(x, y-1, matriz):
                            matriz[x][y] = str(barco.tamaño)
                            matriz[x][y+1] = str(barco.tamaño)
                            matriz[x][y-1] = str(barco.tamaño)
                            matriz[x][y+2] = str(barco.tamaño)
                            barco.set_coord(x, y)
                            barco.set_coord(x, y+1)
                            barco.set_coord(x, y-1)
                            barco.set_coord(x, y+2)
                            barco.set_orient(orientacion)
                            break
                else:  # si la orientación es vertical
                    if barco.tamaño == 2 and self.is_rango(x+1, y):
                        if self.is_espacio(x+1, y, matriz):
                            matriz[x][y] = str(barco.tamaño)
                            matriz[x+1][y] = str(barco.tamaño)
                            barco.set_coord(x, y)
                            barco.set_coord(x+1, y)
                            barco.set_orient(orientacion)
                            break
                    if barco.tamaño == 3 and self.is_rango(x+1, y) and self.is_rango(x-1, y):
                        if self.is_espacio(x+1, y, matriz) and self.is_espacio(x-1, y, matriz):
                            matriz[x][y] = str(barco.tamaño)
                            matriz[x+1][y] = str(barco.tamaño)
                            matriz[x-1][y] = str(barco.tamaño)
                            barco.set_coord(x, y)
                            barco.set_coord(x+1, y)
                            barco.set_coord(x-1, y)
                            barco.set_orient(orientacion)
                            break
                    if barco.tamaño == 4 and self.is_rango(x+1, y) and self.is_rango(x+2, y) and self.is_rango(x-1, y):
                        if self.is_espacio(x+1, y, matriz) and self.is_espacio(x+2, y, matriz) and self.is_espacio(x-1, y, matriz):
                            matriz[x][y] = str(barco.tamaño)
                            matriz[x+1][y] = str(barco.tamaño)
                            matriz[x-1][y] = str(barco.tamaño)
                            matriz[x+2][y] = str(barco.tamaño)
                            barco.set_coord(x, y)
                            barco.set_coord(x+1, y)
                            barco.set_coord(x-1, y)
                            barco.set_coord(x+2, y)
                            barco.set_orient(orientacion)
                            break

    def is_rango(self, x, y):  # valida que las coordenadas dadas estén en el rango de las filas y columnas
        return x >= 0 and x <= self.board_size-1 and y >= 0 and y <= self.board_size-1

    def is_espacio(self, x, y, matriz):  # indica si en las coordenadas dadas hay espacio vacío
        return matriz[x][y] == self.SPACE