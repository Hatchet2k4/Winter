import ika
import riptiles
import system
import effects
import controls

automapdata = { #automap data for all maps because I'm lazy, in (x, y, w, h, maptype) notation
'map01.ika-map' : (10, 32, 3, 2, 'snow'),
'map02.ika-map' : (7, 30, 3, 3, 'snow'),
'map03.ika-map' : (2, 30, 5, 2, 'snow'),
'map04.ika-map' : (2, 27, 2, 3, 'snow'),
'map05.ika-map' : (2, 26, 1, 1, 'cave'),
'map06.ika-map' : (8, 18, 3, 3, 'snow'),
'map07.ika-map' : (11, 17, 4, 2, 'snow'),
'map08.ika-map' : (5, 16, 3, 3, 'snow'),
'map09.ika-map' : (3, 16, 2, 3, 'snow'),
'map10.ika-map' : (3, 14, 2, 2, 'snow'),
'map11.ika-map' : (5, 19, 3, 2, 'snow'),
'map12.ika-map' : (4, 20, 1, 1, 'cave'),
'map13.ika-map' : (15, 17, 4, 2, 'snow'),
'map14.ika-map' : (17, 16, 1, 1, 'snow'),
'map15.ika-map' : (8, 27, 1, 3, 'snow'),
'map16.ika-map' : (19, 15, 3, 3, 'snow'),
'map17.ika-map' : (22, 15, 1, 1, 'snow'),
'map18.ika-map' : (8, 22, 2, 5, 'cave'),
'map19.ika-map' : (16, 13, 3, 3, 'snow'),
'map20.ika-map' : (8, 21, 2, 1, 'snow'),
'map21.ika-map' : (16, 10, 2, 3, 'snow'),
'map22.ika-map' : (18, 1, 1, 1, 'snow'),
'map23.ika-map' : (13, 10, 3, 3, 'snow'),
'map24.ika-map' : (12, 14, 3, 2, 'snow'),
'map25.ika-map' : (9, 10, 4, 3, 'cave'),
'map26.ika-map' : (7, 11, 2, 2, 'cave'),
'map27.ika-map' : (7, 6, 2, 5, 'cave'),
'map28.ika-map' : (8, 4, 1, 2, 'cave'),
'map29.ika-map' : (9, 7, 1, 1, 'cave'),
'map30.ika-map' : (11, 8, 1, 2, 'snow'),
'map31.ika-map' : (11, 6, 2, 2, 'snow'),
'map32.ika-map' : (10, 3, 3, 3, 'snow'),
'map33.ika-map' : (10, 0, 3, 3, 'snow'), 
'map34.ika-map' : (3, 8, 4, 2, 'snow'),
'map35.ika-map' : (4, 6, 2, 2, 'snow'),
'map36.ika-map' : (4, 3, 1, 3, 'snow'),
'map37.ika-map' : (4, 2, 1, 1, 'snow'),
'map38.ika-map' : (1, 9, 2, 1, 'snow'),
'map39.ika-map' : (1, 10, 2, 2, 'snow'),
'map40.ika-map' : (1, 12, 2, 2, 'snow'),
'map41.ika-map' : (5, 11, 2, 3, 'snow'),
'map42.ika-map' : (5, 14, 2, 2, 'snow'),
'map43.ika-map' : (10, 30, 3, 2, 'snow'),
'map44.ika-map' : (13, 29, 3, 3, 'snow'),
'map45.ika-map' : (14, 32, 2, 2, 'snow'),
'map46.ika-map' : (16, 30, 1, 1, 'snow'), 
'map47.ika-map' : (18, 28, 5, 2, 'cave'), 
'map48.ika-map' : (22, 26, 1, 2, 'cave'), 
'map49.ika-map' : (16, 28, 2, 2, 'cave'), 
'map50.ika-map' : (18, 9, 2, 1, 'cave'), 
'map51.ika-map' : (3, 20, 1, 3, 'cave'), 
'map52.ika-map' : (2, 23, 2, 3, 'cave'), 
'map53.ika-map' : (3, 11, 2, 1, 'snow'), 
'map54.ika-map' : (13, 32, 1, 1, 'cave'), 
'map55.ika-map' : (20, 25, 2, 3, 'snow'), 
} 

mapnames = { #all the maps that have save points. Could have used metadata, but this was more convenient.
'map02.ika-map' : 'Mount Durinar Base',
'map11.ika-map' : 'Misty Cliffs',
'map12.ika-map' : 'Misty Cave', 
'map14.ika-map' : 'Lookout Point',
'map30.ika-map' : 'Serpent Valley',
'map38.ika-map' : 'Northwest Summit',
'map50.ika-map' : 'Northeast Cave'
} 

class Automap(object):
    def __init__(self):
        self.maptiles=riptiles.RipTiles('overworld/maptiles.png', 12, 9)
        
        self.bg=ika.Image('overworld/mapbg.png')
        self.cavebg=ika.Image('overworld/mapbg-cave.png')
        
        self.mapwidth=23
        self.mapheight=35
        self.tilewidth=12
        self.tileheight=9
        
        #hack. Todo, implement loading from actual json file
        self.data=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 17, 0, 0, 0, 0, 0, 6, 10, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 35, 0, 12, 5, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 18, 0, 0, 0, 36, 0, 15, 11, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 7, 0, 24, 25, 0, 0, 6, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 16, 0, 30, 31, 20, 0, 15, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 10, 10, 7, 30, 31, 0, 0, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 9, 15, 11, 11, 16, 30, 31, 0, 0, 18, 0, 0, 0, 0, 0, 0, 26, 27, 0, 0, 0, 0, 6, 7, 0, 0, 0, 0, 33, 34, 0, 24, 28, 25, 6, 10, 7, 6, 7, 2, 0, 0, 0, 0, 0, 15, 16, 8, 9, 6, 7, 24, 25, 0, 30, 23, 31, 12, 5, 13, 12, 13, 0, 0, 0, 0, 0, 0, 6, 7, 0, 0, 12, 13, 33, 34, 26, 29, 29, 34, 15, 11, 16, 15, 16, 0, 0, 0, 0, 0, 0, 15, 16, 0, 0, 15, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 10, 7, 0, 0, 0, 0, 0, 0, 0, 6, 7, 6, 7, 0, 0, 0, 0, 0, 24, 28, 25, 0, 12, 5, 13, 0, 0, 0, 0, 0, 0, 0, 15, 16, 15, 16, 0, 0, 0, 0, 0, 33, 29, 34, 0, 15, 11, 16, 6, 10, 7, 2, 0, 0, 0, 6, 7, 6, 10, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 12, 0, 13, 0, 0, 0, 0, 12, 13, 12, 5, 13, 0, 0, 0, 6, 10, 10, 7, 6, 10, 10, 7, 15, 11, 16, 0, 0, 0, 0, 15, 16, 15, 11, 16, 6, 10, 7, 15, 11, 11, 16, 15, 11, 11, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 10, 7, 12, 5, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 35, 20, 15, 11, 16, 15, 11, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 0, 0, 0, 0, 8, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 36, 0, 0, 0, 0, 0, 35, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 35, 0, 0, 0, 0, 0, 22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 0, 0, 0, 0, 0, 22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26, 34, 0, 0, 0, 0, 24, 31, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 0, 0, 0, 0, 0, 33, 34, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 35, 0, 0, 6, 7, 0, 0, 0, 0, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 36, 0, 0, 12, 13, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 24, 27, 24, 28, 28, 28, 25, 0, 0, 15, 16, 0, 0, 0, 0, 18, 0, 0, 0, 0, 6, 10, 7, 36, 0, 33, 29, 29, 29, 34, 0, 0, 6, 10, 10, 10, 7, 6, 10, 7, 6, 10, 7, 12, 5, 13, 2, 0, 0, 0, 0, 0, 0, 0, 0, 15, 11, 11, 11, 16, 12, 5, 13, 15, 11, 16, 15, 11, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 11, 16, 6, 10, 7, 20, 6, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 11, 16, 0, 15, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.icons=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 37, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 38, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 39, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 54, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 54, 38, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 41, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 41, 0, 0, 0, 0, 0, 37, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 39, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 43, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 41, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 37, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 54, 0, 0, 44, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 41, 0, 0, 0, 0, 0, 0, 0, 45, 0, 0, 0, 0, 0, 0, 0, 0, 0, 54, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 39, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 54, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 37, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 40, 0, 0, 45, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 39, 0, 0, 0, 0, 42, 0, 0, 0, 0, 0, 53, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 51, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 38, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 54, 0, 0, 0, 0, 45, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 38, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  
        self.connections=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 48, 0, 0, 0, 48, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 47, 0, 0, 0, 47, 0, 0, 47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 48, 0, 0, 0, 50, 49, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 47, 0, 0, 0, 0, 0, 0, 47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 48, 50, 49, 0, 0, 0, 0, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 47, 0, 0, 0, 0, 0, 48, 48, 0, 0, 47, 0, 0, 0, 50, 49, 50, 49, 0, 0, 0, 0, 0, 48, 50, 49, 50, 49, 0, 47, 47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 47, 0, 0, 0, 0, 0, 0, 50, 49, 0, 0, 0, 0, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 48, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 50, 49, 0, 50, 49, 0, 0, 0, 47, 0, 47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 47, 50, 49, 0, 0, 0, 0, 0, 0, 0, 50, 49, 48, 50, 49, 0, 50, 49, 0, 0, 50, 49, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 50, 52, 0, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 48, 0, 0, 0, 0, 0, 47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 51, 0, 0, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 47, 0, 0, 0, 0, 0, 47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 48, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 50, 49, 0, 47, 0, 47, 0, 0, 48, 0, 0, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 47, 0, 0, 0, 50, 49, 47, 50, 49, 0, 50, 49, 0, 50, 47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 50, 49, 0, 50, 49, 0, 47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.visible=[0]*(self.mapwidth*self.mapheight)
        
        
        
        
        
        
        self.px=0
        self.py=0
        self.frame=0
        self.layer=''
        
        self.total = self.counttotalrooms()
        self.visited = 0 #number of rooms visited
        
        

    def counttotalrooms(self):
        i = 0
        for room in self.data:
            if room > 0: i+=1
        return i
        
    def countvisitedrooms(self):
        i = 0
        for room in self.visible:
            if room > 0: i+=1
        return i
        
        

    def update(self):
        x=y=w=h=0        
        
        if system.engine.mapName in automapdata:                    
            x,y,w,h,self.layer = automapdata[system.engine.mapName]
        
        #refresh which rooms should be visible:
        for tx in range(x, x+w):
           for ty in range(y, y+h):
              self.visible[ty*self.mapwidth+tx]=1
              
        self.visited = self.countvisitedrooms() #number of rooms visited
        
        px = system.engine.player.x
        py = system.engine.player.y        
        
        
        self.py = int((float(py) / ika.Map.height) * h) + y        
        self.px = int((float(px) / ika.Map.width) * w) + x        
        self.ticks=0
        self.time=ika.GetTime()
        
        
    def draw(self, topx, topy):              
        t=ika.GetTime()
        if t>self.time: 
            self.time=t
            self.ticks+=1
            
        if self.layer=='cave': 
            ika.Video.Blit(self.cavebg, topx-2,topy-3)
        else:
            ika.Video.Blit(self.bg, topx-2,topy-3)
        
    
        for y in range(self.mapheight):
            for x in range(self.mapwidth):
                for tset in [self.data, self.icons, self.connections]:
                    tile = tset[y*self.mapwidth+x]
                    if tile and self.visible[y*self.mapwidth+x]: 
                        ika.Video.Blit(self.maptiles[tile-1], topx+(x*self.tilewidth),topy+(y*self.tileheight))
                        
        if self.ticks %30 <15: ika.Video.Blit(self.maptiles[18], topx+(self.px*self.tilewidth), topy+(self.py*self.tileheight))
       
        font = system.engine.font
        pct = round(self.visited * 100.0 / self.total, 1)
        
        if system.engine.mapName in mapnames:                                
            font.Print(20,  10, mapnames[system.engine.mapName])
        font.Print(20,  20, 'Map Completion: ' + str(pct) + '%')
        

class MapScreen(object):
    def __init__(self):        
        self.maxscroll = 110
        self.scroll = self.maxscroll
        
    def update(self):
        pass
        
    def show(self):
        self.images = effects.createBlurImages()
    
    def hide(self):
        pass
    
    def draw(self, opacity = 255):
        pass
        
    def run(self):
        self.show()          
        
        topx=12
        topy=12
        
        while True:            
            ika.Video.ScaleBlit(self.images[-1], 0, 0, ika.Video.xres, ika.Video.yres, ika.Opaque)
            ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, 128), True)
            
            map.draw(topx, topy-self.scroll)
            
            ika.Video.ShowPage()
            ika.Input.Update()
            
            if controls.cancel() or controls.showmap(): 
                break
            
            if controls.down() and self.scroll < self.maxscroll: 
                self.scroll+=1
            elif controls.up() and self.scroll > 0: 
                self.scroll-=1
        
        
map = Automap()        
        