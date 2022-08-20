import pygame

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    def draw_cursor(self):
        self.game.draw_text('*', 25, self.cursor_rect.x, self.cursor_rect.y, self.game.WHITE)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.offset = - 150
        self.background=pygame.image.load("img/BattleShip.png")        
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 150
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 190
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 230
        self.exitx, self.exity = self.mid_w, self.mid_h + 270
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            # self.game.display.fill(self.game.BLACK)
            self.game.draw_image(self.background, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2)            
            self.game.draw_text("Start Game", 30, self.startx, self.starty, self.game.WHITE)
            self.game.draw_text("Options", 30, self.optionsx, self.optionsy, self.game.WHITE)
            self.game.draw_text("Credits", 30, self.creditsx, self.creditsy, self.game.WHITE)
            self.game.draw_text("Exit", 30, self.exitx, self.exity, self.game.WHITE)
            self.draw_cursor()
            self.blit_screen()


    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Exit'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
        elif self.game.MOUSE_MOVE:
            mousex=self.game.mouse_position[0]
            mousey=self.game.mouse_position[1]
            if(mousex>self.startx+self.offset and mousex<self.startx-self.offset and mousey>self.starty-25 and mousey<self.starty+25):
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'                
            elif(mousex>self.optionsx+self.offset and mousex<self.optionsx-self.offset and mousey>self.optionsy-25 and mousey<self.optionsy+25):
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif(mousex>self.creditsx+self.offset and mousex<self.creditsx-self.offset and mousey>self.creditsy-25 and mousey<self.creditsy+25):
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif(mousex>self.exitx+self.offset and mousex<self.exitx-self.offset and mousey>self.exity-25 and mousey<self.exity+25):
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Exit'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.curr_menu=self.game.input_menu
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            elif self.state == 'Exit':
                self.game.running, self.game.playing = False, False
                self.game.curr_menu.run_display = False
            self.run_display = False
        elif self.game.MOUSE_DOWN:
            mousex=self.game.mouse_position[0]
            mousey=self.game.mouse_position[1]
            if(mousex>self.startx+self.offset and mousex<self.startx-self.offset and mousey>self.starty-25 and mousey<self.starty+25):
                self.game.curr_menu=self.game.input_menu                
            elif(mousex>self.optionsx+self.offset and mousex<self.optionsx-self.offset and mousey>self.optionsy-25 and mousey<self.optionsy+25):
                self.game.curr_menu = self.game.options
            elif(mousex>self.creditsx+self.offset and mousex<self.creditsx-self.offset and mousey>self.creditsy-25 and mousey<self.creditsy+25):
                self.game.curr_menu = self.game.credits
            elif(mousex>self.exitx+self.offset and mousex<self.exitx-self.offset and mousey>self.exity-25 and mousey<self.exity+25):
                self.game.running, self.game.playing = False, False
                self.game.curr_menu.run_display = False
            self.run_display = False

class InputDataMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.backx, self.backy=50, 30
        self.playx, self.playy=self.mid_w, self.mid_h+300
        self.list1x, self.list1y = self.mid_w-250, self.mid_h-220
        self.list2x, self.list2y = self.mid_w+250, self.mid_h-220
        self.list3x, self.list3y = self.mid_w-250, self.mid_h+150
        self.list4x, self.list4y = self.mid_w+250, self.mid_h+150
        self.list1 = OptionBox(self.list1x, self.list1y, 130, 30, (25, 137, 255), (100, 200, 255), pygame.font.Font(self.game.font_name,20),["1", "2", "3", "4"])
        self.list2 = OptionBox(self.list2x, self.list2y, 130, 30, (25, 137, 255), (100, 200, 255), pygame.font.Font(self.game.font_name,20), ["0","1", "2", "3", "4"])
        self.list3 = OptionBox(self.list3x, self.list3y, 130, 30, (25, 137, 255), (100, 200, 255), pygame.font.Font(self.game.font_name,20), ["0","1", "2", "3", "4"])
        self.list4 = OptionBox(self.list4x, self.list4y, 130, 30, (25, 137, 255), (100, 200, 255), pygame.font.Font(self.game.font_name,20), ["0","1", "2", "3", "4"])
    def display_menu(self):
        self.run_display = True
        
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.list1.update(self.game.MOUSE_DOWN, self.game.mouse_position)
            self.list2.update(self.game.MOUSE_DOWN, self.game.mouse_position)
            self.list3.update(self.game.MOUSE_DOWN, self.game.mouse_position)
            self.list4.update(self.game.MOUSE_DOWN, self.game.mouse_position)           
            self.game.display.fill((255, 255, 255))
            self.list1.draw(self.game.display)
            self.list2.draw(self.game.display)
            self.list3.draw(self.game.display)
            self.list4.draw(self.game.display)
            self.game.draw_text("Number of ships", 30, self.playx, 20, self.game.BLACK)
            self.game.draw_text("Size 1", 20, self.list1x, self.list1y-35, self.game.BLACK)
            self.game.draw_text("Size 2", 20, self.list2x, self.list2y-35, self.game.BLACK)
            self.game.draw_text("Size 3", 20, self.list3x, self.list3y-35, self.game.BLACK)
            self.game.draw_text("Size 4", 20, self.list4x, self.list4y-35, self.game.BLACK)
            self.game.draw_text("Back", 20, self.backx, self.backy, self.game.BLACK)
            self.game.draw_text("play", 40, self.playx, self.playy, self.game.BLACK)           
            self.blit_screen()
    
    def check_input(self):
        if self.game.MOUSE_DOWN:
                mousex=self.game.mouse_position[0]
                mousey=self.game.mouse_position[1]
                if(mousex>self.backx-40 and mousex<self.backx+40 and mousey>self.backy-15 and mousey<self.backy+15):
                    self.game.curr_menu = self.game.main_menu
                    self.run_display = False
                elif(mousex>self.playx-80 and mousex<self.playx+80 and mousey>self.playy-20 and mousey<self.playy+20):                    
                    self.game.curr_menu=self.game.main_menu
                    self.game.n_ship1 = self.list1.selected+1
                    self.game.n_ship2 = self.list2.selected
                    self.game.n_ship3 = self.list3.selected
                    self.game.n_ship4 = self.list4.selected
                    self.run_display=False
                    self.game.playing=True


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.backx, self.backy=50, 30
        self.offset=-150
        self.state = 'Volume'
        self.soundx, self.soundy = self.mid_w, self.mid_h + 20        
        self.cursor_rect.midtop = (self.soundx + self.offset, self.soundy)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text("Back", 20, self.backx, self.backy, self.game.WHITE)
            self.game.draw_text('Options', 40, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 60, self.game.WHITE)
            self.game.draw_text("Sound "+("on" if self.game.SOUND else "off"), 30, self.soundx, self.soundy, self.game.WHITE)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.MOUSE_DOWN:
                mousex=self.game.mouse_position[0]
                mousey=self.game.mouse_position[1]
                if(mousex>self.backx-40 and mousex<self.backx+40 and mousey>self.backy-15 and mousey<self.backy+15):
                    self.game.curr_menu = self.game.main_menu
                    self.run_display = False
                elif(mousex>self.soundx+self.offset and mousex<self.soundx-self.offset and mousey>self.soundy-25 and mousey<self.soundy+25):
                    self.game.SOUND=not self.game.SOUND
        elif self.game.START_KEY:
            # TO-DO: Create a Volume Menu and a Controls Menu
            self.game.SOUND=not self.game.SOUND
            pass

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.offset=-50
        self.backx, self.backy=50, 30
    def display_menu(self):
        self.run_display = True

        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            elif self.game.MOUSE_DOWN:
                mousex=self.game.mouse_position[0]
                mousey=self.game.mouse_position[1]
                if(mousex>self.backx+self.offset and mousex<self.backx-self.offset and mousey>self.backy-15 and mousey<self.backy+15):
                    self.game.curr_menu = self.game.main_menu
                    self.run_display = False
                    
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("Back", 20, self.backx, self.backy, self.game.WHITE)
            self.game.draw_text('Credits', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20, self.game.WHITE)
            self.game.draw_text('Made by Mateo Aristizabal', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10, self.game.WHITE)
            self.game.draw_text('Universidad del Norte', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 30, self.game.WHITE)
            self.blit_screen()


class OptionBox():

    def __init__(self, x, y, w, h, color, highlight_color, font, option_list, selected=0):
        self.color = color
        self.highlight_color = highlight_color
        self.rect = pygame.Rect(0, 0, w, h)
        self.rect.center=(x,y)
        self.font = font
        self.option_list = option_list
        self.selected = selected
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, surf):
        pygame.draw.rect(
            surf, self.highlight_color if self.menu_active else self.color, self.rect)
        pygame.draw.rect(surf, (0, 0, 0), self.rect, 2)
        msg = self.font.render(self.option_list[self.selected], 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center=self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.option_list):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(surf, self.highlight_color if i ==
                                 self.active_option else self.color, rect)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center=rect.center))
            outer_rect = (self.rect.x, self.rect.y + self.rect.height,
                          self.rect.width, self.rect.height * len(self.option_list))
            pygame.draw.rect(surf, (0, 0, 0), outer_rect, 2)
    
    def update(self, MOUSE_DOWN, mouse_pos):        
        self.menu_active = self.rect.collidepoint(mouse_pos)

        self.active_option = -1
        for i in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mouse_pos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        
        if MOUSE_DOWN:
            if self.menu_active:
                self.draw_menu = not self.draw_menu
            elif self.draw_menu and self.active_option >= 0:
                self.selected = self.active_option
                self.draw_menu = False
                return self.active_option
        return -1

class EndGameMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.mainmenux, self.mainmenuy=self.mid_w, self.game.DISPLAY_H-50

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()         
            self.game.display.fill((255, 255, 255))
            self.game.draw_text("Main menu", 20, self.mainmenux, self.mainmenuy, self.game.BLACK)
            self.game.draw_text("player 1 board", 20, self.mid_w/2-64, self.mid_h/2-20, self.game.BLACK)
            self.game.draw_text("player 2 board", 20, self.mid_w*1.5+32, self.mid_h/2-20, self.game.BLACK)
            self.game.draw_text("Player "+str(self.game.active_player+1) +" has won", 40, self.mid_w, 50, (127, 238, 50))
            for player in self.game.players:    
                for i in range(self.game.board_size):
                    for j in range(self.game.board_size):
                        pygame.draw.rect(self.game.display,self.game.BLACK, [(50 if player.name == 0 else self.mid_w+132) +j*32, self.mid_h/2+i*32, 32.5, 32.5], 1)
                        if(player.matriz[i][j] == self.game.MISSED_SHOT):                        
                            self.game.draw_image(pygame.transform.scale(self.game.missed_shot_img, (30, 30)), (50 if player.name == 0 else self.mid_w+132)+32*j+16, self.mid_h/2+32*i+16)                                        
                        elif(player.matriz[i][j] == self.game.SUCCESSFUL_SHOT):
                            self.game.draw_image(pygame.transform.scale(self.game.successful_shot_img, (30, 30)), (50 if player.name == 0 else self.mid_w+132)+32*j+16, self.mid_h/2+32*i+16)
            
            self.blit_screen()

    def check_input(self):
        if self.game.MOUSE_DOWN:
            mousex=self.game.mouse_position[0]
            mousey=self.game.mouse_position[1]
            if(mousex>self.mainmenux-40 and mousex<self.mainmenux+40 and mousey>self.mainmenuy-15 and mousey<self.mainmenuy+15):
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
    
    # def check_destroyed(self):
    #     # Se recorren todos los barcos para ver cuales fueron destruidos y mostrarlos
    #     for barco in self.players[self.opposite_player].barcos:
    #         if barco.is_destroyed():
    #             # Si es un submarino no tenemos que mirar la orientacion
    #             if barco.tamaño == 1:
    #                 self.draw_image(self.ship1_img, 10+65*int(barco.get_coord()[0][4])+32, 20+65*int(barco.get_coord()[0][1])+32)
    #             # Si la orientacion es horizontal
    #             if barco.orient == 1:
    #                 # Si es un destructor
    #                 if barco.tamaño == 2:
    #                     self.draw_image(pygame.transform.rotate(self.ship2_img , 90), 10+65*(int(barco.get_coord()[0][4])+1), 53+65*int(barco.get_coord()[0][1]))                        
    #                 # Si es un crucero
    #                 elif barco.tamaño == 3:
    #                     self.draw_image(pygame.transform.rotate(self.ship3_img , 90), 10+65*(int(barco.get_coord()[2][4])+1.5), 53+65*int(barco.get_coord()[2][1]))
    #                 # Si es un portaaviones
    #                 elif barco.tamaño == 4:
    #                     self.draw_image(pygame.transform.rotate(self.ship4_img , 90), 10+65*(int(barco.get_coord()[2][4])+2), 53+65*int(barco.get_coord()[2][1]))                        
    #             # Si la orientacion es vertical
    #             elif barco.orient == 0:
    #                 # Si es un destructor
    #                 if barco.tamaño == 2:
    #                     self.draw_image(self.ship2_img, 43+65*int(barco.get_coord()[0][4]), 20+65*(int(barco.get_coord()[0][1])+1))                        
    #                 # Si es un crucero
    #                 elif barco.tamaño == 3:
    #                     self.draw_image(self.ship3_img, 43+65*int(barco.get_coord()[2][4]), 20+65*(int(barco.get_coord()[2][1])+1.5))
    #                 # Si es un portaaviones
    #                 elif barco.tamaño == 4:
    #                     self.draw_image(self.ship4_img, 43+65*int(barco.get_coord()[2][4]), 20+65*(int(barco.get_coord()[2][1])+2))



