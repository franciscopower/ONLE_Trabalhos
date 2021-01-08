# Otimização não linear em Engenharia

## Maximização da Cobertura 5G num determinado espaço

O objetivo deste trabalho é descobrir, para uma certa área , qual é o menor numero de router possível, bem como as suas coordenadas no espaço de modo a oferecerem cobertura de internet em todo o espaço​

Terá que ser tido em consideração, que as ondas eletromagnéticas sofrem reflexão e são bloqueados por obstruções no espaço e que o alcance também e limitado por cada router.

### Programas usados para análise

- **raytracer.py** (desenvolvido por nós para o efeito) - Sendo fornecido um mapa de obstáculos como imagem a níveis de cinzento, em que o preto é a área livre e branco são as obstruções, e fornecendo a potencia das torres e as suas posições, calcula a matriz de intensidade de sinal em cada ponto.
  - ray_tracer_interactive.py - Versão interativa do ray_tracer, permite mover a posição de duas torres usando o rato.
- **InternetObjRestr.py** - Calcula o valor da função objetivo e verifica o cumprimento ou não das restrições impostas. Exporta os resultados para ficheiros .csv.

***

## Minimização do tempo de curso em vazio na impressão 3D FFF de múltiplas peças

O objetivo deste trabalho é desenvolver um programa para minimizar o tempo de impressão, que, conhecendo o formato das peças a imprimir e as dimensões da cama quente consiga dispor as peças na cama quente de forma ótima e automática, de modo a que o percurso em vazio da extrusora seja o menor possível. ​

O programa terá que ter em consideração o percurso da extrusora em todas as camadas da impressão e não apenas a forma da base.​

### Programas usados para análise

- **Ultimaker Cura** - Programa de preparação de impressões 3D da Ultimaker, permite a criação do g-code de cada peça
  - https://github.com/Ultimaker/Cura
- **interpretGCode.py** - Cria uma lista com os pontos de interesse extraídos dos ficheiros G-Code presentes numa determinada pasta.
  - A lista criada contém uma lista para cada objeto, lista essa que contém 3 matrizes, uma com os pontos todos do objeto, uma com os pontos de chegada do extrusor ao objeto e uma com os pontos de saída do extrusor do objeto.
- **moveObjects.py** - Permite a aplicação de operaçes de translaço e rotação aos pontos da peça a partir dos pontos obtidos pelo programa *interpretGCode.py*
- **ImpressaoObjRestr.py** - Calcula o valor da função objetivo e verifica o cumprimento ou não das restrições. Exporta os resultados para ficheiros .csv.
 ***
 
 ## Bibliotecas necessárias:
 
 ```bash
 pip install numpy
 pip install matplotlib
 pip install opencv-python
 pip install pandas
pip install Shapely
```
***

Trabalhos realizados por

- Francisco Power
- Pedro Rolo

No âmbito da disciplina de Otimização Não Linear em Engenharia, Mestrado Integrado em Engenharia Mecânica, Universidade de Aveiro.
