#denna fil inehåller alla klasser som gjort för spelet wumpus



import math,random

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
    total_number_of_paths=0
    def __init__(self,up=None,right=None,down=None,left=None,content=None,roomx=None,roomy=None,visit=False) :
        self.direction_list=[up,right,down,left]#listan för vad som finns i rummets riktningar
           #None är ogenererad, True är gång, False är vägg
        self.visited=False  #True om rummet besökts av spelaren False om obesökt
        self.content=content
        Room.total +=1 #vi vill att totala antalet rum ska öka när ett rum skapas
    def set_direction  (self,direction,connection) : #bestämer att det ska finnas gång/vägg åt
        #det bestämda hållet om connection är True så gång, False om Vägg, None anses som ogenererad
        if connection==True :
            Room.total_number_of_paths+=1
        elif self.direction_list[direction]==True and connection==False :
            Room.total_number_of_paths-=1
        self.direction_list[direction]=connection
    def set_content(self,content) : #bestämmer rumets inehåll, exempelvis dödshål
        self.content=content
    def get_content(self) : #returnerar vad som finns i rummet
        return self.content
    def get_direction(self,direction) : #returnerar om det finns vägg/gång åt den begärda riktningen
        #argumentet direction är riktningen man vill ha, 0 är upp och sedan som klockan
        return self.direction_list[direction]
    def number_of_unknown_directions(self):#returnerar antalett okända gångar/väggar vid rummet
        return direction_list.count(None)
    def unknown_directions(self):#returnerar en lista för alla up/right/down/left som är None
        #0<=up, 1<=rigth, 2<=down,3<=left
        directions =[]
        for i in range(4) :
            if self.direction_list[i]==None :
                directions.append(i)
        return directions
    def number_of_paths(self) :#returnerar antalet gångar som finns d.v.s riktningar med True 
        return direction_list.count(True)
    #obs!!!! jag har samma kod här som i unknown_directions
    def path_directions(self):#returnerar riktningarna där det finns gångar åt
        directions=[] 
        for i in range(4) :
            if self.direction_list[i]==True :
                directions.append(i)
        return directions
    def room_visited (self) :#ser om man varit i rummet
        return self.visited
    def visit_room (self):#gör att rummet blir upptäkt
        self.visited=True
    @staticmethod
    def get_total_number_of_paths () :
        return Room.total_number_of_paths
    @staticmethod
    def get_total(): #returnerar antalet rum som skapats
        return Room.total
    @staticmethod
    def reset() :#ska ankallas när det ska slumpas nya rum
        #exempelvis nollställas räknaren för totala antalet rum
        Room.total=0
        Room.total_number_of_paths=0

        
class Matrix(object) : #klass som skapar spelplasmatrisen och fylls på allt eftersom
    #hella klassen bygger på att man har en stor lista som har listor i sig där dom inre
    #listorna representerar kolumner där alla element i matrisen börjar som None och sedan
    #kan man lägga till objekt vilket kommer vara rum från klassen Room.
    #i matrisen antyder x på vilken kolumn det ska vara och y på elementet det ska vara
    
    def __init__(self,x_dimension=16,y_dimension=12) :#börjar med att definiera brädets dimensioner
        self.matrix_list=[] #matrisen som ska representera spelplanen. matrisen inehåller listor
        #för varje kolumn och i kolumnerna finns rummen från klassen Room eller None

        self.x_dimension=x_dimension
        self.y_dimension=y_dimension
        #vi börjar med att skapa en tom matris genom att kalla på funktionen som gör att alla
        #element i matrisen blir None
        self.reset_matrix()
    def __str__(self) :
        print(self.matrix_list)# jag vet att man inte ska ha print men det går inte att returnera
        #en lista när man använder __str__,
        return ''
    def reset_matrix(self):#gör att alla element i matrisen blir None
        self.matrix_list.clear()
        for column in range(self.x_dimension) :
            column_list=[]
            for row in range(self.y_dimension) :
                column_list.append(None)
            self.matrix_list.append(column_list)
    def call_object(self,x,y):#kallar på element/objekt beroende på x,y, som kan ändras mm
        return self.matrix_list[x][y]#behäver tekniskt sätt inte vara ett rum
    def random_object_xy (self):#hittar random x,y kodrinat för ett objekt i matrisen
        while True :
            random_x=random.randrange(self.x_dimension)
            random_y=random.randrange(self.y_dimension)
            if self.matrix_list[random_x][random_y]!=None:
                return (random_x,random_y)
    def get_dimensions (self) :#ger bredd,höjd som tupple
        return (self.x_dimension,self.y_dimension)
    def get_area(self) :#anger arean på matrisen dvs bredd x höjd
        return self.x_dimension*self.y_dimension
    
    def get_direction_xy(self,x,y,direction) :#man får nytt x,y ett steg från riktning som tupple
        return (x+(direction%2)*(2-direction),y+((direction+1)%2)*(direction-1))

    def direction_on_edge (self,x,y,direction):#är man i äden av kanten och riktning mot kant?
        return (direction==0 and y==0) or (direction==3 and x==0) or  (direction==1 and x==self.x_dimension-1) or (direction==2 and y==self.y_dimension-1)
    def get_surrounding_objects_direction (self,x,y):#riktningar för icke None objekt
        direction_list=[] #lista med riktningarne som fylls på
        for direction in range(4) :
            if self.direction_on_edge(x,y,direction) :
                continue
            elif self.call_object(*(self.get_direction_xy(x,y,direction)))==None :
                continue
            else :
                direction_list.append(direction)
        return direction_list
    
    def get_surrounding_objects_xy(self,x,y) :#returnerar icke None för närligande objekt som 
        xy_list=[] #lista med element kordinater
        for direction in self.get_surrounding_objects_direction(x,y) :
            xy_list.append((self.get_direction_xy(x,y,direction)))
        return xy_list
                
class Room_matrix (Matrix):#en matris som genererar en matris med rum
    #obs kodupprepning
    def set_difficulty (self,difficulty):#difficult förväntas vara ett objekt
        self.difficulty=difficulty
    def get_difficulty (self) :
        return self.difficulty
    def reset_matrix(self) :
        super(Room_matrix,self).reset_matrix()#gör att alla element i matrisen blir None
        Room.reset()#resetar rum statistik
    
        
    def generate_rooms(self) :#funktionen som ankallas när alla rum/laburinten ska slumpas om.
    #funktionen kommer att nollställa föregående laburint och returnera en ny.

    #Laburinten är tänkt att beffina sig i en matris(en lista med listor i) som beskrivs
    #med klassen Matrix och kallas matrix. i matrisen  börjar med att alla element är 
    #None och sedan bygges det på med objekt från klassen Room. rummen manipuleras sedan 
    #allt eftersom det genereras.

    #genererandet ska ske med hjälp av en rekursiv funktion som slumpar ett
    #rum som ankalar att slumpa åt ett håll där det saknas förklaring d.v.s om det inte
    #finns gång eller vägg åt det hållet. Om det finns ett annat rum åt det slumpade hållet
    #så slumpas det om det ska finnas en väg eller gång mellan vilket ändrar båda objekten
    #Om det slumpas åt ett håll där det inte finns ett rum så slumpas om det ska finnas en vägg
    #eller ett nytt rum, om det ska skapas ett rum ankalla funktionen sig själv

    #funktionen ska köra ända tills man är nöjd med den slumpade laburinten och är det så att
    #man slumpat en massa laburinter utan bra resultat tar man bara den senaste
        self.number_of_generated_mazes=0#antal slumpade laburinter
        while self.number_of_generated_mazes<1000 :#loop som körs tills jag är nöjd med laburinten
            start_x,start_y = int(self.x_dimension/2),int(self.y_dimension/2)#där genereringen ska börja
            self.reset_matrix()
            self.add_room(start_x,start_y)#skapar startrummet
            self.generate_rooms_recursion(start_x,start_y)#den rekursiva funktionen
            print('rooms',Room.get_total(),'paths',Room.get_total_number_of_paths())
            #nedan konner mitt test om laburinten var bra eller ej om inte, gör om
            if  self.difficulty.room_range(self) :
                break
            else:
                self.number_of_generated_mazes+=1
        print('generate atemptes:',self.number_of_generated_mazes)#antal gånger rum genererats

        
    def generate_rooms_recursion(self,x,y) :#den rekursiva funktionen som genererar rum, x och y
    #är det rum som genereras för närvarande
    
    #raden under beskrivs chansen för att det blir en wägg som genereras istället för rum
        make_room_chance=self.difficulty.make_room_chance(self)
        connect_rooms_chance=self.difficulty.connect_rooms_chance(self)#chansen för att ett rum man stöterpå ska bilda koppling
        unknown_directions=(self.call_object(x,y)).unknown_directions()#får ordnad lista av riktningar utan vägg/gång
        random_directions=random.sample(unknown_directions,len(unknown_directions))#slumpar listans
    #ordning, det borde funka med random.shuffle() men det värkar som python har brister...
        for random_direction in random_directions :
            #obs brace yourself recuring code i comming
            #slumpande behöver modifieras

            #logik bakom riktningar mm. riktningen är som klockan, kallas (riktning+2)%4
            #snurrar riktningen den 180,
            #glöm inte att y ökar längre ner
            random_direction_flip=(random_direction+2)%4 #för att få mosatta riktningen
            random_direction_xy=self.get_direction_xy(x,y,random_direction)
            #variabeln ovan säger kordinaten för rummet i vald riktning

            #om man är i kanten av planen ska det bli en vägg
            if self.direction_on_edge(x,y,random_direction)  :
                self.call_object(x,y).set_direction(random_direction,False)#gör en vägg åt hållet
                #om det finns ett rumm intill bildas gång mellan?
            elif (self.call_object(*random_direction_xy)) != None :
                if connect_rooms_chance > random.random() :#kopla ihop ?
                    self.call_object(x,y).set_direction(random_direction,True)#ändrar egna rummet
                    self.call_object(*random_direction_xy).set_direction(random_direction_flip,True)
                else :#rummen ska inte kopplas ihop
                    self.call_object(x,y).set_direction(random_direction,False)#vägg för egna rummet
                    #sätter vägg för andra rummer
                    self.call_object(*random_direction_xy).set_direction(random_direction_flip,False)
            else: #den valda riktningen är tom brevid
                if random.random() > make_room_chance :#skapa vägg?
                    self.call_object(x,y).set_direction(random_direction,False)#skapar vägg
                else : #skapa nytt rum
                    self.call_object(x,y).set_direction(random_direction,True)#väg till nytt rum
                    self.add_room(*random_direction_xy)#lägger till nya rummet i matrisen
                    self.call_object(*random_direction_xy).set_direction(random_direction_flip,True)#nya rummet väg till egna
                    self.generate_rooms_recursion(*random_direction_xy)#generera nya rummet

    def random_empty_room_xy(self) :#retrunerar x,y kordinater för tomt rum
        while True : #prövar rum tills man hittar ett
            random_xy=self.random_object_xy()#man vill bara slumpa en gång per runda
            if self.call_object(*random_xy).get_content() ==None :
                return random_xy
                    
    def random_empty_room(self) :#returnerar ett rum i matrisen som saknar inehåll
        return self.call_object(*self.random_empty_room_xy())

    def add_specific_content(self,content,amount) :#lägger till ett hål mm i random tomt ställe
        if amount ==0 :
            return
        else :
            self.random_empty_room().set_content(content)
            self.add_specific_content(content,amount-1)
            
    def add_all_content (self) : #lägger till massa hål mm till laburinten
        self.difficulty.set_content_multiplier()
        print('amount of holes',self.difficulty.hole_amount(),'bats',self.difficulty.bat_amount())
        self.add_specific_content('hole',self.difficulty.hole_amount())
        self.add_specific_content('bat',self.difficulty.bat_amount())
        self.add_specific_content('arrows',self.difficulty.find_arrow_amount())
    def get_near_content(self,x,y) :#ger inehållet för närliggande rum
        near_content_list=[]
        for direction in range(4) :
            if self.call_object(x,y).get_direction(direction) == True :
                if (self.call_object(*self.get_direction_xy(x,y,direction)).get_content()) != None:
                    near_content_list.append( (self.call_object(*self.get_direction_xy(x,y,direction)).get_content()))
            else :
                continue
        return near_content_list
    
    def add_room (self,x,y):#skapar ett rum av klassen Room och lägger det i matrisen
        self.matrix_list[x][y]=Room()

    def create_maze(self) :#skapar laburinten från generering till att fylla med inehåll mm
        self.difficulty.set_room_multiplier()
        self.generate_rooms()
        self.add_all_content()
        
class Character (object) :#klass för att beskriva var karaktärerna är i x,y led
    instance_list = []
    def __init__ (self,matrix,difficulty) :
        Character.instance_list.append(self)
        self.matrix=matrix#matrisen förutsätts vara Room_matrix för många metoder
        self.x=1#måste definieras även om det inta användes
        self.y=1
        self.difficulty=difficulty#notera att ska vara ett objekt

        
    def change_x (self,new_x) :#ändrar spelarens x kordinat
        self.x=new_x
    def change_y(self,new_y) :#ändrar spelarens y kordinat
        self.y=new_y
    def change_xy (self,x,y) :#ändrar spelarens x och y kordinat
        self.change_x(x)
        self.change_y(y)
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def get_xy (self) :
        return (self.x,self.y)
    def place_random_empty_room(self) :#plaserar karaktären i ett tomt rum utan hinder,karaktärer
        while True :
            random_empty_room_xy=self.matrix.random_empty_room_xy()#notera lista/tuple
            if Character.get_all_xy().count(random_empty_room_xy) != 0 :
                continue
            else :
                self.change_xy(*random_empty_room_xy)
                return random_empty_room_xy
            
    def get_possible_directions(self) :#returnera en lista/tuple av alla väg riktning
        return self.matrix.call_object(self.x,self.y).path_directions()
    
    @classmethod
    def get_all_xy (cls):
        xy_list=[]
        for instance in Character.instance_list :
            xy_list.append(instance.get_xy())
        return xy_list
    
class Wumpus(Character) :
    def get_possible_directions(self) :#skilnaden är att han inte kan gå ner i hål
        paths_list=super(Wumpus,self).get_possible_directions()
        new_path_list=[]
        for direction in paths_list :
            if (self.matrix.call_object(*self.matrix.get_direction_xy(self.x,self.y,direction)).get_content()) ==('hole') :
                continue
            else :
                new_path_list.append(direction)
        return new_path_list

    def wumpus_new_position(self,x,y):#kan äta fladdermöss, tar ej hänsyn till hens plasering
        self.x=x
        self.y=y
        if self.matrix.call_object(x,y).get_content() == 'bat':#wumpus äter möss
            self.matrix.call_object(x,y).set_content(None)

    def wumpus_move (self,x_hunter=None,y_hunter=None):#wumpus flyttar ska sig
        possible_directions=self.get_possible_directions()
        if possible_directions==[]  :#om det iinte går att gå
            self.place_random_empty_room()
        elif random.random() <self.difficulty.wumpus_stay_chance() :#chansen att wumpus ska stanna
            return
        elif random.random()<self.difficulty.wumpus_move_chance()  : #wumpus ska röra sig random
            direction=random.choice(possible_directions)#slumpar riktning
            self.wumpus_new_position(*self.matrix.get_direction_xy(self.x,self.y,direction))
            return
        elif random.random()<self.difficulty.wumpus_move_to_player_chance() and (x_hunter != None or y_hunter != None ) :#röra sig mot spelaren
            for tries in range(100):#körs tills hen valt möjlig väg eller ingen väg funkar
                if random.random() > 0.5 :#han går efter x
                    if self.x<x_hunter: #vilken riktning ska det vara
                        direction=1
                    else :
                        direction=3
                else : #han går efter y
                    if self.y<y_hunter :
                        direction=2
                    else :
                        direction=0
                if possible_directions.count(direction)==0:#kollar om man kan gå åt hållet
                    continue
                else : #han ska gå

                    self.wumpus_new_position(*self.matrix.get_direction_xy(self.x,self.y,direction))
                    return
            self.wumpus_move(x_hunter,y_hunter)#funka inte, pröva nytt alternativ 
        else:
            return
            
class Hunter(Character) :#klass för jägaren med metoder för att röra sig och ststistik

    def __init__(self,matrix,difficulty) :
        super(Hunter,self).__init__(matrix,difficulty)
        self.reset_statistics()
        
    def reset_statistics (self) :
        self.arrows=self.difficulty.number_of_start_arrows()#pilar hen har
        self.shots_fired=0#skott som skjutits
        self.game_ended=False
        self.shoot=False #om jägaren drar strängen eller ej
        self.found_rooms=0#antalet rum jägaren hittat(redan hittade räknas ej
        self.moves=0
        self.cause_of_end=None#varför sluta spelet ex wumpus var hungrig

    def game_restart (self) :
        self.reset_statistics()
        self.place_random_empty_room()
        
    def hunter_move (self,direction) :
        xy=self.matrix.get_direction_xy(self.x,self.y,direction)
        self.hunter_new_position(*xy)
        self.moves+=1
    def hunter_new_position(self,x,y) :#
        self.x=x
        self.y=y
        if not self.matrix.call_object(x,y).room_visited() :
            self.found_rooms+=1
        self.matrix.call_object(x,y).visit_room()
        if self.matrix.call_object(x,y).get_content()=='bat' :#om man går på fladder möss, flyg
            self.place_random_empty_room()
        elif self.matrix.call_object(x,y).get_content()=='hole' :#dör om man går på hål,
            pass
        elif self.matrix.call_object(x,y).get_content()=='arrows' :
            self.arrows+=self.difficulty.number_of_pick_up_arrows()
            self.matrix.call_object(x,y).set_content(None)
    def hunter_near_content(self) :#ger dom hinder i rummen brevid
        return self.matrix.get_near_content(self.x,self.y)
    def hunter_senses(self,wumpus_x=99,wumpus_y=99) :#får det jägaren känner, som hinder och wumpus
        sense_list=[]#lista som fylls med all jägaren känner
        sense_list.extend(self.hunter_near_content())#lägger till alla nära hinder
        if ((wumpus_x-self.x)**2+(wumpus_y-self.y)**2)**0.5 <=self.difficulty.sense_wumpus_radius():
            sense_list.append('wumpus')
        return sense_list
        
    def place_random_empty_room(self) :
        xy=super (Hunter,self).place_random_empty_room()
        self.hunter_new_position(*xy)

    def got_killed(self,wumpus_x,wumpus_y):#blev hen dödad?
        if self.x==wumpus_x and self.y==wumpus_y :#om man blev äten av wumpus
            self.dead('wumpus')
            return True
        elif self.matrix.call_object(self.x,self.y).get_content() =='hole':#om man trillar i hål
            self.dead('hole')
            return True
        else :
            return False
    def hunter_shoot(self,direction,wumpus_x,wumpus_y):#funktion som körs när man ska skjuta
        #skjuter rakt, annars blir det för lätt eftersom grafiken är som den är
        shoot_length=self.difficulty.shoot_length()#hur långt kan hen skjuta

        if self.shoot == True and self.arrows>0:
            self.shoot_toggle ()
            self.arrows-=1
            self.shots_fired+=1
            if (0<(direction%2)*((self.x-wumpus_x)*(direction-2)) <= shoot_length and wumpus_y==self.y) or( 0<((direction+1)%2)*((wumpus_y-self.y)*(direction-1)) <=shoot_length and wumpus_x==self.x):#självklar formel för att man träffar
                self.game_ended=True
                self.cause_of_end='win'
                return True#om hen träffar så returneras True
            else :
                return False

    def shoot_toggle(self) :#om han drar strängen och ska sluta eller motsatt
        self.shoot=not self.shoot

    def get_number_of_arrows(self) :
        return self.arrows
        
    def is_shooting(self) :#om han drar strängen
        return self.shoot
    
    def dead(self,cause='wumpus') :#kallas på om han blir dödad
        self.game_ended=True
        if self.cause_of_end != 'win' :
            self.cause_of_end=cause
        return True
    
    def get_statistics_string(self) :#ska ge divere statisk för att skriva ut
        return str('arrows:'+ str(self.arrows)+' moves:'+ str(self.moves)+ ' found rooms:'+ str(self.found_rooms))

    def get_statistics_list(self) :
        return {'difficulty': self.difficulty.get_difficulty() ,
                'moves':self.moves,
                'found rooms':self.found_rooms,
                'shots fired':self.shots_fired,
                'name':None}
                        
                
    def has_game_ended (self):#har spelet tagit slut?
        return self.game_ended

    def cause_of_ended_game (self,wumpus_x,wumpus_y) :#hur slutade spelet
        if self.game_ended :
            if self.cause_of_end =='win' :#ser om det var för att man vann
                return 'win'
            self.got_killed(wumpus_x,wumpus_y)#om man inte vann så räknas det ut varför man är död
            return self.cause_of_end
        else:
            return None
    
class Difficulty (object) :#håller reda på svårighetsgrad och chanser
    def __init__ (self,difficulty='easy') :
        self.difficulty=difficulty
        self.set_room_multiplier()
        self.set_content_multiplier()

    def __str__(self) :
        return self.difficulty
        
    def get_difficulty(self) :
        return  self.difficulty
    def change_difficulty(self,new_difficulty) :
        self.difficulty=new_difficulty
    def set_room_multiplier (self) :#avgör hur många rum det ska vara beroende på svårighetsgrad
        if self.difficulty=='easy' :
            self.room_multiplier=0.5
        elif self.difficulty=='hard' :
            self.room_multiplier=1.5
        else :
            self.room_multiplier=1
    def room_range (self,matrix=None): #avgör det tillåtna gränserna en laburint kan ha
        if self.room_multiplier*0.4*matrix.get_area() < Room.get_total() <self.room_multiplier* 0.6*matrix.get_area() and 2<Room.get_total_number_of_paths()/Room.get_total() <3 :
            return True
        else :
            return False
    def make_room_chance (self,matrix) :#hansen att skapa ett rum 
        return self.room_multiplier*(1- Room.get_total()/matrix.get_area()*5*math.sin(1*Room.get_total_number_of_paths()))
    def connect_rooms_chance(self,matrix):#chansen för att två rumkopplas
        return  math.sin(1*Room.get_total_number_of_paths()) 
    def set_content_multiplier (self):#avgör hur många objekt av nått det ska bli
        self.content_multiplier=0.1*self.room_multiplier*Room.get_total()
    #kodupprepning?    
    def hole_amount (self) :
        return int(1*self.content_multiplier)
    def bat_amount(self) :
        return int(2*self.content_multiplier)

    def difficulty_chance(self,chance_easy,chance_medium,chance_hard) :
        if self.difficulty == 'easy' :
            return chance_easy
        elif self.difficulty == 'medium' :
            return chance_medium
        elif self.difficulty == 'hard' :
            return chance_hard
        else :
            return 0.5
    
    def find_arrow_amount(self) :
        return self.difficulty_chance(0,5,5)#borde bero på rumm men hitta ingen snygg lös
        
        
    def wumpus_stay_chance (self) :
        return self.difficulty_chance(0.9,0.3,0.01)

    def wumpus_move_chance (self) :
        return self.difficulty_chance(0.2,0.7,0.2)        

    def wumpus_move_to_player_chance (self) :
        return self.difficulty_chance(0.1,0.1,0.9)
    def sense_wumpus_radius(self) :
        return 1
    def shoot_length(self) :#jur långt kan jägaren skjuta, notera att det är rakt
        #om det är 1 betyder det att hen skjuter till och med rummet brevid
        return 2
    def number_of_start_arrows(self) :
        return self.difficulty_chance(420,5,2)
    
    def number_of_pick_up_arrows(self) :
        return self.difficulty_chance(420,3,1)
