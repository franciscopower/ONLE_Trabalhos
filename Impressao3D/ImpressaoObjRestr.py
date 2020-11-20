import numpy as np
import interpretGCode

def objFunction(objs):
    n_layers = [o[1].shape[1] for o in objs] #numero de camadas de cada objeto
    
    obj_n = 0 #primeiro objeto a testar
    tested_objs = [obj_n] #indice dos objetos que ja foram testados
    d_min = 200 #distancia para comparacao
    d_total = 0
    #percorrer cada camada
    for l in range(0, max(n_layers)):
        #comecar no primeiro objeto, ir de objeto em objeto
        for _ in range(0,len(objs)): 
            try:
                out = objs[obj_n][2][:,l]
            except:
                out = objs[obj_n][2][:,l-1]   
                
            for n,o in enumerate(objs):
                
                if n in tested_objs:
                    continue
                
                try:
                    inn = o[1][:,l]
                except:
                    continue
                else:
                    d = np.sqrt((out[0]-inn[0])**2 + (out[1]-inn[1])**2)
                    
                    if d <= d_min:
                        d_min = d
                        obj_n = n
            
            d_total += d_min

            tested_objs.append(obj_n)
                
        obj_n = tested_objs[-1]    
        tested_objs = [obj_n]  
          
    return d_total

def restriction():
    pass

def main():
    objs = interpretGCode.getObjectsPts('Impressao3D/GCode/')
    print(objFunction(objs))
    

if __name__ == "__main__":
    main()