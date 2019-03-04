using Microsoft.Kinect;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace KinectConverter
{
    public class Converter
    {
        KinectSensor sensor;

        public Converter()
        {

        }

        public ConverterPoints ConvertPoints(float x, float y, float z)
        {
            //instance of KinectSensor that holds object created by system when Kinect is 
            //plugged in. Has no constructor - cannot be instantiated, just initialized.
            sensor = KinectSensor.KinectSensors[0];
            //create new point 
            SkeletonPoint point = new SkeletonPoint();
            point.X = x;
            point.Y = y;
            point.Z = z;
            //convert point to color space 
            ColorImagePoint colorpoint = sensor.CoordinateMapper.MapSkeletonPointToColorPoint(point, ColorImageFormat.RgbResolution640x480Fps30);
            return new ConverterPoints() { x = colorpoint.X, y = colorpoint.Y };
        }
    }
}
