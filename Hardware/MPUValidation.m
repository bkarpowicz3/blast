%ESE Senior Design Team 11
%MPU6050 Percent Error Code
%Objective: In importing the values from the MPU6050, calcualte the measure
%error to the 'theortical' (protractor) value

format long

filename = 'DummyData.txt'; %insert filename
delimiterIn = '\t'; %determine what delimiter will be based on textfile
headerLinesIn = 1; %Number of text header lines in ASCII file

A = importdata(filename, delimiterIn, headerLinesIn);
[m,n] = size(A.data);
%disp(A.data);

errorXAxis = zeros(m,1); %initialize error array
errorYAxis = zeros(m,1); %initialize error array
errorZAxis = zeros(m,1); %initialize error array
errorZAxisAct = zeros(m,1);

%Angle from protractor
%Should only vary one axis at a time
measuredX = 0; 
measuredY = 0;
measuredZ = 10; 

for i = 1:m
   quaternion = A.data(i,:);
   eulZYX = quat2eul(quaternion, 'ZYX');
   
   %Reverse order of eulZYX to output XYZ. Convert from radians to degrees
   eulXYZ = (180/pi)*fliplr(eulZYX); 
   
   %disp(eulXYZ);
   
   %Calculate error of other axis
   errorXAxis(i,1) = (abs(eulXYZ(1)-measuredX));
   
   errorYAxis(i,1) = (abs(eulXYZ(2)-measuredY));
   
   errorZAxis(i,1) = 100*(abs(eulXYZ(3)-measuredZ))./(measuredZ);
   %disp(errorZAxis(i,1))
end 

errorXAxisAvg = sum(errorXAxis)/m;
errorYAxisAvg = sum(errorYAxis)/m;
errorZAxisAvg = sum(errorZAxis)/m;
disp(errorZAxisAvg);