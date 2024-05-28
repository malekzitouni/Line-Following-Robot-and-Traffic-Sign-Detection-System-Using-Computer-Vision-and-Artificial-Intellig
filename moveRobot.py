void move_distance(float distance,float speed)
{
	init();
	//Set accel/decel distance
	if (fabs(distance) < (speed*speed/ramp))
	{
		accel_dist = fabs(distance)/2;
		decel_dist = fabs(distance)/2;
		speed = sqrt (2*ramp*accel_dist);
	}
	else
	{
		accel_dist = (float)0.5*speed*speed/ramp;
		decel_dist = (float)0.5*speed*speed/ramp;
	}
	while(fabs((total_right+total_left)/2-distance)>1 && evitementFlag)
	{

//			loop();
//			HAL_Delay(5);
		nh.spinOnce();

		t0=t;
		//Accel/Decel Speed Set
		if (((total_right+total_left)/2 -distance)<0)
			sens = 1;
		else
			sens = -1;
		if (fabs((total_right+total_left)/2) < accel_dist)
			speed_ref = sens*50+sens*(constrain(sqrt (ramp*fabs(total_right+total_left))-50,0,1000));

		else if (fabs((total_right+total_left)/2 -distance) < decel_dist)
			speed_ref = sens*10+sens*constrain((sqrt(2*ramp*fabs((total_right+total_left)/2 -distance))-10),0,1000);//fabs((total_right+total_left)/2 -distance)
		else
			speed_ref = sens*speed;
		//Right wheel regulation
		right_error = speed_ref - right_speed;
		i_right_error += right_error;
		PWM_RB = kp * right_error + ki * i_right_error;
		if (PWM_RB>PWM_Max) PWM_RB = PWM_Max;
		if (PWM_RB<-PWM_Max) PWM_RB = -PWM_Max;
		//Left wheel regulation
		left_error = speed_ref - left_speed;
		i_left_error += left_error;
		PWM_LB = kp * left_error + ki * i_left_error;
		if (PWM_LB>PWM_Max) PWM_LB = PWM_Max;
		if (PWM_LB<-PWM_Max) PWM_LB = -PWM_Max;
		//Orientation Correction²
		left_correction = coef_correct_dist * (total_right-total_left);
		right_correction = - left_correction;
		PWM_R = PWM_RB + right_correction;
		PWM_L = PWM_LB + left_correction;
		//Execution
		run_motors();
		do delta=t-t0;
		while (delta<T);
	}

	stop_motors();
}