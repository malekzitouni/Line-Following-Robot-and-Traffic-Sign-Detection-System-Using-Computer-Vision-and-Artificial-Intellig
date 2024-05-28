// Définition
des
broches
des
capteurs
infrarouges

const
int
sensorPin1 = A0;
const
int
sensorPin2 = A1;
const
int
sensorPin3 = A2;
const
int
sensorPin4 = A3;
const
int
sensorPin5 = A4;
int
vitesse = 255;
float
coef = 0.9;
// Variables
pour
stocker
les
lectures
des
capteurs

int
sensorValue1 = 0;
int
sensorValue2 = 0;
int
sensorValue3 = 0;
int
sensorValue4 = 0;
int
sensorValue5 = 0;
int
c = 0;

// Définition
des
broches
des
moteurs

const
int
leftMotor1 = 5;
const
int
leftMotor2 = 6;
const
int
rightMotor1 = 9;
const
int
rightMotor2 = 10;

// other
definitions
int
time = 0;
int
s;
int
chef = 1;
float
seuil[5];
int
sensorValues[5];
int
sensorPin[5] = {A0, A1, A2, A3, A4};
int
s1;
int
condition_arret;
int
condition_erreur;
int
condition_gap;
int
ds;
float
black[5];
float
white[5];

void
forward()
{
    analogWrite(rightMotor1, vitesse * coef);
analogWrite(rightMotor2, 0);
analogWrite(leftMotor1, vitesse);
analogWrite(leftMotor2, 0);

}
void
forward2()
{
    analogWrite(rightMotor1, vitesse * coef / 2);
analogWrite(rightMotor2, 0);
analogWrite(leftMotor1, vitesse / 2);
analogWrite(leftMotor2, 0);

}
void
backwards()
{
    analogWrite(rightMotor1, 0);
analogWrite(rightMotor2, 255);
analogWrite(leftMotor1, 0);
analogWrite(leftMotor2, 255);

}

void
left()
{
    analogWrite(rightMotor1, 0);
analogWrite(rightMotor2, 0);
analogWrite(leftMotor1, 255);
analogWrite(leftMotor2, 0);

}
void
right()
{
    analogWrite(rightMotor1, 255);
analogWrite(rightMotor2, 0);
analogWrite(leftMotor1, 0);
analogWrite(leftMotor2, 0);

}

void
left2()
{
    analogWrite(rightMotor1, 0);
analogWrite(rightMotor2, 70);
analogWrite(leftMotor1, 70);
analogWrite(leftMotor2, 0);

}
void
right2()
{
    analogWrite(rightMotor1, 70);
analogWrite(rightMotor2, 0);
analogWrite(leftMotor1, 0);
analogWrite(leftMotor2, 70);

}

void
stopp()
{
    analogWrite(rightMotor1, 0);
analogWrite(rightMotor2, 0);
analogWrite(leftMotor1, 0);
analogWrite(leftMotor2, 0);

}

void
smoothleft()
{
    analogWrite(rightMotor1, 0);
analogWrite(rightMotor2, 0);
analogWrite(leftMotor1, 255);
analogWrite(leftMotor2, 0);
}

void
smoothright()
{
    analogWrite(rightMotor1, 255);
analogWrite(rightMotor2, 0);
analogWrite(leftMotor1, 0);
analogWrite(leftMotor2, 0);
}
void
readSensors()
{
for (int i=0;i < 5;i++){
    sensorValues[i]=analogRead(sensorPin[i]);
}
}

void
s_counter()
{
    s = 0;
/ *
for (int i=0;i < 5;i++)
{
if (sensorValues[i] > seuil[i])
{
    s = s + pow(10, i);
}
}
* /

if (sensorValues[0] > seuil[0]){
s += 1;
} if (sensorValues[1] > seuil[1]){
s += 10;
} if (sensorValues[2] > seuil[2]){
s += 100;
} if (sensorValues[3] > seuil[3]){
s += 1000;
} if (sensorValues[4] > seuil[4]){
s += 10000;
}
return s;
}


void
calibre()
{
for (int i=0;i < 6;i++){

    digitalWrite(13, HIGH);
delay(50);
digitalWrite(13, LOW);
delay(50);

}

Serial.println("beginnnn");

int
iter = 10000;
int
x = millis();
int
b = 0;
while ((millis() - x) < 2000){
readSensors();
for (int j=0;j < 5;j++){
black[j] += sensorValues[j];
}
b++;
}
// for (int i=0;i < iter;i++){

                             // readSensors();
// for (int j=0;j < 5;j++){
// black[j] += sensorValues[j];
//}
//}

for (int j=0;j < 5;j++){
    black[j]= black[j] / b;
}

digitalWrite(13, HIGH);
delay(4000);
digitalWrite(13, LOW);

int
y = millis();
int
w = 0;
while ((millis() - y) < 2000){
w++;
readSensors();
for (int j=0;j < 5;j++){
white[j] += sensorValues[j];
}
}

for (int j=0;j < 5;j++){
    white[j]/= w;}

for (int i=0;i < 5;i++){
    seuil[i]=(black[i]+white[i]) / 2;
}

for (int i=0;i < 6;i++){

    digitalWrite(13, HIGH);
delay(50);
digitalWrite(13, LOW);
delay(50);

}

Serial.println("Seuil ---------------------");
for (int j=0;j < 5;j++){
    Serial.print(seuil[j]);
Serial.print("   ");
}
Serial.println("-------------------------");

}



void
setup()
{

pinMode(sensorPin1, INPUT);
pinMode(sensorPin2, INPUT);
pinMode(sensorPin3, INPUT);
pinMode(sensorPin4, INPUT);
pinMode(sensorPin5, INPUT);
pinMode(rightMotor1, OUTPUT);
pinMode(rightMotor2, OUTPUT);
pinMode(leftMotor1, OUTPUT);
pinMode(leftMotor2, OUTPUT);
pinMode(13, OUTPUT);
ds = 0;
Serial.begin(9600);
s = 0;
s1 = 0;
condition_arret = 0;
condition_erreur = 0;
// put
your
setup
code
here, to
run
once:
calibre();

}
void
loop()
{

condition_gap = 0;
if (s != 0){
ds=s;
}
s = 0;
// putv
your
main
code
here, to
run
repeatedly:
/ *
sensorValue1 = analogRead(sensorPin1);
sensorValue2 = analogRead(sensorPin2);
sensorValue3 = analogRead(sensorPin3);
sensorValue4 = analogRead(sensorPin4);
sensorValue5 = analogRead(sensorPin5); * /

readSensors();
s_counter();
// Serial.println(s);

if (s == 100 | | s == 1110 | | s == 10101){
forward();
}
if (s == 1100 | | s == 11100 | | s == 11110 | | s == 10000 | | s == 1000){
if (s == 1100) {smoothright ();} else {right();
}
}
if (s == 11 | | s == 111 | | s == 1111 | | s == 110 | | s == 10 | | s == 11011 | | s == 11111){
if (s == 110) {smoothleft ();} else {left();
}
}

if (s == 0){if (ds == 10000){right();}
else {if (ds == 1){left();}}}
Serial.println(millis());

while (millis() > 27500){
if (millis() < 37500
){

readSensors();
s=0;
s_counter();

if (s % 10 == 1){
// if ( chef != 1 ){
// c=c+1;
// stopp();
// delay(1000);
//}


chef=1;
}

if (s / 10000 == 1 ){

chef=2;
}

if (s == 100 | | s == 1110){
forward2();
}

if ( s == 1000 | | s == 1001  ){
right2();
}
if (s == 0 & & chef == 1){
left2();
}
if (s == 0 & & chef == 2){
right2();

}
if (s == 0 & & !chef){
right2();
}

if ( s == 10 ){
left2();

}}
else {
condition_gap=0;
if (s != 0){
ds=s;
}
s=0;
// putv your main code here, to run repeatedly:
    /
    * \
    sensorValue1 = analogRead(sensorPin1);
sensorValue2 = analogRead(sensorPin2);
sensorValue3 = analogRead(sensorPin3);
sensorValue4 = analogRead(sensorPin4);
sensorValue5 = analogRead(sensorPin5); * /

readSensors();
s_counter();
// Serial.println(s);

if (s == 100 | | s == 1110 | | s == 10101)
{
    forward();
}
if (s == 0){
forward2();}
if (s == 1100 | | s == 11100 | | s == 11110 | | s == 10000 | | s == 1000 ){
if (s == 1100) {smoothright ();} else {right();
}
}
if ( s == 11 | | s == 111 | | s == 1111 | | s == 110 | | s == 10 | | s == 11011 | | s == 11111){
if (s == 110) {smoothleft ();} else {left();
}
}

// putv your main code here, to run repeatedly:
    /
    * \
    sensorValue1 = analogRead(sensorPin1);
sensorValue2 = analogRead(sensorPin2);
sensorValue3 = analogRead(sensorPin3);
sensorValue4 = analogRead(sensorPin4);
sensorValue5 = analogRead(sensorPin5); * /

/ * if (s == 11111)
{
    condition_arret += 1;
} else {condition_arret = 0;}
if (condition_arret >= 150){
stopp();

}
* /}}
}