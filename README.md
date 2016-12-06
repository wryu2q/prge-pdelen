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

import pygame, sys, pickle, shelve


```
##Programflöde och dataflöde


##Plan B och brodering i kanterna
Om det går dåligt och jag får ont om tid så kommer vissa saker plockas bort. Sådant som kan plockas bort är: 
* att spara ett highscore.

sånt som kan läggas till om det ska bli extra fint är: 
* att ge jägaren ett begränsat antal pilar samt pilar som går att plocka upp
* En AI som inte är värdelös.
