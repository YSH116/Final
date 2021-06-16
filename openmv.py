import pyb, sensor, image, time, math
enable_lens_corr = False # turn on for straighter lines...
sensor.reset()
sensor.set_pixformat(sensor.RGB565) # grayscale is faster
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()

f_x = (2.8 / 3.984) * 160 # find_apriltags defaults to this if not set
f_y = (2.8 / 2.952) * 120 # find_apriltags defaults to this if not set
c_x = 160 * 0.5 # find_apriltags defaults to this if not set (the image.w * 0.5)
c_y = 120 * 0.5 # find_apriltags defaults to this if not set (the image.h * 0.5)


def degrees(radians):
   return (180 * radians) / math.pi

def cm(none):
   return 3 * none

uart = pyb.UART(3,9600,timeout_char=1000)
uart.init(9600,bits=8,parity = None, stop=1, timeout_char=1000)
i=0

while(True):
   clock.tick()
   img = sensor.snapshot()
   if enable_lens_corr: img.lens_corr(1.8) # for 2.8mm lens...
   if i < 20:
       for l in img.find_line_segments(roi = (80, 10, 40, 10), merge_distance = 200, max_theta_diff = 5):
          img.draw_line(l.line(), color = (255, 0, 0))
          line = (l.x1(), l.y1(), l.x2(), l.y2())
          print("x1: %d, y1: %d, x2: %d, y2: %d" % line)
          i+=1
          if (l.x2() < 70) and i < 20:
            uart.write(("/turn/run 40 -0.3 \n").encode())
            time.sleep_ms(100)
            print("right")
          elif (l.x2() > 100) and i < 20:
            uart.write(("/turn/run 40 0.3 \n").encode())
            time.sleep_ms(100)
            print("left")
          elif i > 20:
            break
          else:
            uart.write(("/goStraight/run 40 \n").encode())
            time.sleep_ms(100)
            print("Go straight")
   #uart.write(("/stop/run \n").encode())
   else:
       for tag in img.find_apriltags(fx=f_x, fy=f_y, cx=c_x, cy=c_y): # defaults to TAG36H11
          img.draw_rectangle(tag.rect(), color = (255, 0, 0))
          img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))

          print_args = (cm(tag.x_translation()), cm(tag.y_translation()), cm(tag.z_translation()), \
                degrees(tag.x_rotation()), degrees(tag.y_rotation()), degrees(tag.z_rotation()))
          print(print_args)
          if cm(tag.x_translation()) > 0 and abs(cm(tag.z_translation())) > 14:
            uart.write(("/turn/run 40 0.3 \n").encode())
            print("l")
          elif cm(tag.x_translation()) < 0 and abs(cm(tag.z_translation())) > 14:
            uart.write(("/turn/run 40 -0.3 \n").encode())
            print("r")
          elif abs(cm(tag.z_translation())) < 14:
            uart.write(("/stop/run \n").encode())
            print("stop2\n")
            uart.write(("K \n").encode())
          else:
            uart.write(("/goStraight/run 100 \n").encode())
            print("g")
       print("FPS %f" % clock.fps())
