import pygame, sys,shelve#standard moduler i python
import wumpusclasses#min fil med klasser för spelet

import pygame_textinput #modul från en cool snubbe på github som kallas "Nearoo" se:
#https://github.com/Nearoo/pygame-text-input

#kommande raderna beskriver grundlägande saker för pygame

pygame.init() #krav för att pygame ska funka

#färger som konstanter som skrivs som tupler i RGB
BLACK       =(0,0,0)
GREY        =(128,128,128)
GREY_DARK   =(50,50,50)
GREY_LIGHT  =(200,200,200)
WHITE       =(255,255,255)
RED         =(255,0,0)
RED_LIGHT   =(255,100,100)
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

#nedan skapas några konstanter
SCREEN_SIZE= SCREEN_WIDTH,SCREEN_HEIGHT=(1280,720) #tuple/konstanter för fönstrets dimensionering
main_screen= pygame.display.set_mode(SCREEN_SIZE) #skapar skärmen som man ritar på
BOARD_WIDTH,BOARD_HEIGHT=15,12 #antalet rutor spelplanen har
BOARD_SQUARE_WIDTH,BOARD_SQUARE_HEIGHT=60,60#antalet pixlar som varje ruta får
FPS =30 #frames per second, antalet gånger i sekunden skärmen updateras
clock=pygame.time.Clock() #klocka för FPS i pygame

pygame.display.set_caption('Wumpus')#texten för spelrutan
window_icon=pygame.image.load('wumpus.png')
pygame.display.set_icon(window_icon)#bilden för spelrutan

#genelt så skrivs funktionerna med argumenten i ordningen
#x kordinat, y kordinat, bredden, höjden för det som ritas på skärmen
#notera att i pygame beskrivs oftast kordinaten för något med punkten som är högst up till vänster

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
    #nedan kommer min gissning på lagom fontstorlek så att texten inte kommer utanför rutan
    font_height=int(height/2)#gissning på fontsize avseende på höjd
    font_width=int(2*width/len(text))#gissnig på storlek avseende på brädd
    if font_height < font_width : #val av om vilken begränsning av texten som ska användas
        font_size=font_height
    else :
        font_size=font_width
    message(x+width/2, y+height/2, font_size, text, font,text_color)#ritar texten på knappen
    
def text_button(x,y,width,height,text,color,active_color,action=None,action_arguments=(),mouse_click=None) :
    #funktionen ritar en rektangulär knapp på main_screen
    #active_color syftar på när musen är på knappen
    #action är funktionen man vill köra när man trycker på knappen
    #action_arguments är en tuple av dom argument som action ska ha
    #mouse_click är om musknappen trycks(funkar utan men i sådana fall kan man stöta på problemet
    #att det är helatiden när musen är nere, man kansek bara vill ha på realese)
    mouse_coordinates=pygame.mouse.get_pos()#ger x,y för musen
    if mouse_click==None :
        mouse_click=pygame.mouse.get_pressed()[0]#avgör om vänsterclick är nere

    if x+width> mouse_coordinates[0] >x and y+height> mouse_coordinates[1] >y:#är musen på knappen?
        message_box(x,y,width,height,text,active_color)#ritar ruta med nyans när mus är över
        if mouse_click==True :#om man klickar på knappen
            if action !=None :#om det inte finns nån funktion ska inget köras
                action (*action_arguments) #nu körs funktionen
            return True #så man vet att en knapp är tryckts
    else:
        message_box(x,y,width,height,text,color)
        
def close_game(state=None) :#stänger hela programet med eventuel funktion när det stängs
    #state syftar på vad som ska hända när programet stäng exempelvis kan ett medelande dyka upp
    pygame.quit() #stänger pygame modulen
    sys.exit() #stänger programet

def key_command() :
    pressed_keys=pygame.key.get_pressed()#lista på 323 element,1 eller 0 för var tangentbords knapp
    ctrl_down= (pressed_keys[306] or pressed_keys[305])#höger eller vänster controll
    q_down=pressed_keys[113]#knappen q
    if ctrl_down :#är kontroll nere?
        if q_down :#ctrl q för att stänga
            close_game()
    
#nedon kommer logik om själva spelet och spelplanen

#mycket sparas i object på heapen, för att se alla object som skapas, se dom sista raderna i koden

#spelplanen genereras med hjälp av filen wumpusclasses.py som har massa klasser för att generera
#laburinter och hur det görs med rum etc, myckes förlitas på heapen och många klasser tar in object
#från andra klasser. Se wumpusclasses.py för hur det funkar och vilka metoder som kallas på

#rummen är 60x60 pixlar. rummen slumpas där ett rum kan ha 4-1 in/utgångar och varje
#rum kan ha ett inehåll så som hål eller flygande råttor eller pilar.

#generelt sätt skrivs riktningarna i ordningen med upp först och sedan som klockan om det
#ska inkludera siffror så blir upp 0 och sedan ökar det med 1 i ordningen ovan

def paint_room(x,y,directions,content=None,near_content=()) :#ritar ett rum beroende på ienhåll och
    #riktningarna. ritas vid x,y är kordinaten för rummet
    #rummet förväntas vara 60X60
    #diections or en lista eller tupple som beskriver alla riktningarna frön rummet
    #content är innehållet i rummet
    
    #rummet ritas som en cirkel med rektanglar som sticker ut, rummets färg beror på närliggande
    #inehåll och inehållet i rummet


#kodupprepning?
    #nedan är if komandom om vilken färg det ska vara beroende på närliggande grejer
    if near_content.count('hole') and near_content.count('bat') :
        color=BLUE_DARK
    elif near_content.count('hole') :
        color=GREY_DARK
    elif near_content.count('bat') :
        color=BLUE
    else:
        color=GREY
    radius=20#radien för cirkeln som ritas
    hole_radius=10#radien för hål
    path_width=20#brädden för varje gång
    pygame.draw.rect(main_screen,BLACK,(x,y,BOARD_SQUARE_WIDTH,BOARD_SQUARE_HEIGHT))#ritar svart bakgrund

    #obs semikodupprepning
    for direction in directions :#går igenom alla gångars riktningar som ska ritas
#kodupprepning?
        
        if not direction%2 :#riktningen är vertical dvs gången går upp eller ner
            path_x=x+(BOARD_SQUARE_WIDTH-path_width)/2#avgör vart rutans x ska ritas
            path_y=y#avgör var rutans y ska ritas
            if direction==2 :#om det är ner så måste man lägga till lite på y
                path_y +=BOARD_SQUARE_HEIGHT/2
            rect_width=path_width#bredden på rektangeln som ritas
            rect_height=BOARD_SQUARE_HEIGHT/2#höjden på rektangeln som ritas
        else :#när det är verticalt, typ samma men annan konstant och bytta roller på x/y
            path_y=y+(BOARD_SQUARE_HEIGHT-path_width)/2
            path_x=x
            if direction==1 :
                path_x +=BOARD_SQUARE_WIDTH/2

            rect_width=BOARD_SQUARE_WIDTH/2
            rect_height=path_width
            
        pygame.draw.rect(main_screen,color,(path_x,path_y,rect_width,rect_height))
    
    pygame.draw.circle(main_screen,color,(int(x+BOARD_SQUARE_WIDTH/2),int(y+BOARD_SQUARE_HEIGHT/2)),radius)#ritar cirkeln i mitten    
    if content=='hole' :#om det finns ett hål
        pygame.draw.circle(main_screen,BLACK,(int(x+BOARD_SQUARE_WIDTH/2),int(y+BOARD_SQUARE_HEIGHT/2)),hole_radius)
    elif content=='bat' :#om det finns fladdermöss, ritan nån fladdermus grej
        pygame.draw.polygon(main_screen,BLUE_LIGHT,((x+30,y+30),(x+40,y+20),(x+50,y+30),(x+30,y+40),(x+10,y+30),(x+20,y+20)))
    elif content=='arrows' :#om det finns pilar
        pygame.draw.rect(main_screen,RED_DARK,(x+15,y+25,30,10))
        
def display_rooms(night_vision=False):#funktion som går igenom matrisen för alla slumpade rum och
    #ritar planen
    
    #om ett rum inte ska visas eftersom det är obesökt eller det står None i matrisen så
    #ritas en svart ruta eller liknande

    #om rummet är besökt ska det ritas en bild, som ritas med paint_room

    for x in range(BOARD_WIDTH) :#vi har en loop som går igenom varje x och y i matrisen beroende
        for y in range(BOARD_HEIGHT) :#på konstanterna av brädets volym, kallar dom x/y
            draw_x=x*BOARD_SQUARE_WIDTH #avgör vart x/y ska ritas som kordinat, beroende på
            draw_y=y*BOARD_SQUARE_HEIGHT#vilket x/y och pixelstorleken på var ruta
            if matrix.call_object(x,y)==None or not(matrix.call_object(x,y).room_visited() or night_vision) :
                #if ovan avgör om man ska rita svart ruta, ritar sen en svart ruta
                pygame.draw.rect(main_screen,BLACK,(draw_x,draw_y,BOARD_SQUARE_WIDTH,BOARD_SQUARE_HEIGHT))
            else:#om det ska ritas ett rumm
                #konstanterna tar riktningarna man kan ta i rummet samt inehåll
                path_directions=(matrix.call_object(x,y)).path_directions()#möjliga riktnninngar
                content=(matrix.call_object(x,y)).get_content()#rummets inehåll
                near_content=matrix.get_near_content(x,y)#närliggande inehäll
                
                paint_room(draw_x,draw_y,path_directions,content,near_content)#ritar rummet

#nedan ritas wumpus och jägaren, båda tar hjälp av des lämpade objekt på heapen och ritar sedan

def paint_wumpus () :#funktion som ritar Wumpus
    #tänket bakom funktionen är helt enkelt att rita en importerad bild på rätt plats
    x=BOARD_SQUARE_WIDTH*wumpus.get_x()#tar objektet wumpus x och formulerar vart det ska ritas
    y=BOARD_SQUARE_HEIGHT*wumpus.get_y()#tar objektet wumpus y och formulerar vart det ska ritas
    wumpus_pic=pygame.image.load('wumpus.png')#bilden på wumpus som är 60x60
    main_screen.blit(wumpus_pic,(x,y))#ritar bilden
    
def paint_hunter () :#funktionen som ritar jägaren
    #jägaren kommer ritas som en circel med en bild på en pilbåge på, när man drar bågen används
    #en annan bild, cirkeln ska ändra färg när wumpus är nära
    #hunter är ett object för jägaren som har metorder som ankallas, se wumpusclasses
    x=BOARD_SQUARE_WIDTH*hunter.get_x()#jagarens x/y i pixlar
    y=BOARD_SQUARE_HEIGHT*hunter.get_y()
    radius=10#radien för cirkeln som markerar jägaren 
    circle_thickness=0#cirkelns tjocklek (noll betyder fylld)
    wumpus_close_color=RED#färgen på cirkeln när wumpus är nära
    not_close_color=YELLOW#färgen när wumpus inte är nära
    if hunter.hunter_senses(*wumpus.get_xy()).count('wumpus') :#wumpus är nära
        color=wumpus_close_color#färgen som cirkeln får
    else :#wumpus r inte nära
        color=not_close_color
        
    if hunter.is_shooting():#är bågen dragen, ta då bilden när den är dragen, ta annars den andra
        bow_pic=pygame.image.load('bow_drawn.png')#bild på dragen båge
    else :
        bow_pic=pygame.image.load('bow.png')#bild på odragen båge
    pygame.draw.circle(main_screen,color,(int(x+BOARD_SQUARE_WIDTH/2),int(y+BOARD_SQUARE_HEIGHT/2)),radius,circle_thickness)#ritar cirkeln som representerar jägaren 
    main_screen.blit(bow_pic,(x,y))#ritar bilden på pilgågen
    

def direction_to_text(direction):#gör om en mattematisk riktning till text, dvs upp,höger...
    #ganska självklart vilken riktning som ska vart man bör ha lärt sig ordningen
    #den begärda riktningen returneras sedan i textformat som string
    if direction==0 :
        return 'up'
    elif direction==1 :
        return 'right'
    elif direction==2 :
        return 'down'
    elif direction==3 :
        return 'left'

def hunter_senses_text():#texten som skrivs när jägaren är brevid wumpus eller hinder
    #skulle lika gärna kunna vare en metod -_-
    sense_list=hunter.hunter_senses(*wumpus.get_xy())#listan på vad jägaren känner
    text_list=[]#listan på texten som ska skrivas, fylls med tiden
    for sense in list(set(sense_list)) :#loop som går igenom alla unika element
        if sense=='wumpus' :#wumpus är nära
            text_list.append('I smell Wumpus.')
        elif sense =='hole' :#ett hål är nära
            text_list.append('I feel the wind of a bottomless pit.')
        elif sense=='bat' :#en fladdermus är nära
            text_list.append('I hear the sound of flying rats.')
    return text_list

def senses_text_box (x,y,width=350,height=120,color=BLUE_LIGHT):#ritar rutan där texten om nära
    #hinder och statistik dycker upp
    #color är färgen på rutan
    font_size=30#storleken på texten
    font='comicsansms'#textens font
    text_color=BLACK#färgen på texten
    space_between_text= 2#mellanrummet mellan vraje rad
    text_height=font_size + space_between_text#utrymmet var rad får(inka mellanrum)
    pygame.draw.rect(main_screen,color,(x,y,width,height))#ritar ruttan texten är på
    turn =0#hur många gånger man skrivit en text, så man kan räkna utrymme
    for text in (hunter.get_statistics_string(),*hunter_senses_text()) :#texten som ska skrivas
        message(x,y+turn*text_height,font_size,text,font,text_color,True)#ritar text
        turn+=1#man har nu ritat en rad till

def hunter_move_by_input(direction=None,toggle_shoot=False):#jägaren rör sig eller skjuter av input
    #notera att den körs i en loop så den kör om och om igen varje frame gånger i sekunden

    if toggle_shoot :#ska han dra bågen/sluta dra bågen
        hunter.shoot_toggle()#metod för att sluta/dra
    elif hunter.get_possible_directions().count(direction) == 1 :
        #ovan avgörs om spelaren har valt en riktning som går att ta
        if  hunter.is_shooting()  :#hen skjuter om bågen dragits
            hunter.hunter_shoot(direction,*wumpus.get_xy())#skjuter
        else :#annars flyttars hen 
            hunter.hunter_move(direction)
        #efter att jägaren skjutit eller gått så går wumpus
        wumpus.wumpus_move(*hunter.get_xy())#wumus rör sig 
        hunter.got_killed(*wumpus.get_xy())#avgör om man dött

        
        
def hunter_buttons (x,y,mouse_click) :#knappar för spelet och triggar att wumpus ska röra sig
    #är tänkt att knapparna ska ligga som ett kors där skjut är i mitten och gåriktningar runt om
    button_dimension =100 #bredd och höjd på var knapp
    between_space=10#mellanrummet mellan alla knappar
    #nedan beskrivs koordinaten för knapparnas kollektiva övre vänstra hörn dvs det är ingen knapp
    #där men som grupp blir det ett hörn
    collective_corner_xy=collective_corner_x,collective_corner_y=x,y
    color=BLUE#färg på knappen
    active_color=BLUE_LIGHT#färg när musen är över knappen
    impossible_action=False#om det inte går att göra handlingen
    impossoble_action_color=BLUE_DARK#knapp färg,musen på knapen men inte går att trycka
    #det blir ett kors med 9 möjliga positioner där bara 5 ska fyllas med knappar så vi gör en
    #loop där vi går igenom alla möjliga positioner och för en specifik position så beskrivs en text
    #och en funktion
    mouse_click=mouse_click#avgör om musen är tryckt
    for turn in range(9) :#man går från vänster till höger upp till ner
        impossible_action=False#om man inte kan trycka på knappen för att tex ingen gång går åt dit
        got_click=False#om knappen blev tryckt blir den True
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
        if turn==4 :#knappen för att man ska skjuta
            text='shoot'#text på knappen
            if hunter.get_number_of_arrows()<=0:#slut på pilar
                impossible_action=True
        elif turn%2 :# ska det finnas knapp rör dig knapp
            text=direction_to_text(direction)
            if hunter.get_possible_directions().count(direction) == 0 :#kan inte gå åt hållet
                impossible_action=True
        else :#det är ingen knapp så inget ska ritas
            continue
        
        if impossible_action :# om det inte går blir knappen en textruta
            message_box(local_x,local_y,button_dimension,button_dimension,text,impossoble_action_color)
        else :#annars kan man trycka den och och om den tryck ska got_click bli True
            got_click=text_button(local_x,local_y,button_dimension,button_dimension,text,color,active_color,mouse_click=mouse_click)
            
        if got_click and turn%2:#han har valt att skjuta/gå och valt riktning
            hunter_move_by_input(direction)
        elif got_click and turn==4: #han väljer att dra/släppa bågen
            hunter_move_by_input(toggle_shoot=True)
        
def taskbar(mouse_click):#funktionen som kör för att visa aktivitetsfältet i spelet
    #aktivitetsfältet förväntas bli 320x720 pixlar och ska inkludera knappar för vilket hål man
    #ska gå till och information om vad jägaren känner i omgivningen
    #inputen mouse_click är om musen trycks
    taskbar_width=SCREEN_WIDTH-BOARD_WIDTH*BOARD_SQUARE_WIDTH#bredden på menyn
    taskbar_left_edge=SCREEN_WIDTH-taskbar_width#vänsterkanten för menyn
    pygame.draw.rect(main_screen,GREEN,(taskbar_left_edge,0,taskbar_width,SCREEN_WIDTH))#ritar fält
    if not hunter.has_game_ended() :#ritar knaparna för att gå om inte spelet slutat
        hunter_buttons(taskbar_left_edge+30,380,mouse_click)
    senses_text_box(taskbar_left_edge+20,20)#skriver det jägaren känner i omgivningen
    if True == text_button(taskbar_left_edge+10,150,300,100,'main menu',RED,RED_LIGHT) :
        #knapp som trycks när man vill tillbaks till huvudmenyn
        return 'main menu'#returnerar att man vill tillbaks till huvudmenyn
    
def run_game(new_difficulty='medium') :#kör spelet, börjar med att generera plan etc
    difficulty.change_difficulty(new_difficulty)#man byter svårighetgraden
    matrix.create_maze()#genererar ny laburint
    night_vision=False#om man vill se alla rum på kartan 
    show_wumpus=False#om man ska visa wumpus, i normalfallet ska man inte se honom
    wumpus.place_random_empty_room()#placerar wumpus
    hunter.game_restart()#placerar jägaren och nolstäler statistik
    while True :#huvudloop som körs tills spelet slutar
        key_command()
        mouse_click=False#man förutsätter att musen inte tryckts, den kan ändras senare
        events=pygame.event.get()#lista på alla event från användaren typ knaptryck musen flytas etc
        for event in events :#man kallar event för ette evetnt pygame regestrerat
            if event.type== pygame.QUIT :#om man väljer att stänga programet
                close_game ()
            if event.type == pygame.MOUSEBUTTONDOWN:#om man clickar med en musknapp
                mouse_click=True
            if event.type == pygame.KEYDOWN and not hunter.has_game_ended():#knappar tryckningar
                #för användraval i spelet
                if event.key==pygame.K_n :#man vill se/sluta se hela kartan
                    night_vision=not night_vision
                if event.key==pygame.K_m :#man vill se/sluta se wumpus
                    show_wumpus=not show_wumpus
                #nedan beskrivs vilken input som jägaren får från tangenter så som
                #piltangenter och vart dom leder (givestvis räknas wasd) samt dra bågen
                if event.key==pygame.K_w or event.key==pygame.K_UP :
                    hunter_move_by_input(0)
                if event.key==pygame.K_d or event.key==pygame.K_RIGHT :
                    hunter_move_by_input(1)
                if event.key==pygame.K_s or event.key==pygame.K_DOWN :
                    hunter_move_by_input(2)
                if event.key==pygame.K_a or event.key==pygame.K_LEFT :
                    hunter_move_by_input(3)
                if event.key==pygame.K_SPACE and hunter.get_number_of_arrows()>0:#space för dra båge
                    hunter_move_by_input(toggle_shoot=True)

        display_rooms(night_vision)#ritar alla rum
        if show_wumpus :#ritar wumpus om han ska ritas
            paint_wumpus()
        paint_hunter()#ritar jägaren
        taskbar_return=taskbar(mouse_click)#ritar aktivitetsfältet och ser vad som returneras
        if taskbar_return =='main menu' :#om man valt att gå till huvudmenyn från aktivitetsfältet
            break
        if  hunter.has_game_ended() :#om spelet slutat via vinst eller förlust
            if win_screen(events) == 'quit':#kör funktionen för när spelat slutar
                break
            
        #print(events)#bugg:spelar man och vinner flera gånger kommer den printa sista gamal eventet också, fast bara när man vunnit så inget gamalt när man spelar WTF!!!! 
        pygame.display.update()#updaterar med det som ritas
        clock.tick(FPS)#pygames klocka ska ticka efter fps

#nedan kommer massa info om sidor annat än spelsidan
def win_screen (events=[]) :#funktionen som dyker upp när man vunnit och ska skriva sitt namn
    #om man inte vunnit står det bara en text om hur man dog

    events=text_input.update(pygame.event.get())#ta ort när buggen är fixad
    #vet att raden ovan borde ta in events från inputen men de är en bugg som sådan :
    #när man skriver nått första gången är det bra men andra gången så sparas det sista eventet som gjrodes från förra gången, alltså blir det som om enter är nedtryckt konstant nästa gång man skriver, detta beror på inputen man får från run_game men blir fuckad fast bara när spelet slutat
    #eftersom man inte tar input från spelets huvudloop så ger det väldigt trögt när man skriver
    
    cause_of_end=hunter.cause_of_ended_game(*wumpus.get_xy())#hur man dog
    enter_name_x,enter_name_y=410,410#x,y för rutan man fyller i namn
    enter_name_width,enter_name_height=400,50#dimensioner för rutan man fyller i namn på
    enter_name_text_color=RED #färgen på texten när man skriver sitt namn
    enter_name_text='enter name:'#texten i rutan där man ska skrva sitt namn
    enter_name_font_size=35#måste vara 35 anars måste man ändra text_input vilket värkara vara meck
    text_input.set_text_color(enter_name_text_color)
    if cause_of_end == 'win' :#ritar text på skärmen där det står hur spelet sluta
        text='ya win'
    elif cause_of_end  == 'wumpus' :
        text='wumpus killed you'
    elif cause_of_end == 'hole' :
        text='you fell into a pit'
    else :
        text='error 404 kill not found'
    message(SCREEN_WIDTH/2,SCREEN_HEIGHT/2,100,text,'arial',RED)#ritar slutmedelandet
    
    if cause_of_end=='win' :#om man vunnit och ska skriva namn
        pygame.draw.rect(main_screen,WHITE,(enter_name_x,enter_name_y,enter_name_width,enter_name_height))#rutan som namnet skrivs på
        message(enter_name_x+10,enter_name_y+10,enter_name_font_size,enter_name_text,None,enter_name_text_color,True)#inledande medelandet till input
        #print(events)#bugg:ger märkliga utslag när man vunit flera gånger
        
        if events and text_input.get_text()!='':#om man tryckt enter och man har skrivit nått
            name=text_input.get_text()#namnet man skrivit
            save_score(name)#funktionen sör att spara
            text_input.input_string=''#man ska nollstålla text för nästa gång
            return 'quit'
        main_screen.blit(text_input.get_surface(),(int(enter_name_x+len(enter_name_text)*enter_name_font_size/2.5),enter_name_y+10))#ritar den skrivna inputsttexten
        
    
def save_score(name='null') :#funktionen som kör när man ska spara spelerens highscore i dokumentet
    player_score=hunter.get_statistics_list()#tar den info om vad spelaren åstakom och bildar tabell
    player_score['name']=name#tabellen med all statistik får nu ett namn i tabellen
    wumpus_scores=shelve.open('wumpus_scores.dat','w',writeback=True)
    wumpus_scores[('statistics_'+ hunter.difficulty.get_difficulty())].append(player_score)
    #man sparar genom att lägga till det senaste player_score i den shelve som har lämplig svårihet
    wumpus_scores.close()

def high_score_screen():#funktionen som körs när man ska se föregående spelares high score
    button_collective_corner_x,button_collective_corner_y=10,200

    #nedan är variabler för hur listan ska sorteras med knappar
    button_height=100#hur höga ska knapparna vara
    button_width=100#bredden på knapparna
    button_space=20#mellanrum mellan knappar
    collective_corner_x,collective_corner_y=10,200#första knappens hörn
    rect_height=600#hur höga ska  vara rektanglarna vara
    rect_width=400#bredden på rektnaglarna
    rect_space=20#mellanrumet mellan rektanglarna
    header_size=50#font storlek för rubriken för varje spalt med highscore
    list_rect_turn=0#hur många gunger loopen körts för en rektangel med svårighetsgrad
    wumpus_file =shelve.open("wumpus_scores.dat","r")#öpnar och löser sparlilen
    index='moves'#index man sorterar efter
    greatest_to_smallest=False#ordningen man ska sortera i 
    list_font_size=12#varje rads fontstorlek
    list_font='ubuntumono'#fonten man skriver listan med, förslagsvis någon med monospace
    for difficulty in ('easy','medium','hard') :#går igenom varje spalt med svårighetsgrad
        local_x=collective_corner_x+list_rect_turn*(rect_width+rect_space)#x för spalten
        local_y=collective_corner_y#y för spalten
        if list_rect_turn ==0 :#lätt
            color=GREEN
            header='casual'
        elif list_rect_turn==1 :#medium
            color=YELLOW
            header='medium'
        else:#svår
            color=RED
            header='Hard'
        pygame.draw.rect(main_screen,color,(local_x,local_y,rect_width,rect_height))
        message(local_x+rect_width/2,local_y+header_size/2,header_size,header)
        sorted_score_list=sort_dict_by_index(wumpus_file['statistics_'+difficulty],index,greatest_to_smallest)
        score_board_turn=0#räknar hur många gånger man skrivit en enskild rad med resultat
        for singel_score in sorted_score_list :#loppen som ritar varje omgång, bildar först en text
            printed_text=(' %2d'%(score_board_turn+1))+('.name:%10.10s' %singel_score['name'])+('   moves:%3d'%singel_score['moves'])+('   found rooms:%3d' %singel_score['found rooms']) +('   shots:%3d' %singel_score['shots fired'])#texten som skrivs för en rad
            message(local_x,local_y+header_size+score_board_turn*list_font_size,list_font_size,printed_text,list_font,place_corner=True)#ritar medelandet 
            score_board_turn+=1
        
        list_rect_turn+=1
    wumpus_file.close()
    
def sort_dict_by_index(sort_list,index,greatest_to_smallest=True):#sorterar en lista beroende på
    #ett index och om den ska sorteras uppifrån och ner
    new_list=sorted(sort_list,key=lambda  k: k[index])
    if greatest_to_smallest :
        new_list.reverse()
    return new_list


def game_mode_menu_screen():#sidan menyn som dykerupp när man ska välja svårighetsgraden
    button_height=400#hur höga ska knapparna vara
    button_width=400#bredden på knapparna
    button_space=20#mellanrumet mellan knapparna
    collective_corner_x,collective_corner_y=10,300#första knappens hörn
    for turn in range(3) :#en loop som går igenom och ger var knapp text och ritar den
        if turn ==0 :#lätt
            difficult='easy'
            text='Easy mode'
            color=GREEN
            active_color=GREEN_LIGHT
        elif turn==1 :#medel
            difficult='medium'
            text='Medium'
            color=YELLOW
            active_color=YELLOW_LIGHT
        else :#svår
            difficult='hard'
            text='Hard, get rekt'
            color=RED
            active_color=RED_LIGHT
        text_button(collective_corner_x+(button_width+button_space)*turn,collective_corner_y,button_width,button_height,text,color,active_color,run_game,(difficult,))
        

        
def manual_screen (): #funktion man kör för att visa instruktions sidan
    #kommer mest vara en text med en knapp som leder tillbaks till menyn eller stänger programet
    corner_x,corner_y=30,150
    pygame.draw.rect(main_screen,BLUE_LIGHT,(corner_x,corner_y,SCREEN_WIDTH-2*corner_x,SCREEN_HEIGHT-corner_y-30))
    text=['Detta är spelet Wumpus som går ut på att spelaren ska döda monstret Wumpus. För att spela spelet trycker du på ”play” och väljer en',
          'svårighetsgrad. För att se statistik om spelare som spelat spelet och vunnit kan du trycka på ”highscore”. För att stänga programmet',
          'så kan du trycka på fönstrets kryss eller så kan du trycka ctrl-q.',
          '  ',
          'Själva spelet utspelar sig i en slumpad labyrint där spelet går ut på att spelaren/jägaren ska döda monstret Wumpus med sin pilbåge.',
          'I labyrinten väntar faror som dödshål som man kan ramla ner i och dö, fladdermöss som plockar upp jägaren och placerar hen på en',
          'slumpad plats och givetvis Wumpus som rör sig och kan äta upp jägaren om han kommer i kontakt.',
          '  ',
          'spelaren markerats med en prick med en pilbåge på, för att röra sig så kan hen antingen trycka på piltangenterna/ wasd samt dom blåa',
          'knapparen i aktivitetsmenyn. För att jägaren ska ha någon aning om vad som finns i omgivningen så har varje rum en viss färg beroende',
          'på vad som finns intill. Om ett rum är ljusgrått så leder alla gångarna till tomma rum, om det är blått så leder en eller fler av',
          'gångarna åt fladdermöss, om ett rum är mörkgrått så så leder en eller fler av gångarna mot ett hål och ett rum är mörkblått så leder',
          'det till både hål och fladdermöss. Om Wumpus är nära så kommer inte något rum ändra färg utan den gula prick som markerar spelaren',
          'kommer istället bli röd. Ett annat sätt att få reda på vad som finns i närheten är genom läsa i den blå rutan som finns uppe i hörnet.',
          'I rutan står även hur många pilar man har, hur många steg man tagit och  hur många rum man hittat.',
          '  ',
          'För att skjuta så trycker man på mellanslag eller så kan man trycka på mittenknappen hos dom blå tangenterna i aktivitetsfältet. Efter',
          'det så kommer jägaren dra bågen, om man vill släppa utan att skjuta så kan man trycka på samma knapp igen. Om man vill skjuta så måste',
          'bågen vara dragen och därefter så trycker man på en av riktningarna man normalt skulle gå med för att skjuta åt det hållet. Att dra',
          'bågen/sluta dra kommer inte trigga Wumpus att röra sig däremot så kan monstret röra sig om man skjuter. För varje skott man skjuter',
          'så förlorar man en pil, om man har 0 pilar kan inte skjuta. Som tur är så kan man plocka upp pilar om man har tur.',
          '   ',
          'Om man blir uppäten av Wumpus eller trillar ner i ett hål så står det att att man förlorat och man slutar genom att trycka på',
          '”main menu”. Om man vinner så kommer det upp en ruta där det står att man vunnit och så kan man skriva in sitt namn och avsluta',
          'med enter, därefter så registreras namnet ihop med statistik som man sedan kan se via huvudmenyn.' ]
    #det är inte snyggase sättet med lista men va fan det funkar i alla fall
    turn=0#hur många rader som skrivits
    for line in text :
        message(corner_x+10 ,corner_y+turn*18,20,line,'latinmodernsans',place_corner=True)
        turn+=1


def main_menu() :#huvudmenyn som ska köra när spelet startar
    action =None#variabel som betyder vilken funtion som ska köras som senare körs
    while True :
        key_command()
        main_screen.fill(WHITE)#ritar bakgrunden med vitt
        mouse_click=False#om musen har tryckts, kan ändras senare
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :#stäng programet
                close_game()
            if event.type == pygame.MOUSEBUTTONDOWN:#har man tryckt musen
                mouse_click=True
        #nedan kommer semi kodupprepning från annan game_mode_menu_screen
        
        button_height=100#hur höga ska knapparna vara
        button_width=400#bredden på knapparna
        button_space=20#mellanrumet mellan knapparna
        collective_corner_x,collective_corner_y=10,10#första knappens hörn
        for turn in range(3) :#en loop som går igenom och ger var knapp text och ritar den
            if turn == 0 :
                text='highscore'
                color=BLUE
                active_color=BLUE_LIGHT
            elif turn==1 :
                text='Play'
                color=GREEN
                active_color=GREEN_LIGHT
            else :
                text='Instructions'
                color=RED
                active_color=RED_LIGHT
            if True== text_button(collective_corner_x+(button_width+button_space)*turn,collective_corner_y,button_width,button_height,text,color,active_color,mouse_click=mouse_click) :
                if turn == 0 :#highscore rundan
                    action=high_score_screen
                elif turn ==1 :#spela och välj svårighetsgrad
                    action=game_mode_menu_screen
                else :#instruktioner
                    action=manual_screen
        if action != None :#kör funktionen man anget 
            action ()
        pygame.display.update()#uppdaterar det som ritas
        clock.tick(FPS)

    
def does_score_file_exist() :#ser om filen man sparar på finns med lista om inte, skapa den
    try :
        wumpus_file =shelve.open("wumpus_scores.dat","r")#öpnar och om det inte blir error
    except :#något osäker på typen av error så jag kör allmänt på raden ovan
        print('file not found, creating new')
        wumpus_file =shelve.open("wumpus_scores.dat")#skapar filen man vill åt
        #nedan skapas nyckel för varje svårighetsgrad
        wumpus_file['statistics_easy']=[]   
        wumpus_file['statistics_medium']=[]
        wumpus_file['statistics_hard']=[]        
    wumpus_file.close()#stänger filen
        
        
#nedan börjar vi med att skapa objekt som sparas på heapen
matrix = wumpusclasses.Room_matrix(BOARD_WIDTH,BOARD_HEIGHT) #matrisen som spelet utspelas på som
#representeras i klassen Matrix
difficulty=wumpusclasses.Difficulty()#alla behöver ha difficulty för att räkna chancer etc
matrix.set_difficulty(difficulty)
wumpus=wumpusclasses.Wumpus(matrix,difficulty)
hunter=wumpusclasses.Hunter(matrix,difficulty)
text_input=pygame_textinput.TextInput()


does_score_file_exist()#ser om highscorefilen finns

main_menu()#kör programet som börjar med menyn


#nedan finns paperskorgen, kan vara bra när man vill ha tillbaks grejer
