%ESE Senior Design Team 11
%MPU6050 Percent Error Code
%Objective: In importing the values from the MPU6050, calcualte the measure
%error to the 'theortical' (protractor) value

format long

filename = 'Data.txt'; %insert filename
delimiterIn = '\t'; %determine what delimiter will be based on textfile
headerLinesIn = 1; %Number of text header lines in ASCII file

A = importdata(filename, delimiterIn, headerLinesIn);
[m,n] = size(A.data);
%disp(A.data);

error = zeros(m,1); %initialize error array

measAngle = 25; %angle from protractor

for i = 1:m
   quaternion = A.data(i,:);
   eulZYX = quat2eul(quaternion, 'ZYX');
   
   %Reverse order of eulZYX to output XYZ. Convert from radians to degrees
   eulXYZ = (180/pi)*fliplr(eulZYX); 
   
   %disp(eulXYZ);
   %change eul(int) depending on direction being measured
   error(i,1) = 100*(abs(eulXYZ(1)-measAngle))./measAngle;
end 

errorAvg = sum(error)/m;
