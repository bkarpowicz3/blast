function [] = skeletonViewer(skeleton, image, nSkeleton)

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
Hip_Left = 13;
Knee_Left = 14;
Ankle_Left = 15;
Foot_Left = 16;
Hip_Right = 17;
Knee_Right = 18;
Ankle_Right = 19;
Foot_Right = 20;

% imshow(image);

SkeletonConnectionMap = [[1 2]; % Spine
                         [2 3];
                         [3 4];
                         [3 5]; %Left Hand
                         [5 6];
                         [6 7];
                         [7 8];
                         [3 9]; %Right Hand
                         [9 10];
                         [10 11];
                         [11 12]];
%                          [1 17]; % Right Leg
%                          [17 18];
%                          [18 19];
%                          [19 20];
%                          [1 13]; % Left Leg
%                          [13 14];
%                          [14 15];
%                          [15 16]];
                     
for i = 1:size(SkeletonConnectionMap, 1)
     
     if nSkeleton > 0
         X1 = [skeleton(SkeletonConnectionMap(i,1),1,1) skeleton(SkeletonConnectionMap(i,2),1,1)];
         Y1 = [skeleton(SkeletonConnectionMap(i,1),2,1) skeleton(SkeletonConnectionMap(i,2),2,1)];
         line(X1,Y1, 'LineWidth', 1.5, 'LineStyle', '-', 'Marker', '+', 'Color', 'r');
     end
%      if nSkeleton > 1
%          X2 = [skeleton(SkeletonConnectionMap(i,1),1,2) skeleton(SkeletonConnectionMap(i,2),1,2)];
%          Y2 = [skeleton(SkeletonConnectionMap(i,1),2,2) skeleton(SkeletonConnectionMap(i,2),2,2)];     
%          line(X2,Y2, 'LineWidth', 1.5, 'LineStyle', '-', 'Marker', '+', 'Color', 'g');
%      end
    hold on;
 end
 hold off;
 
 [elbow_angleR, elbow_angleL, shoulder_angle] = computeMetrics(skeleton);
 text(10,20, ['Shoulder Angle: ' num2str(shoulder_angle) ' degrees'], 'Color', 'red', 'FontSize', 16);
 text(10,60, ['Left Elbow Angle: ' num2str(elbow_angleL) ' degrees'], 'Color', 'green', 'FontSize', 16);
 text(10,110, ['Right Elbow Angle: ' num2str(elbow_angleR) ' degrees'], 'Color', 'blue', 'FontSize', 16);
