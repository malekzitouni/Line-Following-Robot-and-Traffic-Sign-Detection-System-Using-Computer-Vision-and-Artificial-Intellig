


class Motor():
    def __init__(self,EnaA,In1A,In2A,EnaB,In1B,In2B):
        self.EnaA= EnaA
        self.In1A = In1A
        self.In2A = In2A
        self.EnaB= EnaB
        self.In1B = In1B
        self.In2B = In2B
        GPIO.setup(self.EnaA,GPIO.OUT);GPIO.setup(self.In1A,GPIO.OUT);GPIO.setup(self.In2A,GPIO.OUT)
        GPIO.setup(self.EnaB,GPIO.OUT);GPIO.setup(self.In1B,GPIO.OUT);GPIO.setup(self.In2B,GPIO.OUT)
        self.pwmA = GPIO.PWM(self.EnaA, 100);
        self.pwmB = GPIO.PWM(self.EnaB, 100);
        self.pwmA.start(0);
        self.pwmB.start(0);
        self.mySpeed=0

    def move(self,speed=0.5,turn=0,t=0):
        ki=;
        kp=;
        kd=;
        i_right_error = 0;
        i_left_error = 0;
        speed *=100
        turn *=70
        leftSpeed = speed-turn
        rightSpeed = speed+turn

        #if leftSpeed>100: leftSpeed =100
        #elif leftSpeed<-100: leftSpeed = -100
        #if rightSpeed>100: rightSpeed =100
        #elif rightSpeed<-100: rightSpeed = -100
        #PID :
        right_error=turn
        left_error=turn
        #//Right wheel regulation

		i_right_error += right_error;
		rightspeed= kp * right_error + ki * i_right_error;
		if (right_speed>speed_max) rightspeed = speed_max;
		if (right_speed<-speed_max) rightspeed = -speed_max;
		#//Left wheel regulation

		#i_left_error += left_error;
		#leftspeed = kp * left_error + ki * i_left_error;
		#if (leftspeed>speed_max) leftspeed = speed_max;
		#if (leftspeed<-speed_max) leftspeed = -speed_max;
        #print(leftSpeed,rightSpeed)
        self.pwmA.ChangeDutyCycle(abs(leftSpeed))
        self.pwmB.ChangeDutyCycle(abs(rightSpeed))
        if leftSpeed>0:GPIO.output(self.In1A,GPIO.HIGH);GPIO.output(self.In2A,GPIO.LOW)
        else:GPIO.output(self.In1A,GPIO.LOW);GPIO.output(self.In2A,GPIO.HIGH)
        if rightSpeed>0:GPIO.output(self.In1B,GPIO.HIGH);GPIO.output(self.In2B,GPIO.LOW)
        else:GPIO.output(self.In1B,GPIO.LOW);GPIO.output(self.In2B,GPIO.HIGH)
        sleep(t)
    def stop(self,t=0):
        self.pwmA.ChangeDutyCycle(0);
        self.pwmB.ChangeDutyCycle(0);
        self.mySpeed=0
        sleep(t)

def main():
    motor.move(0.5,0,2)
    motor.stop(2)
    motor.move(-0.5,0,2)
    motor.stop(2)
    motor.move(0,0.5,2)
    motor.stop(2)
    motor.move(0,-0.5,2)
    motor.stop(2)

if __name__ == '__main__':
    motor= Motor(2,3,4,17,22,27)
    main()
