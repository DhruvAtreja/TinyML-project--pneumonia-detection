# Edge Impulse - OpenMV Image Classification Example
# Modifications by Arijit Das and Zin Kyaw
import sensor, image, time, os, tf

sensor.reset()                         # Reset and initialize the sensor.
sensor.set_pixformat(sensor.GRAYSCALE)    # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)      # Set frame size to QVGA (320x240)
sensor.set_windowing((240, 240))       # Set 240x240 window.
#sensor.set_auto_whitebal(True)
#sensor.set_auto_gain(True)
sensor.skip_frames(time=1000)          # Let the camera adjust.

net = "trained.tflite"
labels = [line.rstrip('\n') for line in open("labels.txt")]

clock = time.clock()
while(True):
    clock.tick()

    img = sensor.snapshot()

    # default settings just do one detection... change them to search the image...
    for obj in tf.classify(net, img, min_scale=1.0, scale_mul=0.8, x_overlap=0.5, y_overlap=0.5):
        print("**********\nPredictions at [x=%d,y=%d,w=%d,h=%d]" % obj.rect())
        img.draw_rectangle(obj.rect())
        # This combines the labels and confidence values into a list of tuples
        predictions_list = list(zip(labels, obj.output()))


        for i in range(len(predictions_list)):
           print("%s = %f" % (predictions_list[i][0], predictions_list[i][1]))

           if predictions_list[i][0] == 'bacteria' and predictions_list[i][1] > 0.5:
              print("Bacteria")
              img.draw_string(10,10, "Bacteria", scale=3, mono_space=False)
           elif predictions_list[i][0] == 'normal' and predictions_list[i][1] > 0.5:
              print("Normal")
              img.draw_string(10,10, "Normal", scale=3, mono_space=False)
           elif predictions_list[i][0] == 'virus' and predictions_list[i][1] > 0.5:
              print("Virus")
              img.draw_string(10,10, "Virus", scale=3, mono_space=False)


    print(clock.fps(), "fps")
