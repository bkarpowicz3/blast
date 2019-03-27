function [elbow_angleR, elbow_angleL, shoulder_angle] = computeMetrics(skeleton)

Hip_Center = 1;
Spine = 2;
Shoulder_Center = 3;
Head = 4;
Shoulder_Left = 5;
Elbow_Left = 6;
Wrist_Left = 7;
Hand_Left = 8;
Shoulder_Right = 9;
Elbow_Right = 10;
Wrist_Right = 11;
Hand_Right = 12;

shoulderL = skeleton(5,:);
shoulderR = skeleton(9,:);
elbowL = skeleton(6,:);
wristL = skeleton(7,:);
elbowR = skeleton(10,:);
wristR = skeleton(11,:);
y = abs(shoulderL(2) - shoulderR(2));  
x = abs(shoulderL(1) - shoulderR(1)); 
shoulder_angle = atand(y/x);

%left elbow angle calculation
%first find the hypotenus that shows the distance between the elbow and
%wrist
elb_wristLy = abs(elbowL(2) - wristL(2));
elb_wristLx = abs(elbowL(1) - wristL(1));
elb_wristLhyp = sqrt(elb_wristLy^2 + elb_wristLx^2);

%first find the hypotenus that shows the distance between the elbow and
%shoulder
elb_shoulderLy = abs(elbowL(2) - shoulderL(2));
elb_shoulderLx = abs(elbowL(1) - shoulderL(1));
elb_shoulderLhyp = sqrt(elb_shoulderLy^2 + elb_shoulderLx^2);

%first find the hypotenus that shows the distance between the wrist and
%shoulder
wrist_shoulderLy = abs(wristL(2) - shoulderL(2));
wrist_shoulderLx = abs(wristL(1) - shoulderL(1));
wrist_shoulderLhyp = sqrt(wrist_shoulderLy^2 + wrist_shoulderLx^2);

%find C i.e.the angle opposite elb-shoulder length
C = acosd((-elb_shoulderLhyp^2 + wrist_shoulderLhyp^2 + elb_wristLhyp^2)...
    /(2*elb_wristLhyp*wrist_shoulderLhyp));

%find angle alpha
alpha = 90-C;

%find the distance a-x and then the elbow angle
a_x = elb_wristLhyp*cosd(C);
xdist = wrist_shoulderLhyp - a_x;
beta = asind(xdist/elb_shoulderLhyp);
elbow_angleL = alpha+beta;
elbow_angleL = round(elbow_angleL,2,'significant');

%right elbow angle calculation
%first find the hypotenus that shows the distance between the elbow and
%wrist
elb_wristRy = abs(elbowR(2) - wristR(2));
elb_wristRx = abs(elbowR(1) - wristR(1));
elb_wristRhyp = sqrt(elb_wristRy^2 + elb_wristRx^2);

%first find the hypotenus that shows the distance between the elbow and
%shoulder
elb_shoulderRy = abs(elbowR(2) - shoulderR(2));
elb_shoulderRx = abs(elbowR(1) - shoulderR(1));
elb_shoulderRhyp = sqrt(elb_shoulderRy^2 + elb_shoulderRx^2);

%first find the hypotenus that shows the distance between the wrist and
%shoulder
wrist_shoulderRy = abs(wristR(2) - shoulderR(2));
wrist_shoulderRx = abs(wristR(1) - shoulderR(1));
wrist_shoulderRhyp = sqrt(wrist_shoulderRy^2 + wrist_shoulderRx^2);

%find CR i.e.the angle opposite elb-shoulder length
CR = acosd((-elb_shoulderRhyp^2 + wrist_shoulderRhyp^2 + elb_wristRhyp^2)...
    /(2*elb_wristRhyp*wrist_shoulderRhyp));

%find angle alphaR
alpha_R = 90-CR;

%find the distance a-x and then the elbow angle
a_xR = elb_wristRhyp*cosd(CR);
xdistR = wrist_shoulderRhyp - a_xR;
beta_R = asind(xdistR/elb_shoulderRhyp);
elbow_angleR = alpha_R+beta_R;
elbow_angleR = round(elbow_angleR,2,'significant');
end 
