// Atualiza o mapa baseando-se nas coordenadas atuais do robô e a leitura do PLS.
void AIRMap::atualizeGrid(int posX, int posY, float theta, TLaser rangeLaser, TLaser angLaser, int iteration, float releaseRate, int id)
{

    int i, xL, yL, deltaX, deltaY, sX, sY, erro, erro2;
    float taxaOC, tempRange, tempAng;


    for(i = LASERINIT; i < LASERFINAL; i++){

        if(rangeLaser[i] < RANGE_MAX*RANGE_LIMIT)
            taxaOC = 0.9;
        else {
            taxaOC = 0.48;
        }


      //Determinação dos pontos onde o laser bateu
      tempRange = rangeLaser[i];
      tempAng = angLaser[i];

      xL = cos(angLaser[i]+theta)*tempRange/RES + (posX);
      yL = sin(angLaser[i]+theta)*tempRange/RES + (posY);

      //ajuste das bordas do mapa
      if (xL < 0) xL = 0;
      if (xL > MAPWIDTH) xL = MAPWIDTH;
      if (yL < 0) yL = 0;
      if (yL > MAPHEIGHT) yL = MAPHEIGHT;

      //ajuste das bordas do mapa
      if (BndLeft > xL) BndLeft = xL;
      if (BndRight < xL) BndRight = xL;
      if (BndSup < yL) BndSup = yL;
      if (BndInf > yL) BndInf = yL;

      //ajuste das bordas do mapa
      if (BndLeft < 0) {BndLeft = 0; xL = 0;}
      if (BndRight > (MAPWIDTH)) {BndRight = (MAPWIDTH); xL = (MAPWIDTH);}
      if (BndSup > (MAPHEIGHT)) {BndSup = (MAPHEIGHT); yL = (MAPHEIGHT);}
      if (BndInf < 0) {BndInf = 0; yL = 0;}

      setMapGlobalBnd(xL,yL,BndLeft,BndRight,BndInf,BndSup);


      //Verificar por qual cĂ©lula o laser passa para setar probabilidade;
      //A reta comeca onde o laser "bateu" e termina no robĂŽ
      //Utilizando o algoritmo de Bresenham
      deltaX = abs(xL-posX);
      deltaY = abs(yL-posY);

      if(xL < posX) sX = 1; else sX = -1;
      if(yL < posY) sY = 1; else sY = -1;
      erro = deltaX - deltaY;

      while(1){
          //cálculo da probabilidade de ocupação
          setMapGlobalOG(xL,yL,1-pow((1+(taxaOC/(1-taxaOC))*((1-PRIORI)/PRIORI)*(getMapGlobalOG(xL,yL)/((1-getMapGlobalOG(xL,yL))+0.00001))),-1)+0.00001);

          setMapGlobalVs(xL,yL);//celula visitada

          if(taxaOC > 0.5){
              taxaOC = 0.48;
          }else{
              taxaOC = taxaOC*0.95;
          }

          if((xL == posX) && (yL == posY)){
            break;
          }

          erro2 = 2*erro;
          if(erro2 > -deltaY){
                erro = erro - deltaY;
                xL = xL + sX;
          }
          
	  if(erro2 < deltaX){
              erro = erro + deltaX;
              yL = yL + sY;
          }
      }
    }
