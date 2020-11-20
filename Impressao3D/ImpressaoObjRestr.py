import numpy as np
import interpretGCode

def objFunction(objs):
    n_layers = [o[1].shape[1] for o in objs] #numero de camadas de cada objeto
    
    
    obj_n = 0 #primeiro objeto a testar
    tested_objs = [obj_n] #indice dos objetos que ja foram testados
    #percorrer cada camada
    for l in range(0, max(n_layers)):
        
        #comecar no primeiro objeto, ir de objeto em objeto
        for _ in range(0,len(objs)): 
            try:
                out = objs[obj_n][2][:,l]
                for n,o in enumerate(objs):
                    
                    if n in tested_objs:
                        continue
                    
                    inn = o[1][:,l]
                    #TODO calcular a distancia entre out e inn
                    
                #TODO encontrar indice da distancia minima
                #TODO guardar como obj_n
                tested_objs.append(obj_n)
                    
            except:
                pass

def restriction():
    pass

def main():
    objs = interpretGCode.getObjectsPts('Impressao3D/GCode/')
    

if __name__ == "__main__":
    main()