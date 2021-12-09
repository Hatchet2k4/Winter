import ika
import riptiles
import system
import effects
import controls

#automap data for all maps because I'm lazy, in (x, y, w, h, maptype) notation
automapdata = {
'map01.ika-map' : (10, 32, 3, 2, 'snow', 'Southern Ravine'),
'map02.ika-map' : (7, 30, 3, 3, 'snow', 'Mount Durinar Base'),
'map03.ika-map' : (2, 30, 5, 2, 'snow', 'Western Ravine'),
'map04.ika-map' : (2, 27, 2, 3, 'snow', 'Durinar Cairn Stones'),
'map05.ika-map' : (2, 26, 1, 1, 'cave', 'Cairn Cave'),
'map06.ika-map' : (8, 18, 3, 3, 'snow', 'Durinar Ascent'),
'map07.ika-map' : (11, 17, 4, 2, 'snow', 'Spur Cliffs'),
'map08.ika-map' : (5, 16, 3, 3, 'snow', 'Central Lake Durinar'),
'map09.ika-map' : (3, 16, 2, 2, 'snow', 'West Lake Durinar'),
'map10.ika-map' : (3, 14, 2, 2, 'snow', 'Yeti Pond'),
'map11.ika-map' : (5, 19, 3, 2, 'snow', 'Misty Cliffs'),
'map12.ika-map' : (5, 20, 1, 1, 'cave', 'Misty Cave Entrance'),
'map13.ika-map' : (15, 17, 4, 2, 'snow', 'Foggy Foothills'),
'map14.ika-map' : (17, 16, 1, 1, 'snow', 'Lookout Point'),
'map15.ika-map' : (8, 27, 1, 3, 'snow', 'Lower Durinar River'),
'map16.ika-map' : (19, 15, 3, 3, 'snow', 'Fog Valley'),
'map17.ika-map' : (22, 15, 1, 2, 'snow', 'Eastern Caves'),
'map18.ika-map' : (8, 22, 2, 5, 'cave', 'Lower Durinar Cave'),
'map19.ika-map' : (16, 13, 3, 3, 'snow', 'Donut Hills'),
'map20.ika-map' : (9, 21, 1, 1, 'snow', 'Lower Cave Exit'),
'map21.ika-map' : (16, 10, 2, 3, 'snow', 'Northeast Cliffs'),
'map22.ika-map' : (18, 10, 1, 1, 'snow', 'Northeast Summit'),
'map23.ika-map' : (13, 10, 3, 3, 'snow', 'Labyrinth Heights'),
'map24.ika-map' : (11, 8, 3, 2, 'snow', 'Rune Temple'),
'map25.ika-map' : (9, 10, 4, 3, 'cave', 'Devourer Den East'),
'map26.ika-map' : (7, 11, 2, 2, 'cave', 'Devourer Den West'),
'map27.ika-map' : (7, 6, 2, 5, 'cave', 'Devourer Den Northwest'),
'map28.ika-map' : (8, 4, 1, 2, 'cave', 'Bone Chamber'),
'map29.ika-map' : (9, 7, 1, 1, 'cave', 'Gorilla Lair'),
'map30.ika-map' : (10, 8, 1, 2, 'snow', 'Serpent Valley'),
'map31.ika-map' : (10, 6, 2, 2, 'snow', 'Serpent Valley North'),
'map32.ika-map' : (9, 3, 3, 3, 'snow', 'Serpent River'),
'map33.ika-map' : (10, 0, 3, 3, 'snow', 'Durinar Descent'), 
'map34.ika-map' : (3, 8, 4, 2, 'snow', 'Bridge Cliffs'),
'map35.ika-map' : (4, 6, 2, 2, 'snow', 'Summit River'),
'map36.ika-map' : (4, 3, 1, 3, 'snow', 'Summit Lake'),
'map37.ika-map' : (4, 2, 1, 1, 'snow', 'Northwest Summit'),
'map38.ika-map' : (1, 9, 2, 1, 'snow', 'Northwest Camp'),
'map39.ika-map' : (1, 10, 2, 2, 'snow', 'Bridge Crossing'),
'map40.ika-map' : (1, 12, 2, 2, 'snow', 'Western Hill'),
'map41.ika-map' : (5, 11, 2, 3, 'snow', 'Durinar Forest'),
'map42.ika-map' : (5, 14, 2, 2, 'snow', 'Upper Durinar River'),
'map43.ika-map' : (10, 30, 3, 2, 'snow', 'Durinar Creek'),
'map44.ika-map' : (13, 29, 3, 3, 'snow', 'Ice Floats Maze'),
'map45.ika-map' : (14, 32, 2, 2, 'snow', 'Damaged Bridge'),
'map46.ika-map' : (16, 30, 1, 1, 'snow', 'Hidden Den'), 
'map47.ika-map' : (18, 28, 5, 2, 'cave', 'Carnivore Den'), 
'map48.ika-map' : (21, 26, 2, 2, 'cave', 'Nesting Area'), 
'map49.ika-map' : (16, 28, 2, 2, 'cave', 'Den Entrance'), 
'map50.ika-map' : (18, 9, 2, 1, 'cave', 'Northeast Cave'), 
'map51.ika-map' : (3, 20, 2, 3, 'cave', 'Upper Misty Cave'), 
'map52.ika-map' : (2, 23, 2, 3, 'cave', 'Lower Misty Cave'), 
'map53.ika-map' : (3, 11, 2, 1, 'snow', 'Land Bridge'), 
'map54.ika-map' : (13, 32, 1, 1, 'cave', 'Dragonpup Nest'), 
'map55.ika-map' : (19, 25, 2, 3, 'snow', 'Durinar Island'), 
} 

mapnames = { #all the maps that have save points. Could have used metadata, but this was more convenient.
'map02.ika-map' : 'Mount Durinar Base',
'map08.ika-map' : 'Lake Durinar',
'map11.ika-map' : 'Misty Cliffs',
'map12.ika-map' : 'Misty Cave', 
'map14.ika-map' : 'Lookout Point',
'map30.ika-map' : 'Serpent Valley',
'map38.ika-map' : 'Northwest Summit',
'map50.ika-map' : 'Northeast Cave'
} 

icontiles = {
'TNT': 37,
'Strength': 38,
'Guard': 39,
'Power': 40,
'Boulder': 41,
'Water': 42,
'Fire': 43,
'Wind': 44,
'Lightning': 46
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
        self.data=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 17, 0, 0, 0, 0, 6, 10, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 35, 12, 5, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 18, 0, 0, 0, 36, 15, 11, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 7, 0, 24, 25, 0, 6, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 16, 0, 30, 31, 20, 15, 16, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 10, 10, 7, 30, 31, 0, 17, 24, 28, 25, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 9, 15, 11, 11, 16, 30, 31, 0, 18, 33, 29, 34, 1, 0, 0, 0, 26, 27, 0, 0, 0, 0, 6, 7, 0, 0, 0, 0, 33, 34, 0, 24, 28, 25, 6, 10, 7, 6, 7, 2, 0, 0, 0, 0, 0, 15, 16, 8, 9, 6, 7, 24, 25, 0, 30, 23, 31, 12, 5, 13, 12, 13, 0, 0, 0, 0, 0, 0, 6, 7, 0, 0, 12, 13, 33, 34, 26, 29, 29, 34, 15, 11, 16, 15, 16, 0, 0, 0, 0, 0, 0, 15, 16, 0, 0, 15, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 10, 7, 0, 0, 0, 0, 0, 0, 0, 6, 7, 6, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 5, 13, 0, 0, 0, 0, 0, 0, 0, 15, 16, 15, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 11, 16, 6, 10, 7, 17, 0, 0, 0, 6, 7, 6, 10, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 12, 0, 13, 18, 0, 0, 0, 12, 13, 12, 5, 13, 0, 0, 0, 6, 10, 10, 7, 6, 10, 10, 7, 15, 11, 16, 0, 0, 0, 0, 15, 16, 15, 11, 16, 6, 10, 7, 15, 11, 11, 16, 15, 11, 11, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 10, 7, 12, 5, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 24, 27, 20, 15, 16, 15, 11, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 36, 0, 0, 0, 0, 0, 35, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 24, 25, 0, 0, 0, 0, 0, 22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 30, 31, 0, 0, 0, 0, 0, 22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 33, 34, 0, 0, 0, 0, 24, 31, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 9, 0, 0, 0, 0, 20, 0, 0, 0, 0, 0, 33, 34, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 24, 25, 0, 0, 6, 7, 0, 0, 0, 0, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 33, 34, 0, 0, 12, 13, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 24, 25, 24, 28, 28, 28, 25, 0, 0, 15, 16, 0, 0, 0, 0, 18, 0, 0, 0, 0, 6, 7, 1, 33, 34, 33, 29, 29, 29, 34, 0, 0, 6, 10, 10, 10, 7, 6, 10, 7, 6, 10, 7, 12, 5, 7, 2, 0, 0, 0, 0, 0, 0, 0, 0, 15, 11, 11, 11, 16, 12, 5, 13, 15, 11, 16, 15, 11, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 11, 16, 6, 10, 7, 20, 1, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 11, 16, 0, 8, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.connections=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 48, 0, 0, 0, 48, 0, 58, 59, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 47, 0, 0, 0, 47, 0, 56, 57, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 48, 0, 0, 0, 50, 49, 48, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 47, 0, 50, 49, 0, 0, 47, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 48, 50, 49, 0, 0, 0, 0, 0, 0, 48, 1, 0, 48, 0, 0, 0, 0, 48, 0, 0, 0, 0, 0, 47, 0, 0, 0, 0, 0, 48, 48, 0, 47, 1, 0, 47, 0, 50, 49, 50, 60, 0, 0, 0, 0, 0, 48, 50, 49, 50, 49, 0, 47, 47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 47, 0, 0, 0, 0, 0, 0, 50, 49, 0, 0, 50, 49, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 48, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 50, 49, 0, 50, 49, 0, 0, 0, 47, 0, 47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 47, 50, 49, 0, 0, 0, 0, 0, 0, 0, 50, 49, 48, 50, 49, 0, 50, 49, 0, 0, 50, 49, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 50, 52, 49, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 51, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 48, 0, 0, 0, 0, 0, 47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 51, 0, 0, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 47, 0, 0, 0, 0, 0, 47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 48, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 50, 49, 47, 0, 0, 47, 0, 0, 48, 0, 0, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 47, 0, 0, 0, 50, 49, 47, 50, 49, 0, 50, 49, 0, 50, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 50, 49, 0, 50, 49, 0, 47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.icons=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 37, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 38, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 39, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 54, 0, 0, 41, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 41, 0, 0, 0, 0, 0, 0, 46, 48, 0, 0, 0, 0, 54, 38, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 37, 0, 0, 0, 0, 41, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 41, 0, 0, 0, 39, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 39, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 43, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 39, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 37, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 54, 0, 0, 44, 0, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 54, 0, 0, 0, 0, 41, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 39, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 38, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 37, 0, 0, 0, 0, 37, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 42, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 38, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 38, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 54, 0, 0, 0, 0, 0, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 39, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]        
        self.visiblerooms=[0]*(self.mapwidth*self.mapheight)
        self.visitedrooms=[0]*(self.mapwidth*self.mapheight)
        self.collected=[0]*(self.mapwidth*self.mapheight)

        self.px=0
        self.py=0        
        self.maptype=''
        
        self.total = self.counttotalrooms()
        self.visited = 0 #number of rooms visited
        self.time=ika.GetTime()
        self.ticks=0



    def counttotalrooms(self):
        i = 0
        for room in self.data:
            if room > 0: i+=1
        return i
        
    def countvisitedrooms(self):
        i = 0
        for room in self.visitedrooms:
            if room > 0: i+=1
        return i
        
        

    def update(self):
        x=y=w=h=0        
        
        if system.engine.mapName in automapdata:                    
            x,y,w,h,self.maptype,mapname = automapdata[system.engine.mapName]
        
        #update current room to be visible in map data
        if system.engine.mapName=='map11.ika-map': #special case for oddly shaped map        
            for xy in [(0,0), (1,0), (2,0), (1, 1), (2, 1)]:
                tx=x+xy[0]
                ty=y+xy[1]
                self.visiblerooms[ty*self.mapwidth+tx]=1
            
        else: #normal maps
            for tx in range(x, x+w):
               for ty in range(y, y+h):
                  self.visiblerooms[ty*self.mapwidth+tx]=1

        
        if system.engine.player: #player may not be inited yet
            px = system.engine.player.x
            py = system.engine.player.y                        
            self.py = int((float(py) / ika.Map.height) * h) + y        
            self.px = int((float(px) / ika.Map.width) * w) + x        

        self.visitedrooms[self.py*self.mapwidth+self.px]=1 #mark current player location as visited
        self.visited = self.countvisitedrooms() #refresh number of rooms visited
            
        self.ticks=0
        self.time=ika.GetTime()
        
        
    def draw(self, topx, topy):              
        t=ika.GetTime()
        if t>self.time: 
            self.time=t
            self.ticks+=1
            
        if self.maptype=='cave': 
            ika.Video.Blit(self.cavebg, topx-2,topy-3)
        else:
            ika.Video.Blit(self.bg, topx-2,topy-3)
            
        for y in range(self.mapheight):
            for x in range(self.mapwidth):
                for tset in [self.data, self.connections]:
                    tile = tset[y*self.mapwidth+x]
                    if tile and self.visitedrooms[y*self.mapwidth+x]: 
                        ika.Video.Blit(self.maptiles[tile-1], topx+(x*self.tilewidth),topy+(y*self.tileheight))                        
                    elif tile and self.visiblerooms[y*self.mapwidth+x]:                         
                        ika.Video.TintBlit(self.maptiles[tile-1], topx+(x*self.tilewidth),topy+(y*self.tileheight), ika.RGB(100,100,100))                    
                tile = self.icons[y*self.mapwidth+x]
                if tile and self.visitedrooms[y*self.mapwidth+x]:
                    if self.collected[y*self.mapwidth+x]: #item collected, mark green
                        ika.Video.TintBlit(self.maptiles[tile-1], topx+(x*self.tilewidth),topy+(y*self.tileheight), ika.RGB(20,250,20))                    
                        #ika.Video.Blit(self.maptiles[tile-1], topx+(x*self.tilewidth),topy+(y*self.tileheight))                        
                        #ika.Video.TintBlit(self.maptiles[4], topx+(x*self.tilewidth),topy+(y*self.tileheight), ika.RGB(20,250,20, 128))                    
                    else: #not collected, draw normal
                        ika.Video.Blit(self.maptiles[tile-1], topx+(x*self.tilewidth),topy+(y*self.tileheight))                        
                        #ika.Video.TintBlit(self.maptiles[tile-1], topx+(x*self.tilewidth),topy+(y*self.tileheight), ika.RGB(100,100,100))                    
                
                        
        if self.ticks %40 <20: ika.Video.Blit(self.maptiles[18], topx+(self.px*self.tilewidth), topy+(self.py*self.tileheight))
       
        font = system.engine.font
        pct = self.getMapPct()
        
        if system.engine.mapName in automapdata:                                
            m = automapdata[system.engine.mapName][5]
            font.Print(20,  10, m)
        font.Print(20,  20, 'Map Completion: ' + str(pct) + '%')
        
    def getMapPct(self):
        return round(self.visited * 100.0 / self.total, 1)

    def SetCollected(self, tilename): #check current room for tile to mark as collected
        tile = icontiles[tilename]                
        x,y,w,h,maptype,mapname = automapdata[system.engine.mapName]
        #ika.Log("Set Collected "+tilename)
        #ika.Log(str(tile))
        for tx in range(x, x+w):
           for ty in range(y, y+h):
              if self.icons[ty*self.mapwidth+tx]==tile:
                #ika.Log('Found:'+str(self.icons[ty*self.mapwidth+tx]))
                self.collected[ty*self.mapwidth+tx]=1        


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
        map.update()
        topx=12
        topy=12
        
        while True:            
            ika.Video.ScaleBlit(self.images[-1], 0, 0, ika.Video.xres, ika.Video.yres, ika.Opaque)
            ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, 128), True)
            
            map.draw(topx, topy-self.scroll)
            
            ika.Video.ShowPage()
            ika.Input.Update()
            
            if controls.cancel() or controls.ui_cancel() or controls.joy_cancel() or controls.showmap(): 
                break
            
            if (controls.down() or controls.ui_down() or controls.joy_down()) and self.scroll < self.maxscroll: 
                self.scroll+=1
            elif (controls.up() or controls.ui_up() or controls.joy_up()) and self.scroll > 0: 
                self.scroll-=1
        
        
map = Automap()        
        