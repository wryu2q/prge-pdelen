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
GREY_LIGHT  =(200,200,200)
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
BOARD_WIDTH,BOARD_HEIGHT=15,12 #antalet rutor spelplanen har

#nedan beskrivs generella funktioner for pygame så som att rita en text eller att göra en knapp
#genelt så skrivs funktionerna med argumenten i ordningen
#x kordinat, y kordinat, bredden, höjden för det som ritas på skärmen
#notera att i pygame beskrivs oftast kordinaten för något med det som är högst up till vänster

def message(x,y,font_size,text,font='comicsansms',color=BLACK,place_corner=False) :#ritar ett text
    #medelande på main_screen, notera att x,y är i mitten av texten om inte place_corner är True
    font_object=pygame.font.SysFont(font,font_size)
    text_surface_object=font_object.render(text,True,color)
    text_rect=text_surface_object.get_rect()
    if place_corner : #placerar textens x,y i hörnet
        text_rect.topleft=(x,y)
    else:
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
        font_size=font_height
    message(x+width/2, y+height/2, font_size, text, font,text_color)#ritar texten på knappen
def text_button(x,y,width,height,text,color,active_color,action=None,action_arguments=(),mouse_click=None) :
    #funktionen ritar en rektangulär knapp på main_screen
    #active_color syftar på när musen är på knappen
    #action är funktionen man vill köra när man trycker på knappen
    #action_arguments är en tuple av dom argument som action ska ha
    mouse_coordinates=pygame.mouse.get_pos()#ger x,y för musen
    if mouse_click==None :
        mouse_click=pygame.mouse.get_pressed()[0]#avgör om vänsterclick är nere
    else :
        mouse_click=mouse_click#tar in om musen ska klickas
    if x+width> mouse_coordinates[0] >x and y+height> mouse_coordinates[1] >y:#musen på knappen
        message_box(x,y,width,height,text,active_color)#ritar ruta med nyans när mus är höver
        if mouse_click==True and action !=None :#om man klickar på knappen, borde vara på relsea
            action (*action_arguments) #nu körs funktionen
        if mouse_click==True :
            return True #så man vet att en knapp är tryckt
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

def paint_room(x,y,directions,content=None,near_content=()) :#ritar ett rum beroende på ienhåll och riktningarna
    #som det finns gångar. ritas vid x,y är kordinaten för rummet
    #rummet är 60X60 pixlar
    #diections or en lista eller tupple som beskriver alla riktningarna från rummet
    #content är innehåll
    #rummet blir en cirkel med rktanglar som sticker ut

    #tänk för i helvette på att inte ha samma ska 2 gånger så att vi inte gör om misstaget
    if near_content.count('hole') and near_content.count('bat') :
        color=BLUE_DARK
    elif near_content.count('hole') :
        color=GREY_DARK
    elif near_content.count('bat') :
        color=BLUE
    else:
        color=GREY
        
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
        pygame.draw.polygon(main_screen,BLUE_LIGHT,((x+30,y+30),(x+40,y+20),(x+50,y+30),(x+30,y+40),(x+10,y+30),(x+20,y+20)))
    elif content=='arrows' :
        pygame.draw.rect(main_screen,RED_DARK,(x+15,y+25,30,10))
        
def display_rooms(night_vision=False):#funktion som går igenom matrisen för alla slumpade rum och ritar planen
    #om ett rum inte ska visas eftersom det är obesökt eller det står None i matrisen så
    #ritas en svart ruta eller liknande

    #om rummet är besökt ska det ritas en bild
    #bilden jag tänkt mig ska ritas är den cirkel, cirkeln ska få rektanglar åt alla hål som det
    #finns gångar, det är möjligt att jag snyggar till det senare
    #för att visa inehållet ritar jag något extra,  typ svart ring för hål etc

    #jägaren och Wumpus ritas separat
    for x in range(BOARD_WIDTH) :
        for y in range(BOARD_HEIGHT) :
            if matrix.call_object(x,y)==None or not(matrix.call_object(x,y).room_visited() or night_vision) :
                pygame.draw.rect(main_screen,BLACK,(x*60,y*60,60,60))#ritar svart ruta
            else:
                path_directions=(matrix.call_object(x,y)).path_directions()
                content=(matrix.call_object(x,y)).get_content()
                
                near_content=matrix.get_near_content(x,y)
                paint_room(x*60,y*60,path_directions,content,near_content)

#kommer använda mig utav klasser för att få karaktärernas x,y samt svårighetsgrad 

def paint_wumpus () :
    color=RED
    x=wumpus.get_x()
    y=wumpus.get_y()
    pygame.draw.circle(main_screen,color,(x*60+30,y*60+30),25)
def paint_hunter (hunter) :
    x=hunter.get_x()
    y=hunter.get_y()
    pygame.draw.circle(main_screen,YELLOW,(x*60+30,y*60+30),25)
    

def direction_to_text(direction):#gör om en mattematisk riktning till text, dvs upp,höger...
    if direction==0 :
        return 'up'
    elif direction==1 :
        return 'right'
    elif direction==2 :
        return 'down'
    elif direction==3 :
        return 'left'

def hunter_senses_text():#texten som skrivs när jägaren är brevid wumpus eller hinder
    sense_list=hunter.hunter_senses(*wumpus.get_xy())
    text_list=[]
    for sense in list(set(sense_list)) :#loop som går igenom alla unika element
        if sense=='wumpus' :
            text_list.append('I feel the smell of Wumpus.')
        elif sense =='hole' :
            text_list.append('I feel the wind of a bottomless pit.')
        elif sense=='bat' :
            text_list.append('I hear the sound of flying rats.')
    return text_list

def senses_text_box (x,y,width=350,height=150,color=BLUE_LIGHT):
    #message(x,y,font_size,text,font='comicsansms',color=BLACK,place_corner=False) 
    
    font_size=20
    font='comicsansms'
    text_color=BLACK
    space_between_text= 2
    text_height=(font_size*4/3) + space_between_text
    pygame.draw.rect(main_screen,color,(x,y,width,height))#ritar ruttan texten är på
    turn =0#hur många gånger man skrivit en text
    for text in hunter_senses_text() :
        message(x,y+turn*text_height,font_size,text,font,text_color,True)
        turn+=1
         

def hunter_buttons (x,y,mouse_click) :#knappar för spelet och triggar att wumpus ska röra sig
    #är tänkt att knapparna ska ligga som ett kors där skjut är i mitten och gå runt om
    button_dimension =100 #bredd och höjd på var knapp
    between_space=10#rummet mellan alla knappar
    #nedan beskrivs koordinaten för knapparnas kollektiva övre vänstra hörn dvs det är ingen knapp
    #där men men som grupp blir det ett hörn
    collective_corner_xy=collective_corner_x,collective_corner_y=x,y
    color=BLUE#färg på knappen
    active_color=BLUE_LIGHT#färg när musen är över knappen
    impossible_action=False#om det inte går att göra handlingen
    impossoble_action_color=BLUE_DARK#knapp färg,musen på knapen men inte går att trycka
    #det blir ett kors med 9 möjliga positioner där bara 5 ska fyllas med knappar så vi gör en
    #loop där vi går igenom alla möjliga positioner och för en specifik position så beskrivs en text
    #och en funktion
    mouse_click=mouse_click#avgör om musen är tryckt
    end_turn=False# triggar att wumpus ska gå etc
    shoot=False
    for turn in range(9) :#man går från vänster till höger upp till ner
        impossible_action=False
        got_click=False
        local_x=(turn%3)*(button_dimension + between_space)+collective_corner_x
        local_y=int(turn/3)*(button_dimension + between_space)+collective_corner_y  
        if turn ==1: #turn gör i ordnigen upp,V,H,N så jag hårdkådar riktning...gör matte va fan!!!
            direction=0
        elif turn ==3 :
            direction=3
        elif turn ==5 :
            direction=1
        elif turn ==7 :
            direction=2
        if turn==4 :#man ska skjuta
            text='shoot'
            if hunter.is_shooting() :#om han redan valt att skjuta
                impossible_action=True
            else :#han har valt att skjuta
                action=hunter.shoot_toggle
                action_argument=()

        elif turn%2 :# ska det finnas knapp rör dig knapp
            if turn%2==1 :#om man är på en riktning knapp
                text=direction_to_text(direction)
                if hunter.get_possible_directions().count(direction) == 0 :#kan inte gå åt hållet
                    impossible_action=True
                elif hunter.is_shooting() :
                    action=None
                    action_argument=()
                else :
                    action=hunter.hunter_move
                    action_argument=(direction,)    
        else :
            continue
        if impossible_action :# om det inte går blir knappen en textruta
            message_box(local_x,local_y,button_dimension,button_dimension,text,impossoble_action_color)
        else :
            got_click=text_button(local_x,local_y,button_dimension,button_dimension,text,color,active_color,action,action_argument,mouse_click)
            
        if got_click and turn%2 :
            if hunter.hunter_shoot(direction,*wumpus.get_xy()):#skjuter coh träffar
                return 'win'
            end_turn=True
    if end_turn :#om man flytta sig eller skjuter
        if hunter.got_killed(*wumpus.get_xy()) :#om man dör av wumpus eller hål
            return 'dead'
        wumpus.wumpus_move(*hunter.get_xy()) #wumpus ska flytta sig 

            

def taskbar(mouse_click):#funktionen som kör för att visa aktivitetsfältet i spelet
    #aktivitetsfältet blir 320x720 pixlar och ska nkludera knappar för vilket hål man ska gå till
    #och information om vad jägaren känner i omgivningen
    taskbar_width=SCREEN_WIDTH-BOARD_WIDTH*60
    taskbar_left_edge=SCREEN_WIDTH-taskbar_width
    pygame.draw.rect(main_screen,GREEN,(taskbar_left_edge,0,taskbar_width,SCREEN_WIDTH))
    #x,y,width,height,text,color,active_color,action=None,action_arguments=()) :
    text_button(taskbar_left_edge+20,200,200,100,'wumpus go!',RED,RED_LIGHT,wumpus.wumpus_move,(hunter.get_xy()))#text för att se hur wumpus rör sig
    hunter_buttons(taskbar_left_edge+30,380,mouse_click)
    senses_text_box(taskbar_left_edge+20,20)
    

    
def run_game(new_difficulty='medium') :#kör spelet, börjar med att generera plan etc
    difficulty.change_difficulty(new_difficulty)
    print(difficulty)
    matrix.create_maze()
    
    night_vision=False
    show_wumpus=False
    wumpus.place_random_empty_room()
    hunter.place_random_empty_room()
    while True :
        mouse_click=False
        for event in pygame.event.get() :
            if event.type== pygame.QUIT :
                close ()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click=True
            if event.type == pygame.KEYDOWN :
                if event.key==pygame.K_n :
                    night_vision=not night_vision
                if event.key==pygame.K_m :
                    show_wumpus=not show_wumpus
        main_screen.fill(WHITE)
        display_rooms(night_vision)
        if show_wumpus :
            paint_wumpus()
        paint_hunter(hunter)
        taskbar(mouse_click)
        pygame.display.update()
        clock.tick(FPS)
    

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

#nedan börjar vi med att skapa objekt som sparas på heapen
matrix = wumpusclasses.Room_matrix(BOARD_WIDTH,BOARD_HEIGHT) #matrisen som spelet utspelas på som
#representeras i klassen Matrix
difficulty=wumpusclasses.Difficulty('easy')
matrix.set_difficulty(difficulty)
wumpus=wumpusclasses.Wumpus(matrix,difficulty)
hunter=wumpusclasses.Hunter(matrix,difficulty)

run_game ('hard')





#nedan finns paperskorgen, kan vara bra när man vill ha tillbaks grejer
