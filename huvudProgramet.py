import pygame, sys, time, random, pickle, shelve, math
import wumpusclasses

#kommande raderna beskriver grundlägande saker för pygame

pygame.init() #krav för att pygame ska funka
FPS =30 #frames per second, antalet gånger skärmen updateras
clock=pygame.time.Clock() #bra för senare bruk

#färger som konstanter som skrivs som tupler i RGB
BLACK       =(0,0,0)
GREY        =(128,128,128)
GREY_DARK   =(50,50,50)
WHITE       =(255,255,255)
RED         =(255,0,0)
RED_LIGHT    =(255,100,100)
RED_DARK    =(150,0,0)
YELLOW      =(255,255,0)
YELLOW_LIGHT=(255,255,100)
YELLOW_DARK =(100,100,0)
GREEN       =(0,255,0)
GREEN_LIGHT =(100,255,100)
GREEN_DARK  =(0,150,0)
BLUE        =(0,0,255)
BLUE_LIGHT  =(100,100,255)
BLUE_DARK   =(0,0,150)

SCREEN_SIZE= SCREEN_WIDTH,SKREEN_HEIGHT=(1280,720) #tuple/konstanter för fönstrets dimensionering
main_screen= pygame.display.set_mode(SCREEN_SIZE) #skapar skärmen som man ritar på
BOARD_WIDTH,BOARD_HEIGHT=16,12 #antalet rutor spelplanen har

#nedan beskrivs generella funktioner for pygame så som att rita en text eller att göra en knapp
#genelt så skrivs funktionerna med argumenten i ordningen
#x kordinat, y kordinat, bredden, höjden för det som ritas på skärmen
#notera att i pygame beskrivs oftast kordinaten för något med det som är högst up till vänster

def message(x,y,font_size,text,font='comicsansms',color=BLACK) :#ritar ett text medelande på
    #main_screen, notera att x,y är i mitten av texten
    font_object=pygame.font.SysFont(font,font_size)
    text_surface_object=font_object.render(text,True,color)
    text_rect=text_surface_object.get_rect()
    text_rect.center=(x,y)
    main_screen.blit(text_surface_object,text_rect)
def message_box(x,y,width,height,text,color,font=None,text_color=BLACK) :#ritar en ruta på
    #main_screen med en text på
    pygame.draw.rect(main_screen,color,(x,y,width,height))#ritar rektangeln
    #nedan kommer min gissning på lagom fontstorlek så att texten inte kommer utanför
    #gissat via try and error så den är inte perfekt
    font_height=int(height/2)#gissning på fontsize avseende på höjd
    font_width=int(1.8*width/len(text))#gissnig på storlek avseende på brädd
    if font_height < font_width :
        font_size=font_height
    else :
        font_size=font_size
    message(x+width/2, y+height/2, font_size, text, font,text_color)#ritar texten på knappen
def text_button(x,y,width,height,text,color,active_color,action=None,action_arguments=()) :
    #funktionen ritar en rektangulär knapp på main_screen
    #active_color syftar på när musen är på knappen
    #action är funktionen man vill köra när man trycker på knappen
    #action_arguments är en tuple av dom argument som action ska ha
    mouse_coordinates=pygame.mouse.get_pos()#ger x,y för musen
    mouse_click=pygame.mouse.get_pressed()#avgör om musen är klickad
    if x+width> mouse_coordinates[0] >x and y+height> mouse_coordinates[1] >y:#musen på knappen
        message_box(x,y,width,height,text,active_color)#ritar ruta med nyans när mus är höver
        if click[0]==True and action !=None :#om man klickar på knappen
            action(*action_arguments) #nu körs funktionen
    else:
        message_box(x,y,width,height,text,color)
def close(state=None) :#stänger hela programet med eventuel funktion när det stängs
    #state syftar på vad som ska hända när programet stäng exempelvis kan ett medelande duka upp
    pygame.quit() #stänger pygame modulen
    sys.exit() #stänger programet

#nedon kommer logik om själva spelet och spelplanen

#matrisen för spelplanen har x,y numrering som en matte matris fast med 00 uppe i högra hörnet

#nedan kommer lite logic för att generera rummen och visa dom
#tanken bakom rummen är att dom ska hålla sig inom en BOARD_WIDTH x BOARD_HEIGHT matris där alla rutor är rum
#och rummen är 60x60 pixlar. rummen slumpas där ett rum kan ha 4-1 in/utgångar och varje
#rum kan ha ett inehåll så som hål eller flygande råttor.

#generelt sätt skrivs riktningarna i ordningen med upp först och sedan som klockan om det
#ska inkludera siffror så blir upp 0 och sedan ökar det med 1 i ordningen ovan

    

def add_interior():#lägger till slumpat inehåll i den slumpade laburinten så som hål
    pass
def paint_room(x,y,directions,content=None,near_content=()) :#ritar ett rum beroende på ienhåll och riktningarna
    #som det finns gångar. ritas vid x,y är kordinaten för rummet
    #rummet är 60X60 pixlar
    #diections or en lista eller tupple som beskriver alla riktningarna från rummet
    #content är innehåll
    #rummet blir en cirkel med rktanglar som sticker ut
    if len(near_content)==0 :
        color=GREY
    elif True :#near_content.count('hole') and near_content.count('bat') :
        color=GREEN
    radius=20
    hole_radius=10
    path_width=20
    pygame.draw.rect(main_screen,BLACK,(x,y,60,60)) #ritar svart ruta som bakgrund
    pygame.draw.circle(main_screen,color,(x+30,y+30),radius)
    #obs semikodupprepning
    for direction in directions :
        #koduprepning?
        if direction == 0 :#ritar uppåt väg
            pygame.draw.rect(main_screen,color,(x+30-path_width/2,y,path_width,30))
        elif direction==1 :#ritar åt höger 
            pygame.draw.rect(main_screen,color,(x+30,y+30-path_width/2,30,path_width))
        elif direction==2 :#ritar ner
            pygame.draw.rect(main_screen,color,(x+30-path_width/2,y+30,path_width,30))
        else : #ritar åt vänster
            pygame.draw.rect(main_screen,color,(x,y+30-path_width/2,30,path_width))
    if content=='hole' :#om det finns ett hål
        pygame.draw.circle(main_screen,BLACK,(x+30,y+30),hole_radius)
    elif content=='bat' :#om det finn fladdermöss, ritan nån fladdermus grej
        pygame.draw.polygon(main_screen,BLUE,((x+30,y+30),(x+40,y+20),(x+50,y+30),(x+30,y+40),(x+10,y+30),(x+20,y+20)))
    elif content=='arrows' :
        pygame.draw.rect(main_screen,RED_DARK,(x+15,y+25,30,10))
        
def display_rooms(matrix):#funktion som går igenom matrisen för alla slumpade rum och ritar planen
    #om ett rum inte ska visas eftersom det är obesökt eller det står None i matrisen så
    #ritas en svart ruta eller liknande

    #om rummet är besökt ska det ritas en bild
    #bilden jag tänkt mig ska ritas är den cirkel, cirkeln ska få rektanglar åt alla hål som det
    #finns gångar, det är möjligt att jag snyggar till det senare
    #för att visa inehållet ritar jag något extra,  typ svart ring för hål etc

    #jägaren och Wumpus ritas separat
    for x in range(BOARD_WIDTH) :
        for y in range(BOARD_HEIGHT) :
            if matrix.call_object(x,y)==None or not (matrix.call_object(x,y)).room_visited() :
                pygame.draw.rect(main_screen,BLACK,(x*60,y*60,60,60))#ritar svart ruta
            else:
                path_directions=(matrix.call_object(x,y)).path_directions()
                content=(matrix.call_object(x,y)).get_content()
                near_content=matrix.get_near_content(x,y)
                paint_room(x*60,y*60,path_directions,content,near_content)

                

#kommer använda mig utav klasser för att få karaktärernas x,y samt svårighetsgrad 



def hunter_shoot(direction):#funktion som körs när man ska skjuta
    pass
def display_hunter():#en bild av jägaren beroende på var på planen han ska vara
    pass

def taskbar():#funktionen som kör för att visa aktivitetsfältet i spelet
    #aktivitetsfältet blir 320x720 pixlar och ska nkludera knappar för vilket hål man ska gå till
    #och information om vad jägaren känner i omgivningen
    pass
def run_game() :#kör spelet, börjar med att generera plan sedan ge spelaren alternativ etc
    pass
#nedan kommer massa info om sidor annat än spelsidan
def win_screen () :#funktionen som dyker upp när man vunnit och ska skriva sitt namn
    #det finns möjlighet att jag importerar en modul för text input i pygame, annars får den köras
    #sominput i kommandotolken
    pass
def save_score() :#funktionen som kör när man ska spara spelerens highscore i det
    #separata dokumentet
    pass
def high_score_screen():#funktionen som körs när man ska se föregående spelares high score 
    pass
def game_mode_menu_screen():#sidan menyn som dykerupp när man ska välja svårighetsgraden
    pass
def manual_screen (): #funktion man kör för att visa instruktions sidan
    #kommer mest vara en text med en knapp som leder tillbaks till menyn eller stänger programet
    pass


matrix = wumpusclasses.Room_matrix(BOARD_WIDTH,BOARD_HEIGHT) #matrisen som spelet utspelas på som
#representeras i klassen Matrix
difficulty=wumpusclasses.Difficulty('hard')
matrix.set_difficulty(difficulty)
matrix.generate_rooms()
matrix.add_all_content()
#nedan är test, för anti bugg mgenerate_rooms ()
while True :
    for event in pygame.event.get() :
        if event.type== pygame.QUIT :
            close ()
    main_screen.fill(WHITE)
    display_rooms(matrix)
    pygame.display.update()





#nedan finns paperskorgen, kan vara bra när man vill ha tillbaks grejer
