clc; clear all; close all;
imaqreset;

v = VideoWriter('presentation_video.mp4');
v.Quality = 95;
open(v);

colorVid = videoinput('kinect', 1);
depthVid = videoinput('kinect', 2);

triggerconfig(depthVid, 'manual');
triggerconfig(colorVid, 'manual');

colorVid.FramesPerTrigger = 1;
depthVid.FramesPerTrigger = 1;
colorVid.TriggerRepeat = inf;
depthVid.TriggerRepeat = inf;

% set(getselectedsource(depthVid), 'TrackingMode', 'Skeleton');
depthSrc = getselectedsource(depthVid);
depthSrc.TrackingMode = 'Skeleton';
viewer = vision.DeployableVideoPlayer();

start(colorVid);
start(depthVid);
himg = figure;

while ishandle(himg)
    trigger(colorVid);
    trigger(depthVid);
    [frameDataColor, colorTimeData, colorMetaData] = getdata(colorVid);
    [DepthMap, ~, depthMetaData] = getdata(depthVid);
    
%     anySkeletonsTracked = any(depthMetaData(95).IsSkeletonTracked ~= 0);
%     trackedSkeletons = find(depthMetaData.IsSkeletonTracked);
    nSkeleton = sum(depthMetaData.IsSkeletonTracked);

    imshow(frameDataColor)%, [0, 4096]);
    
    if nSkeleton > 0
        skeletonJoints = depthMetaData.JointImageIndices(:,:,depthMetaData.IsSkeletonTracked);
%         hold on; 
%         plot(skeletonJoints(:,1), skeletonJoints(:,2), '.', 'MarkerSize', 20);
%         hold off
        skeletonViewer(skeletonJoints, frameDataColor, nSkeleton);
        F = getframe(gcf);
        writeVideo(v, F);
    end 
end 

stop(depthVid);
close(v);