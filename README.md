#Wumpus
wumpus är ett spel som är skrivet i python som går ut på att man är en jägare i en slumpad laburint och med sin pilbåge ska man skjuta månstret wumpus.
##installation
notera att för närvarande så är programet ingen .exe så man måsta köra programet via terminalen eller motsvarande.
för att köra spelet så måste man först och främst instalera python 3 och pygame.Sedan så behöver man skapa en mapp som programmet ska köra i. i mappen så ska man lägga filerna:
* huvudProgramet.py
* wumpusclasses.py
* wumpus.png
* bow.png
* bow_drawn.png
* [pygame_textinput] (https://github.com/Nearoo/pygame-text-input)

För att köra spelet så kör man huvudProgramet.py med python3 

###eventuella fel
om spelet inte kör så gissar jag på att något av följande är fel:
* du kör filen i något annat är python3 
* du har glömt att hämta [pygame_textinput] (https://github.com/Nearoo/pygame-text-input) som inte ligger här eller döpt filen annat än pygame_textinput.py
* pygame inkluderas inte i python3 och kan vara meckigt att instalera
~~* låg IQ~~

ett fel som troligen kommer uppstå är att listor kan se ut att vara ostruckturerade eftersom spelet för närvarande använder sig av ubuntumono vilket är en font som finns för ubuntu. angående fel med fonts så borde programet inte crasha om fonten inte finns med din version av pygame,eftersom pygame borde ta pygames standardfont om fonten saknas.
##övrigt
det borde stå nogot fint här men jag kommer inte på vad, gissar att nått som kan vara kul att veta att spelet är ett skolprojekt...
