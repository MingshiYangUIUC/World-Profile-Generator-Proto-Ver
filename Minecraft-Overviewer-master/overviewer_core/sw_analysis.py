
from pydoc import pager
import numpy as np
from PIL import Image
import time
import os
def packed_longarray_to_shorts_v116_nbt(long_array, n): #Borrowed from Overviewer
    bits_per_value = max(4, (len(long_array) * 64) // n)
    b = np.asarray(long_array, dtype=np.uint64)
    result = np.zeros((n,), dtype=np.uint16)
    shorts_per_long = 64 // bits_per_value
    mask = (1 << bits_per_value) - 1
    for i in range(shorts_per_long):
        j = (n + shorts_per_long - 1 - i) // shorts_per_long
        result[i::shorts_per_long] = (b[:j] >> (bits_per_value * i)) & mask
    return result

def inspect_save_chunk(nbtdata,X,Z,outdir):
    ti = time.time()
    C = nbtdata[1]
    BLOCKS = []
    DATA = np.zeros((16,16**3),dtype=int)
    Biomes = []
    Surface = []
    Ores = []
    Stru = []
    SP,CS = 0,0
    sfc = (packed_longarray_to_shorts_v116_nbt(C['Heightmaps']['WORLD_SURFACE'],256)-65).reshape(16,16)
    i = 0
    for s in C['sections']:
        if len(s['block_states']['palette'])!=1:
            #print(len(s['block_states']['data']))
            data = np.array((s['block_states']['data']))
            unpacked_data = packed_longarray_to_shorts_v116_nbt(data,4096)
            #DATA.append(unpacked_data)
            DATA[i,:] = unpacked_data
        else:
            #DATA.append(np.zeros(4096,dtype=int))
            pass
        #print([b['Name'][10:] for b in s['block_states']['palette']])
        blks = [b['Name'][10:] for b in s['block_states']['palette']]
        for blk in blks:
            if 'spawner' in blk:
                SP += 1
            elif 'chest' in blk:
                CS += 1
        BLOCKS.append(blks)
        biom = s['biomes']['palette']
        for b in biom:
            if b[10:] not in Biomes:
                Biomes.append(b[10:])
        i += 1

    Ymax = int(np.max(sfc))
    Ymin = int(np.min(sfc))
    
    Sfc_data = [[['' for i in range(16)]for j in range(Ymin,Ymax+1)] for k in range(16)]
    for x in range(16):
        for y in range(Ymin,Ymax+1): #dont look for coal to save time, but use 256 if in badland biome, use 320 if in emerald biomes
            for z in range(16):
                blockpos = int(y%16*16*16+z*16+x)
                section = y//16+4
                block = BLOCKS[section][DATA[section,blockpos]]
                Sfc_data[x][y-Ymin][z] = block

    Chunk = []
    Jump = 7
    shift = np.random.randint(Jump)
    for c in range(Jump,int(16*16*(Ymax+64)/Jump)):
        blockpos = (c*Jump-shift) % 4096
        section = (c*Jump-shift) // 4096
        block = BLOCKS[section][DATA[section,blockpos]]
        '''if '_ore' in block or 'bone' in block or 'amethyst' in block:
            Ores.append(block)
            pass'''
        if block != 'stone' and ('_ore' in block or 'bone' in block or 'amethyst' in block):
            Ores.append(block)
            pass
        Chunk.append(block)
    
    for x in range(16):
        for z in range(16):
            y = sfc[z][x]
            Surface.append(Sfc_data[x][y-Ymin][z])

    struct = C['structures']
    for st in struct['References'].keys():
        if struct['References'][st] != ():
            Stru.append(st)

    #BIOMES.append(Biomes)
    #print(Surface)
    #SURFACES.append(Surface)
    f = open(f'{outdir}/data_{X}_{Z}_.txt','w')
    f.write(str(Ores)+'\n')
    f.write(str(Biomes)+'\n')
    f.write(str(Surface)+'\n')
    f.write(str(Stru)+'\n')
    f.write(str(SP)+' '+str(CS)+'\n')
    tf = time.time()-ti
    f.write(str(tf))
    f.close()
    pass





def tilestopng(outdir):
    #time.sleep(1)
    ref = Image.open(f'{outdir}/world-lighting/base.png')
    box = ref.getbbox()
    if (box[2]-box[0]) > 200:
        print('Normal set png')
        depth = 4
        L = 384*2**depth
        imagebig = Image.new('RGBA', (L,L))
        FL = []
        FI = []
        for a in range(4):
            for b in range(4):
                for c in range(4):
                    for d in range(4):
                        try:
                            FL.append(Image.open(f'{outdir}/world-lighting/{a}/{b}/{c}/{d}.png'))
                            FI.append([a,b,c,d])
                        except:
                            pass

        for i in range(len(FI)):
            im = FL[i]
            loc = FI[i]
            x,y = 0,0
            mtp = 1
            for lc in loc:
                if lc // 2 == 1:
                    y += 2**(-mtp)*L
                if lc % 2 == 1:
                    x += 2**(-mtp)*L
                mtp += 1
            x,y = int(x),int(y)
            imagebig.paste(im,(x,y))
        a,b,c,d = imagebig.getbbox()
        imagesm = imagebig.crop((a,b,c,d))
        xw = abs(c-a)
        yw = abs(d-b)
        xb = int(L/2-xw/2)
        yb = int(L/2-yw/2)
        imagebig = Image.new('RGBA', (6144,6144))
        imagebig.paste(imagesm,(xb,yb))
        imagebig.save(f'{outdir}/hdimage.png',"PNG")
        #size = os.path.getsize(f'{outdir}/hdimagexxxx.png')
    else:
        print('Deeper set png')
        depth = 5
        L = 384*2**depth
        imagebig = Image.new('RGBA', (L,L))
        FL = []
        FI = []
        for a in range(4):
            for b in range(4):
                for c in range(4):
                    for d in range(4):
                        for e in range(4):
                            try:
                                FL.append(Image.open(f'{outdir}/world-lighting/{a}/{b}/{c}/{d}/{e}.png'))
                                FI.append([a,b,c,d,e])
                            except:
                                pass

        for i in range(len(FI)):
            im = FL[i]
            loc = FI[i]
            x,y = 0,0
            mtp = 1
            for lc in loc:
                if lc // 2 == 1:
                    y += 2**(-mtp)*L
                if lc % 2 == 1:
                    x += 2**(-mtp)*L
                mtp += 1
            x,y = int(x),int(y)
            imagebig.paste(im,(x,y))
        a,b,c,d = imagebig.getbbox()
        imagesm = imagebig.crop((a,b,c,d))
        xw = abs(c-a)
        yw = abs(d-b)
        xb = int(L/2/2-xw/2)
        yb = int(L/2/2-yw/2)
        imagebig = Image.new('RGBA', (384*2**(depth-1),384*2**(depth-1)))
        imagebig.paste(imagesm,(xb,yb))
        imagebig.save(f'{outdir}/hdimage.png',"PNG")
        #size = os.path.getsize(f'{outdir}/hdimage.png')
    pass



def read_chunkdata(outdir): #The loops inside don't use much time so I don't try optimize them.
    Gold_biomes = ['minecraft:badlands','minecraft:wooded_badlands','minecraft:eroded_badlands']
    Emerald_biomes = ['minecraft:meadow','minecraft:grove','minecraft:snowy_slopes','minecraft:jagged_peaks','minecraft:frozen_peaks','minecraft:stony_peaks','minecraft:windswept_hills','minecraft:windswept_forest','minecraft:windswept_gravelly_hills']
    ORES = []
    BIOMES = []
    SURFACE = []
    STR = []
    SP,CS = 0,0

    d = open(f'{outdir}/domain.txt','r').readlines()
    D= []

    for ds in d:
        if len(ds)>3:
            D.append(ds.split())
    DD = np.zeros((len(D),2))
    for i in range(len(D)):
        for j in range(2):
            try:
                DD[i][j] += int(D[i][j])
            except:
                try:
                    DD[i][j] += int(D[i-1][j])
                except:
                    try:
                        DD[i][j] += int(D[i+1][j])
                    except:
                        pass

    xmin,zmin = np.int32(np.min(DD,axis=0))
    xmax,zmax = np.int32(np.max(DD,axis=0))

    for X in range(xmin,xmax+1):
        for Z in range(zmin,zmax+1):
            try:
                ff = open(f'{outdir}/data_{X}_{Z}_.txt','r')
                f = ff.readlines()
                ff.close()
                expression = f[0]
                exp_as_func = eval('lambda: ' + expression)
                ORES += exp_as_func()
                expression = f[1]
                exp_as_func = eval('lambda: ' + expression)
                BIOMES += exp_as_func()
                expression = f[2]
                exp_as_func = eval('lambda: ' + expression)
                SURFACE += exp_as_func()
                expression = f[3]
                exp_as_func = eval('lambda: ' + expression)
                STR += exp_as_func()

                spcs = f[4].split()
                SP += int(spcs[0])
                CS += int(spcs[1])
            except:pass
    #print(spcs)
    Ustructure = list(set(STR))
    BIOMES = list(set(BIOMES))
        
    EB = []
    GB = []
    for biomes in BIOMES:
        for b in biomes:
            if b in Emerald_biomes:
                if b not in EB:
                    EB.append(b)
            if b in Gold_biomes:
                if b not in GB:
                    GB.append(b)



    dm,gd,em,bn,cp,ir,cl,lp,rs,am,sp,cs = 0,0,0,0,0,0,0,0,0,0,0,0
    tot_ore = len(ORES)
    for ore in ORES:
        if 'coal' in ore:
            cl += 1
        elif 'gold' in ore:
            gd += 1
        elif 'iron' in ore:
            ir += 1
        elif 'emerald' in ore:
            em += 1
        elif 'bone' in ore:
            bn += 1
        elif 'copper' in ore:
            cp += 1
        elif 'diamond' in ore:
            dm += 1
        elif 'lapis' in ore:
            lp += 1
        elif 'redstone' in ore:
            rs += 1
        elif 'amethyst' in ore:
            am += 1
        elif 'spawner' in ore:
            sp += 1
        elif 'chest' in ore:
            cs += 1
    if bn > 0:
        Ustructure.append('fossil')
    

    stone = 0
    veggies = 0
    water = 0
    ores = 0
    tot_surf = 0
    soil = 0
    sandy = 0
    snow = 0
    for blk in SURFACE:
        tot_surf += 1
        if 'stone' in blk:
            stone += 1
        if 'ore' in blk:
            ores += 1
        if 'water' in blk:
            water += 1
        if 'leaves' in blk:
            veggies += 1
        if 'dirt' in blk or 'grass_block' in blk:
            soil += 1
        if 'sand' in blk:
            sandy += 1
        if 'snow' in blk or 'ice' in blk:
            snow += 1
    #print(veggies)
    ore_types = list(set(ORES))
    if len(EB) > 0:
        print(f'Emerald biomes found: {EB}.')
    if len(GB) > 0:
        print(f'gold biomes found: {GB}.')
    print(f'Unique structures found: {Ustructure}.')
    print(f'# Spawner chunks: {SP}, # Chest chunks: {CS}.')
    print(f'Ore composition: Amethyst: {round(am/tot_ore*100,2)}%, Diamond: {round(dm/tot_ore*100,2)}%, Gold: {round(gd/len(ORES)*100,2)}%, Emerald: {round(em/len(ORES)*100,2)}%.')
    print(f'Land coverage: Stone: {round(stone/tot_surf*100,2)}%, Soil: {round(soil/tot_surf*100,2)}%, Veggies: {round(veggies/tot_surf*100,2)}%, Water: {round(water/tot_surf*100,2)}%, Ores: {round(ores/tot_surf*100,2)}%.')
    
    #return features, which can be used to generate pictures.
    return BIOMES,EB,GB,SP,CS,Ustructure,ore_types,am/tot_ore,dm/tot_ore,gd/tot_ore,em/tot_ore,bn/tot_ore,cp/tot_ore,ir/tot_ore,cl/tot_ore,lp/tot_ore,rs/tot_ore,stone/tot_surf,soil/tot_surf,veggies/tot_surf,water/tot_surf,ores/tot_surf,sandy/tot_surf,snow/tot_surf


def get_rarity(summary):
    # 25, 10, 05, 01

    r_sp = np.float32(np.asarray('20.798376047090418 26.274671437360304 30.21856580532989 39.28133223049182'.split()))
    r_cs = np.float32(np.asarray('24.87356649807305 30.67987811454462 34.78232371537665 44.0109458092009'.split()))
    r_am = np.float32(np.asarray('0.04857621968925925 0.057823652996992825 0.06392426595204993 0.07664649073272997'.split()))
    r_em = np.float32(np.asarray('0.0013639611916549308 0.0029665996463801364 0.004724372701815549 0.01131236781573449'.split()))
    r_cl = np.float32(np.asarray('0.26593068907135825 0.29537521422845586 0.3145483112705915 0.3539644940800656'.split()))
    r_cp = np.float32(np.asarray('0.2687231518330518 0.31846280807652494 0.36423550792806686 0.503436168306424'.split()))
    r_bn = np.float32(np.asarray('0.0019807927869329393 0.0028622029291350314 0.0035210829777147503 0.005099698081662132'.split()))
    r_dm = np.float32(np.asarray('0.043233439309139574 0.0457819696770163 0.04710373575173319 0.0492634693952825'.split()))
    r_gd = np.float32(np.asarray('0.07288259617026688 0.07699867624926922 0.07913343402097117 0.08262157633946775'.split()))
    r_rs = np.float32(np.asarray('0.10136153450402448 0.10704497540014286 0.10999262690111615 0.11480901781769662'.split()))
    r_ir = np.float32(np.asarray('0.22403459181578622 0.23550190876256766 0.24144930130665168 0.25116719618574657'.split()))
    r_lp = np.float32(np.asarray('0.06767660632708769 0.07107235386120928 0.07283351941194385 0.07571122112069459'.split()))

    R = [0 for i in range(14)]
    Index = ['Biome','Structures','Spawner','Chest','r_am','r_dm','r_gd','r_em','r_bn','r_cp','r_ir','r_cl','r_lp','r_rs']
    
    structures                  = 'mineshaft ruined_portal village ocean_ruin shipwreck buried_treasure fossil igloo pillager_outpost desert_pyramid swamp_hut jungle_pyramid mansion'.split()
    str_p = np.float32(np.asarray('0.89      0.26          0.25    0.235      0.2       0.135           0.115  0.025 0.01             0.01           0.005     0.005          0.005'.split()))

    biomes = 'river forest plains dripstone_caves beach lush_caves taiga stony_shore ocean savanna cold_ocean birch_forest old_growth_birch_forest lukewarm_ocean frozen_river snowy_plains meadow snowy_taiga frozen_ocean snowy_beach jungle deep_cold_ocean desert sparse_jungle dark_forest savanna_plateau deep_ocean old_growth_pine_taiga swamp old_growth_spruce_taiga windswept_hills warm_ocean badlands flower_forest grove deep_lukewarm_ocean sunflower_plains deep_frozen_ocean snowy_slopes bamboo_jungle windswept_savanna eroded_badlands wooded_badlands windswept_forest windswept_gravelly_hills stony_peaks ice_spikes frozen_peaks jagged_peaks'.split()
    bio_p = np.float32(np.asarray('0.865 0.675 0.6   0.51  0.46  0.435 0.27  0.25  0.23  0.22  0.21  0.21 0.205 0.185 0.17  0.17  0.16  0.13  0.125 0.12  0.115 0.09  0.09  0.09 0.09  0.08  0.075 0.075 0.07  0.07  0.065 0.065 0.06  0.06  0.055 0.055 0.055 0.05  0.05  0.04  0.035 0.035 0.035 0.03  0.025 0.025 0.025 0.02 0.015'.split()))

    d_stru = {}
    for i in range(len(structures)):
        d_stru[structures[i]] = str_p[i]
    
    d_bio = {}
    for i in range(len(biomes)):
        d_bio[biomes[i]] = bio_p[i]

    R[0] = []
    R[1] = []
    for b in summary[0]: #biomes
        try:
            p = d_bio[b]
            if 0.1 < p <= 0.25:
                R[0].append((b,1))
            elif 0.05 < p <= 0.1:
                R[0].append((b,2))
            elif 0.01 < p <= 0.05:
                R[0].append((b,3))
            elif p <= 0.01:
                R[0].append((b,4))
            else:pass
        except: #extremly rare
            R[0].append((b,5))
    for s in summary[5]: #structures
        try:
            p = d_stru[s]
            if 0.1 < p <= 0.25:
                R[1].append((s,1))
            elif 0.05 < p <= 0.1:
                R[1].append((s,2))
            elif 0.01 < p <= 0.05:
                R[1].append((s,3))
            elif p <= 0.01:
                R[1].append((s,4))
            else:pass
        except:
            R[1].append((s,5))
    data,ref,Ri = summary[3], r_sp, 2
    for p in ref:
        if p < data:
            R[Ri] += 1
    data,ref,Ri = summary[4], r_cs, 3
    for p in ref:
        if p < data:
            R[Ri] += 1
    p_ores = [r_am,r_dm,r_gd,r_em,r_bn,r_cp,r_ir,r_cl,r_lp,r_rs]
    for i in range(len(p_ores)):
        data,ref,Ri = summary[i+7], p_ores[i], i+4
        for p in ref:
            if p < data:
                R[Ri] += 1
    return Index,R