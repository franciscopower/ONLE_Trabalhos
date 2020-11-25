import numpy as np
import interpretGCode

def objFunction(objs):
    n_layers = [o[1].shape[1] for o in objs] #numero de camadas de cada objeto
    
    total_obj_idx = range(0, len(objs))
    obj_n = 0 #primeiro objeto a testar
    d_min = 200 #distancia para comparacao
    d_total = 0
    #percorrer cada camada
    for l in range(0, max(n_layers)):
        obj_idx = total_obj_idx[:]
    
        n_valid_objs = len(total_obj_idx)
        
        #comecar no primeiro objeto, ir de objeto em objeto
        while True: 
            if n_valid_objs == 1:
                break
            n_valid_objs -= 1
            obj_idx.pop(obj_idx.index(obj_n))
            if not obj_idx:
                continue
            
            #get out position of current object
            try:
                out = objs[obj_n][2][:,l]
            except:
                out = objs[obj_n][2][:,l-1]   
                
            for i in obj_idx:
                #check if object has current layer
                if objs[i][1].shape[1] == l:
                    try:
                        total_obj_idx.pop(total_obj_idx.index(i))
                    except:
                        pass
                    else:
                        n_valid_objs -= 1
                    continue
                
                #get in position of next object
                inn = objs[i][1][:,l]
                #calculate distance
                d = np.sqrt((out[0]-inn[0])**2 + (out[1]-inn[1])**2)
                
                #check if distance is smaller that with the previous object
                if d <= d_min:
                    d_min = d
                    obj_n_temp = i
            
            #update current object and total distance
            obj_n = obj_n_temp
            d_total += d_min
            # print(l, d_min)
            #reset minimum distance
            d_min = 200
       
    return d_total

def restriction(objs, d_min):
    
    point_interval = 3
    
    n_layers = [o[1].shape[1] for o in objs] #numero de camadas de cada objeto

    for l in range(0, max(n_layers)): #[o1 o2 o3 o4 o5]
        for i,ob in enumerate(objs):
            if i == len(objs)-1 or l>=ob[1].shape[1]:
                break
            
            for n in range(i+1, len(objs)):
                for p1_i in range(0,ob[0].shape[1],point_interval):
                    p1 = ob[0][:,p1_i]
                    
                    for p2_i in range(0,objs[n][0].shape[1], point_interval):
                        if l>=objs[n][1].shape[1]:
                            break
                        
                        p2 = objs[n][0][:,p2_i]
                        
                        d = np.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)
                        if d <= d_min:
                            return False
                        
    return True

def checkInHotBed(objs, hot_bed_size_x, hot_bed_size_y):
    for o in objs:
        x_max = max(o[0][0,:])
        x_min = min(o[0][0,:])
        y_max = max(o[0][1,:])
        y_min = min(o[0][1,:])
        
        if x_max > hot_bed_size_x/2 or x_min < -hot_bed_size_x/2 or y_max > hot_bed_size_y/2 or y_min < -hot_bed_size_y/2:
            print(x_max, x_min, y_max, y_min)
            return False
            
    return True


def main():
    objs = interpretGCode.getObjectsPts('Impressao3D/GCode/')
    print(objFunction(objs))
    print(restriction(objs, 3))
    print(checkInHotBed(objs, 200, 200))
    

if __name__ == "__main__":
    main()
    
    
    
    