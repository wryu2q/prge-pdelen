#nedan kommer klasserna
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
        self.visited=True  #True om rummet besökts av spelaren False om obesökt
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
    def set_difficulty (self,difficulty):
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
        print('atemptes:',self.number_of_generated_mazes)#test för att se om genererandet är bra

        
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

    def random_empty_room(self) :#returnerar ett rum i matrisen som saknar inehåll
        while True : #prövar rum tills man hittar ett
            random_xy=self.random_object_xy()#man vill bara slumpa en gång per runda
            if self.call_object(*random_xy).get_content() ==None :
                return self.call_object(*random_xy)

    def add_specific_content(self,content,amount) :#lägger till ett hål mm i random tomt ställe
        if amount ==0 :
            return
        else :
            self.random_empty_room().set_content(content)
            self.add_specific_content(content,amount-1)
            
    def add_all_content (self) : #lägger till massa hål mm till laburinten
        self.difficulty.set_content_multiplier()
        print(self.difficulty.hole_amount())
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
        print(near_content_list)
        return near_content_list
    
    def add_room (self,x,y):#skapar ett rum av klassen Room och lägger det i matrisen
        self.matrix_list[x][y]=Room()
            
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

class Character (object) :#klass för att beskriva var karaktärerna är i x,y led
    def __init__ (self,x,y) :
        self.x=x
        self.y=y
    def change_x (self,new_x) :
        self.x=new_x
    def change_y(self,new_y) :
        self.y=new_y
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y

class Wumpus(Character) :
    pass

class Hunter(Character) :
    pass
    
    
class Difficulty (object) :#håller reda på svårighetsgrad och chanser
    def __init__ (self,difficulty='easy') :
        self.difficulty=difficulty
        self.set_room_multiplier()
        self.set_content_multiplier()
    def get_difficulty(self) :
        return  difficulty
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
        return int(1*self.content_multiplier)
    def find_arrow_amount(self) :
        if self.difficulty=='easy' :
            return 0
        else :
            return int(50/self.content_multiplier)