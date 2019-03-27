clc; clear all; close all;
imaqreset;

v = VideoWriter('demoday_video.avi');
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
    
    nSkeleton = sum(depthMetaData.IsSkeletonTracked);

    imshow(frameDataColor)%, [0, 4096]);
    
    if nSkeleton > 0
        skeletonJoints = depthMetaData.JointImageIndices(:,:,depthMetaData.IsSkeletonTracked);
        skeletonViewer(skeletonJoints, frameDataColor, nSkeleton);
        F = getframe(gcf);
        writeVideo(v, F);
    end 
end 

stop(depthVid);
close(v);
