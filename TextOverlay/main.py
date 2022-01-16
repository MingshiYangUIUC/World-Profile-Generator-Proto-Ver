#!C:\Users\yangm\Anaconda3\python.exe

from TextOverlay import *
import sys
import os

if __name__ == '__main__':
    #print(os.getcwd())
    imin = int(sys.argv[1])
    try:
        imax = int(sys.argv[2])
    except:
        imax = imin + 1
    for i in range(imin,imax):
        f = open(f'saved/worldfeatures{i}.txt','r', encoding='utf-8')
        texts = []
        for l in f.readlines():
            texts.append(eval(l))
        '''
        test_texts = [[['area', '112896m²'], (255, 255, 255)], [['land', '50.87%'], (255, 255, 255)], [['water', '49.13%'], (255, 255, 255)], [['soil', '23.33%'], (255, 255, 255)]],\
                    [['lukewarm_ocean', (51, 255, 51)], ['swamp', (0, 128, 255)], ['windswept_savanna', (255, 51, 255)], ['warm_ocean', (0, 128, 255)], ['savanna', (51, 255, 51)], ['forest', (255, 255, 255)], ['beach', (255, 255, 255)], ['river', (255, 255, 255)]],\
                    [[['Amethyst', '6.05%'], (0, 128, 255)], [['Diamond', '3.97%'], (255, 255, 255)], [['Gold', '7.03%'], (255, 255, 255)], [['Emerald', '0.0%'], (255, 255, 255)], [['Bone', '0.0%'], (255, 255, 255)], [['Copper', '21.33%'], (255, 255, 255)], [['Iron', '22.61%'], (51, 255, 51)], [['Coal', '22.76%'], (255, 255, 255)], [['Lapis', '6.53%'], (255, 255, 255)], [['Redstone', '9.72%'], (255, 255, 255)]],\
                    [['ocean_ruin', (51, 255, 51)], ['mineshaft', (255, 255, 255)], ['more metal', (51, 255, 51)], ['more gem', (51, 255, 51)], ['multiclimate', (51, 255, 51)], ['uncommon biomes', (255, 128, 0)], ['corals', (0, 128, 255)]]
        '''
        add_text_to_img(texts,i,i+1)
