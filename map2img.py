    
    
    def Map2Img(self, mapName, tiles):            
        ika.Log('Saving map ' + mapName)
        ika.Map.Switch('maps/' + mapName + '.ika-map')
        
        canvas = ika.Canvas(ika.Map.width, ika.Map.height)                
                
        for y in range(int(ika.Map.height/16)):
            for x in range(int(ika.Map.width/16)):
                for l in range(ika.Map.layercount):
                    t=ika.Map.GetTile(x,y,l)
                    tiles[t].Blit(canvas, x*16, y*16, ika.AlphaBlend)
                    
        canvas.Save('map2img/' +  mapName + '.png')
                    
    def rip_tiles(self, image, width, height, span, tilecount):
        """This is a simple function that takes any image that is formatted
        like a tileset and rips the tiles into a list which is then
        returned.

        image - image to rip from
        width/height - width and height of a single tile
        span - how many tiles per row
        tilecount - number of tiles to rip
        """
        tiles = []
        big_image = ika.Canvas(image)
        for i in range(tilecount):
            tile = ika.Canvas(width, height)
            big_image.Blit(tile, -1 - (i % span * (width + 1)),
                           -1 - (i / span * (height + 1)), ika.Opaque)
            #tiles.append(ika.Image(tile))
            tiles.append(tile)
        return tiles        

    def Map2TMX(mapName):
            
        ika.Log('Saving map ' + mapName)
        ika.Map.Switch('maps/' + mapName + '.ika-map')
        
        twidth = theight = 16
        
        mheight = ika.Map.height / theight
        mwidth = ika.Map.width / twidth
        
        #canvas = ika.Canvas(ika.Map.width, ika.Map.height) 
        s = '''<?xml version="1.0" encoding="UTF-8"?>
<map version="1.2" tiledversion="2020.02.12" orientation="orthogonal" renderorder="right-down" compressionlevel="0" 
width="''' + str(100) + '''" height="''' + str(100) + '''" tilewidth="''' +str(twidth) + '''" tileheight="''' + str(theight) +   '''" infinite="0" nextlayerid="5" nextobjectid="1">
 <tileset firstgid="1" source="''' + ika.Map.tilesetname + '''.tsx"/> '''
        
        for l in range(ika.Map.layercount):                
            n, w,h, wrapx,wrapy = ika.Map.GetLayerProperties(l)
            lwidth = w / twidth
            lheight = h / theight
            
            s+= '''<layer id="''' +str(l + 1)  '''" name="''' + n + '''" width="''' +  str(lwidth) +  
            '''height="''' + str(lheight) +  '''">
            <data encoding="csv"> '''          
            
            
            for y in range(int(ika.Map.height/16)):
                for x in range(int(ika.Map.width/16)):
                
                    t=ika.Map.GetTile(x,y,l)
                    s+= str(t) +','
                    #tiles[t].Blit(canvas, x*16, y*16, ika.AlphaBlend)
            +'</data></layer>'
        s+='</map>'
        
        file('maps/' + mapName + '.tmx', 'wt').write(s)                    
        #canvas.Save('map2img/' +  mapName + '.png')
                    
        
    def saveallmaps():
        savemaps=[]
        #tiles=self.rip_tiles('tiles.png', 16, 16, 6, 503)
        
        #hack!
        for i in range(1, 10):
            savemaps.append('map0'+str(i)) 
        for i in range(10, 51):
            if i in [33, 20, 18, 15]: #these maps don't exist!
                pass
            else: 
                savemaps.append('map'+str(i))

        ika.Log('maps: ' + str(savemaps))
        
        for m in savemaps:
            #self.Map2Img(m, tiles)    
            self.Map2TMX(m)
            
            