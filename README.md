#specifikation
##inledning
Jag har tänk att programera spelet wumpus vilket är ett spel där man kontrolerar en jägare som är på jakt efter monstret Wumpus. Spelet utspelar sig i en laburint med separerade rum som innehåller diverse hinder. målet är att döda Wumpus med en pil innan man blir uppäten eller dör av ett hinder. programet ska köras grafiskt i ett eget fönster.

en utmaning med programeringen kan bli att allt ska vara grafisskt och att rummens generering och egenskaper ska fungera som dom ska.
##Användarscenarier
###introduktionen till spelet
Jerka bestämmer sig för att pröva spelet Wumpus och efter att han startar spelet introduceras han till en meny där han för välja olika alternativ som knappar på skärmen. Eftersom han ären ~~noob~~ nybörjare väljer han att läsa spelmanualen. Där efter väljer han att starta spelet och väljer nivån lätt. Även fast Jerka spelar på *lätt* så lyckas han trilla ner i ett dödshål hål ~~eftersom han är en *filthy casual*~~. 
###Spelet
Lisa som har spelat spelet flera gånger väljer i stället att gå direkt till en svårare nivå där Wumpus rör sig. Efter att hon valt så kommer startas spelet där jägaren befinner sig i en laburint där rummen är mörkerlagda tills man varit i dom. Laburinten är slumpmäsigt genererad där ett rum kan ha 4-1 möjliga håll att gå åt där alternativen blir allt färre ju längre man går från satartpunkten. varje rum har ett inehåll exempelvis ett botunlösthål, fladermös, mm. För att navigera så har hon ett aktivitetsfält dör hon kan välja vilket håll hon ska gå åt eller om hon ska skjuta, hon kan även se antalet drag hon gjort, highscore, det jägaren känner från omgivningen och annan info/alternativ. Eftersom hon spelat spelet ett tag och har lärtsig om hur den inkompetenta programeraren gjort wumpus AI så lyckas hon besegra wumpus. Efter att hon vunnit så får hon en ruta där hon fylleri sitt namn så att hennes score för att besegra wumpus kan sparas i ett dokument av higscores.

##Kodsklett
```python
#kodsklett för spelet wumpus

#allt är i ett dokument i sklettet men färdiga produkten lär vara uppdelad

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

def message(x,y,font_size,text,font,color) :#ritar ett text medelande på main_screen
    pass

def message_box(x,y,width,height,text,color) :#ritar en ruta på main_screen med en text på
    pass

def text_button(x,y,width,height,text,color,active_color,action,action_arguments) :
    #funktionen ritar en rektangulär knapp på main_screen
    #active_color syftar på när musen är på knappen
    #action är funktionen man vill köra när man trycker på knappen
    #action_arguments är en tuple av dom argument som action ska ha
    pass

def close(state=None) :#stänger hela programet med eventuel funktion när det stängs
    #state syftar på vad som ska hända när programet stäng exempelvis kan ett medelande duka upp 
    pass


#nedon kommer logik om själva spelet och spelplanen

#matrisen för spelplanen har x,y numrering som en matte matris fast med 00 uppe i högra hörnet

#nedan kommer lite logic för att generera rummen och visa dom
#tanken bakom rummen är att dom ska hålla sig inom en 16x12 matris där alla rutor är rum
#och rummen är 60x60 pixlar. rummen slumpas där ett rum kan ha 4-1 in/utgångar och varje
#rum kan ha ett inehåll så som hål eller flygande råttor.

#generelt sätt skrivs riktningarna i ordningen med upp först och sedan som klockan om det
#ska inkludera siffror så blir up 0 och sedan ökar det med 1 i ordningen ovan

game_matrix=([],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]) #globala matrisen som håller reda på
#laburinten varje lista i tupeln representerar en kolumn och alla 16 listor blidar brädet

def generate_rooms() :#funktionen som ankallas när alla rum/laburinten ska slumpas om.
    #funktionen kommer att nollställa föregående laburint och returnera en ny.

    #Laburinten är tänkt att beffina sig i en matris(en lista med listor i) som börjar
    #med att alla element är None och sedan byggerpå med objekt från klassen Room. rummen
    #manipuleras sedan allt eftersom det genereras.

    #det är tänkt att genererandet ska ske med hjälp av en rekursiv funktion som slumpar ett
    #rum som ankalar att slumpa åt ett håll där det saknas förklaring d.v.s om det inte
    #finns gång eller vägg åt det hållet. Om det finns ett annat rum åt det slumpade hållet
    #så slumpas det om det ska finnas en väg eller gång mellan vilket ändrar båda objekten om
    #det inte är så att det påstötta rumet slumpat en vägg, dåt blir det en vägg
    #Om det slumpas åt ett håll där det inte finns ett rum så slumpas om det ska finnas en vägg
    #eller ett nytt rum, om det ska skapas ett rum ankalla funktionen sig själv
    pass

def add_interior():#lägger till slumpat inehåll i den slumpade laburinten så som hål
    pass

def display_rooms():#funktion som går igenom matrisen för alla slumpade rum och ritar planen
    #om ett rum inte ska visas eftersom det är obesökt eller det står None i matrisen så
    #ritas en svart ruta eller liknande

    #om rummet är besökt ska det ritas en bild
    #bilden jag tänkt mig ska ritas är den cirkel, cirkeln ska få rektanglar åt alla hål som det
    #finns gångar, det är möjligt att jag snyggar till det senare
    #för att visa inehållet ritar jag något extra,  typ svart ring för hål etc

    #jägaren och Wumpus ritas separat
    pass

def random_room():#returnerar en kordinat för ett rum utan inehåll
    pass

#har tänkt att använda mig av globala variabler så att man inte begöver hålla koll på
#massa argument och returnerade värden
hunter_coordinates=[0,0] #kordinaterna för jägaren
wumpus_coordinates=[0,0] #kordinaterna för wumpus
difficulty='easy' #global variabel för vilken svårighetsgrad det är, ändras när man väljer grad

def possible_moves_hunter(): #retrnerar en tupple av alla möjliga riktningar som jägaren kan gå
    pass

def possible_moves_wumpus():#retrnerar en tupple av alla möjliga riktningar som wumpus kan gå
    #skilnaden från jägaren är att wumpus inte kan välja att till ett hål
    pass

def hunter_move (direction) :#ändrar på jägarens x,y beroende på riktning
    #ska även kontrollera riktningen så man inte går genom vägg
    pass


def hunter_shoot(direction):#funktion som körs när man ska skjuta
    pass

def display_hunter(x,y):#en bild av jägaren beroende på var på planen han ska vara
    pass

def wumpus_walk(): #räknar ut vart wumpus ska gå och ändrar på wumpus_coordinates
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

def instructions_screen (): #funktion man kör för att visa instruktions sidan
    #kommer mest vara en text med en knapp som leder tillbaks till menyn eller stänger programet
    pass


#nedan kommer klasserna

class Room (object) :
    #klass som beskriver varje rum som ett object
    #objektet ska inkludera om:
    #det finns ett rum brevid sig eller vägg åt varje håll om det står None har
    #det inte genererats klart, True om det finns dörr och False om det är vägg

    #vad rummet inehåller exempelvis om det finns ett dödshål i rummet, notera att det inte är
    #tänkt att Wumpus eller jägaren är ett inehåll, om inehållet är None så är det bara ett rum

    #ska även inkludera om rummet besökts av spelaren
    
    #det är möjligt att jag inkluderar rummets x och y men tvivelaktigt eftersom objektten sparas i
    #en matris dvs, rummet sparas i en lista så objektets namn ankalas ej utan dess kordinat ankalas

    #generelt sätt skrivs riktningarna i ordningen med upp först och sedan som klockan om det
    #ska inkludera siffror så blir up 0 och sedan ökar det med 1 i ordningen ovan
    
    total=0 #statisk metod så att man kan hålla reda på antalet rum som skapats, bra om chansen för
       #att generera nya rum ska minska desto fler rum man har
    
    def init(self,up=None,right=None,down=None,left=None,content=None,roomx=None,roomy=None,visit=False) :
        Room.total +=1 #ska finnas lite mer...

    def set_direction  (self,connection) : #bestämer att det ska finnas gång/vägg åt de bestämde
        #hållet, 
        #om connection är True så gång, False om Vägg, None anses som ogenererad
        pass
    
    def set_content(self,content) : #bestämmer rumets inehåll, exempelvis dödshål
        self.content=content

    def get_content(self) : #returnerar vad som finns i rummet
        return self.content
    
    def get_direction(self,direction) : #returnerar om det finns vägg/gång åt den begärda riktningen
        #argumentet direction är riktningen man vill ha, 0 är upp och sedan som klockan
        pass
    
    def get_total(): #returnerar antalet rum som skapats
        return Room.total

    def reset() :#ska ankallas när det ska slumpas nya rum
        #exempelvis nollställas räknaren för totala antalet rum
        pass

    def number_of_unknown_directions(self):#returnerar antalett okända gångar/väggar vid rummet
        pass

    def unknown_directions(self):#returnerar en tuple för alla up/right/down/left som är None
        #0<=up, 1<=rigth, 2<=down,3<=left
        pass

    def number_of_paths(self) :#returnerar antalet gångar som finns d.v.s riktningar med True 
        pass 
        
    def path_directions(self):#returnerar riktningarna där det finns gångar som en tupple 
        pass
    
class Stats (object) : #klass för att spara statistik och ge highscore
    #klassen ska inkludera namn, svårighetsgraden, och antalet darg mm

    def __init__(self,difficulty=None,arrows=5,name=None,moves=0,found_rooms=1):
        self.difficulty=difficulty
        self.name=name
        self.moves=moves
        self.found_rooms=found_rooms
        #kan eventuelt bli fler variabler
        
    def __str__(high_score=False) : #skriverut statistik om spelaren
        #om highscore är True så ska info relevant för spelarens highscore returneras
        pass
    
    def add_move(self) : #läggertill ett drag och returnerar antalet drag
        pass

    def get_highscore(self):#räknar ut ett highscore efter lämplig algoritm
        pass

    def get_statistics(self):#ger statistik som anses vara relevant under spelets gång
        pass

    def shots_fired(self) :#visar hus många skott som skjutits
        pass

    def add_shots_fired(self) :#lägger till ett extra skott som skjutits
        pass
    
    def number_of_arrows(self):
        pass
    
    def set_name(self): #ändrar namn, bra att ha när spelarens highscore ska sparas
        #men behövs ej under spelets gång för at visa statistik
        pass
```
##Programflöde och dataflöde

##Plan B och brodering i kanterna
Om det går dåligt och jag får ont om tid så kommer vissa saker plockas bort. Sådant som kan plockas bort är: 
* att spara ett highscore.

sånt som kan läggas till om det ska bli extra fint är: 
* att ge jägaren ett begränsat antal pilar där man ska kunna få fler pilar genom att plocka upp pilar
* En AI som inte är värdelös.
