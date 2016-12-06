

import pygame, sys, time, random, pickle, shelve


#kommande raderna beskriver grundlägande saker för pygame
#

pygame.init() #krav för att pygame ska funka
FPS =30 #frames per second, antalet gånger skärmen updateras
clock=pygame.time.Clock() #bra för senare bruk

#färger som konstanter som skrivs som tupler i RGB
BLACK=(0,0,0)#ska finnas fler färger i färdiga versionen, beskrivs i engelska med FÄRG_NYANS

SCREEN_SIZE= SCREEN_WIDTH,SKREEN_HEIGHT=(1280,720) #tuple/konstanter för fönstrets dimensionering
main_screen= pygame.display.set_mode(SCREEN_SIZE) #skapar skärmen som man ritar på


#nedan beskrivs generella funktioner for pygame så som att rita en text eller att göra en knapp
#genelt så skrivs funktionerna med argumenten i ordningen
#x kordinat, y kordinat, bredden, höjden för det som ritas på skärmen
#notera att i pygame beskrivs oftast kordinaten för något med det som är högst up till vänster

def message(x,y,font_size,text,font,color) :
    #ritar ett text medelande på main_screen
    pass

def message_box(x,y,width,height,text,color) :
    #ritar en ruta på main_screen med en text på
    pass

def text_button(x,y,width,height,text,color,active_color,action,action_arguments) :
    #funktionen ritar en rektangulär knapp på main_screen
    #active_color syftar på när musen är på knappen
    #action är funktionen man vill köra när man trycker på knappen
    #action_arguments är en tuple av dom argument som action ska ha
    pass

def close(state) :
    #stänger hela programet med eventuel funktion när det stängs
    #state syftar på vad som ska hända när programet stäng
    pass







class room (object) :
    #klass som beskriver varje rum som ett object
    #objektet ska inkludera, inehållet i rummet så som ett hål
    def init(self,roomx,roomy,content=None,visited=None) :
        


class stats (object) : #klass för att spara statistik och ge highscore
    #klassen ska inkludera namn, svårighetsgraden, och antalet darg

    def __init__(self,difficulty=None,name=None,moves=0,found_rooms=1):
        self.difficulty=difficulty
        self.name=name
        self.moves=moves
        self.found_rooms=found_rooms

    def __str__(high_score=False) : #skriverut statistik om spelaren
        #om highscore är True så ska info relevant för spelarens highscore returneras
        pass
    
    def add_move(self) : #läggertill ett drag och returnerar antalet drag
        pass

    def get_highscore(self):#räknar ut ett highscore efter lämplig algoritm
        pass

    def get_statistics(self):#ger statistik som anses vara relevant under spelets gång
        pass

    def set_name(self): #ändrar namn, bra att ha när spelarens highscore ska sparas
        #men behövs ej under spelets gång för at visa statistik
        pass

