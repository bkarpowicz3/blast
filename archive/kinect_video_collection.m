colorVid = videoinput('kinect', 1);
depthVid = videoinput('kinect', 2);

triggerconfig([colorVid depthVid], 'manual');

colorVid.FramesPerTrigger = 100;
depthVid.FramesPerTrigger = 100;

%start devices
start([colorVid depthVid]);
% trigger logging 
% trigger([colorVid depthVid]);

disp('Setup complete');

while 1 
    %trigger logging 
    trigger([colorVid depthVid]);
    
    [frameDataColor, colorTimeData, colorMetaData] = getdata(colorVid);
    [depthFrameData, depthTimeData, metaDataDepth] = getdata(depthVid);

    depthSrc = getselectedsource(depthVid);
    depthSrc.TrackingMode = 'Skeleton';

    anyPositionsTracked = any(metaDataDepth(95).IsPositionTracked ~= 0);
    anySkeletonsTracked = any(metaDataDepth(95).IsSkeletonTracked ~= 0);
    trackedSkeletons = find(metaDataDepth(95).IsSkeletonTracked);

    jointCoordinates = metaDataDepth(95).JointWorldCoordinates(:,:,trackedSkeletons);
    jointIndices = metaDataDepth(95).JointImageIndices(:,:,trackedSkeletons);

    image = frameDataColor(:,:,:,95);
    nSkeleton = length(trackedSkeletons);
    skeletonViewer(jointIndices, image, nSkeleton);
end 

stop([colorVid depthVid]);


