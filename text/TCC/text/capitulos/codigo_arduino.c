  
  //###############################################################
  //Codigo do regulador de temperaturas para chuveiros elétricos
  //#############################################################
 #include <TimerOne.h>
 
//DECLARAcaO DE VARIÁVEIS*****************************************
float delta;
float temp_estimada = 0;
float tempo;
float temp_medida = 0;
float temp_desejada = 30 ;
float erro = 0;
float erro_a = 0;
float d;
float tempo_delay = 0;
float temp_ambiente;
float temp_medida_z;
float temp_desejada_z;
float tempo_botao;
boolean controlado = false;
int potencia;
int decimal;
int numeral;
int tensao_retificada;
int i;
int mux1 = 18;
int mux2 = 19;
int flag;
int flag_botao;
byte digitos_display[10][7] = {
    { 1, 1, 1, 1, 1, 1, 0} // = 0
    ,
    { 0, 1, 1, 0, 0, 0, 0} // = 1
    ,
    { 1, 1, 0, 1, 1, 0, 1} // = 2
    ,
    { 1, 1, 1, 1, 0, 0, 1} // = 3
    ,
    { 0, 1, 1, 0, 0, 1, 1} // = 4
    ,
    { 1, 0, 1, 1, 0, 1, 1} // = 5
    ,
    { 1, 0, 1, 1, 1, 1, 1} // = 6
    ,
    { 1, 1, 1, 0, 0, 0, 0} // = 7
    ,
    { 1, 1, 1, 1, 1, 1, 1} // = 8
    ,
    { 1, 1, 1, 1, 0, 1, 1} // = 9
};

//FIM*******************************************************************

//PRIMEIRA FUNcaO A SER EXECUTADA PELO MICROCONTROLADOR*******************
void setup() {
     Serial.begin(9600);
    analogReference(INTERNAL);              
    pinMode(2, OUTPUT); //Pulso para o optoacoplador
    pinMode(11, OUTPUT);//Display
    pinMode(12, OUTPUT);//Display
    pinMode(13, OUTPUT);//Display
    pinMode(14, OUTPUT);//Display
    pinMode(15, OUTPUT);//Display
    pinMode(16, OUTPUT);//Display
    pinMode(17, OUTPUT);//Display
    pinMode(18, OUTPUT);//mux1
    pinMode(19, OUTPUT);//mux2
    pinMode(A0, INPUT); //Entrada da tensao retificada            
    pinMode(A1, INPUT); //entrada da temperatura do sensor
    pinMode(A2, INPUT); //entrada do botao de +/- temperatura   
    Timer1.attachInterrupt(aciona);//interrupcao de tempo para pulso do optoacoplador
    delay(2000);                    
    
    leitura();
    temp_ambiente = temp_medida;
    d = (temp_desejada - temp_ambiente)/28;
    tempo_delay = 1-d;
    tempo = 2000;  
}

//FIM******************************************************************

//*****************FUNCAO PARA PULSO NO OPTOACOPLADOR**************
void aciona(){

    digitalWrite(2,HIGH);
    
    if (tempo_delay < 0.1){
	delayMicroseconds(1000);
    } 
    else
        delayMicroseconds(100);
    
    digitalWrite(2,LOW);
    Timer1.stop(); 

}

//FIM************************************************************************

//FUNCAO DE LEITURA DA TEMPERATURA*****************************************
void leitura(){
     temp_medida=analogRead(A1) * 1.10 / 1024*100; 
     for (i=0;i<20;i++)
         temp_medida = temp_medida *0.9 + (analogRead(A1)* 1.10 / 1024*100) *0.1;
}
//FIM************************************************************************//

//FUNCAO QUE VERIFICA BOTOES***********************************************************//

void verifica_botao(){
    
    if (analogRead(A2) < 2) 
	flag_botao = true;
    
    else{
      if(flag_botao == true){
        if(analogRead(A2) < 819){ 
          temp_desejada = temp_desejada + 1;
          flag_botao = false;
          tempo_botao = millis();
        }
        else{ 
          temp_desejada = temp_desejada - 1;
          flag_botao = false;
          tempo_botao = millis();
         
        }
      }
    }
}
//FIM**********************************************************************************//

//FUNCAO DE ESCRITA DO DISPLAY**********************************************************//
void escreve_display() {
  
  if (millis() - tempo_botao < 5000){
  
      decimal = temp_desejada/10;  
      numeral = temp_desejada -(decimal*10);
  }
  else{
      potencia = d*99;
      decimal = potencia/10;
      numeral = potencia - (decimal*10);
  }
   
      if (flag == 1) //primeiro display
      {
        digitalWrite(mux2, LOW);

        for (byte segCount = 0; segCount < 7; ++segCount) 
        {
            digitalWrite(segCount + 11, digitos_display[decimal][segCount]);
        }
        digitalWrite(mux1, HIGH);
        flag = 2;
      }
      
      else 
      { // segundo display
        digitalWrite(mux1, LOW);
        for (byte segCount = 0; segCount < 7; ++segCount) 
        {
            digitalWrite(segCount + 11, digitos_display[numeral][segCount]);
        }
        digitalWrite(mux2, HIGH);
        flag = 1;
      }  
}

//FIM*************************************************************************

//FUNCAO QUE CALCULA LEI DE CONTROLE*********************************************
  
void controle(){
  
  if (millis() > tempo)// 
  {
   leitura();
   temp_medida_z = temp_medida - temp_ambiente;
   temp_desejada_z = temp_desejada - temp_ambiente;
   erro_a = erro;
 
   temp_estimada = temp_medida_z*0.9613 + 1.103*d;
   erro = temp_desejada_z - temp_estimada;     
   d =  0.143*erro - 0.1374*erro_a + d;
   
    if (d > 1) d = 1;
    if (d < 0) d = 0;
    
    tempo = tempo + 1000;
    tempo_delay = 1 - d;
 
   //Serial.print(temp_medida);
  // Serial.print(" , ");
  // Serial.println(millis()/1000);
   //Serial.print("temp_estimada =  ");
  // Serial.println(temp_estimada+temp_ambiente);
   
  }
}

//FIM*****************************************************************

//FUNcaO PRINCIPAL*******************************************
void loop() {
   
    tensao_retificada = analogRead(A0); 
    if ((tensao_retificada < 2) && !controlado){ 
        
        
        if (tempo_delay==0) 
          aciona();
        else {
          if (tempo_delay<1)  
            Timer1.initialize(tempo_delay * 8333 * 0.88);
        }

       controlado=true;
       escreve_display();
       verifica_botao();
       controle();                  
    } 
	else{ // histerese
          if (tensao_retificada > 10) 
            controlado = false;
        }
}
//FIM*******************************************************************