This project will focus on the integration of Lane detection and Lane-Keeping systems using
different computer vision and deep learning approaches for lane detection and different motor
controlling techniques and algorithms for the lane-keeping system.
- Our system comprises several key components: a camera, a multi-processing unit, a motor driver, and two motors. 
 * Here's how it works:
- The Raspberry Pi Camera captures raw frames of the road.
- These frames are processed by a lane detection algorithm within the multi-processing unit to determine the lane's curve value.
- The curve value is used by the angle calculation module to compute the necessary steering angle.
- The DC Motors ( 12v ) control algorithm receives the steering angle and generates two Pulse Width Modulation (PWM) signals to control the motor driver.
- The L298 Dual H-Bridge Motor Driver adjusts the voltage supplied to Motor 1 and Motor 2, ensuring the vehicle stays within the detected lane.
- ![image](https://github.com/malekzitouni/projectPPP/assets/112777865/115369e7-b309-457f-957e-c681a15b439c)
![image](https://github.com/malekzitouni/projectPPP/assets/112777865/617a7313-8da6-40ec-a48c-d6c99d7c62af)
![image](https://github.com/malekzitouni/projectPPP/assets/112777865/cf18a53b-c49a-47f4-a74d-1151775842bb)

