from PIL import Image
import math
from datetime import datetime

BLACK = (0,0,0)
WHITE = (255,255,255)
CANVAS_SIZE = 25000
max_iterations = 100

zoom = 0.25
offset_x = -CANVAS_SIZE/2
offset_y = -CANVAS_SIZE/2

def CheckMandelbrot(point: tuple):
    cx = point[0]
    cy = point[1]
    x = 1.1
    y = 0
    iteration = 0
    while(x*x + y*y <= 2*2 and iteration < max_iterations):
        new_x = (x*x) - (y*y) + cx
        y = (2*x*y) + cy
        x = new_x
        iteration += 1
    if(iteration == max_iterations):
        return(BLACK)
    else:
        color = round(255*iteration/25)
        if(color > 255):
            color = 255
        return((0,0,color))
    
def GenMandelbrotImage():
    pixels = []
    start_time = datetime.now()
    for iy in range(round(CANVAS_SIZE)):
        for ix in range(round(CANVAS_SIZE)):
            pixels.append(CheckMandelbrot((((ix+offset_x)/(CANVAS_SIZE*zoom)),(iy+offset_y)/(CANVAS_SIZE*zoom))))
        if(iy % 100 == 0):
            if(iy == CANVAS_SIZE/10):
                cur_time = datetime.now()
                end_time = datetime.now() + ((cur_time - start_time) * 10)
                print(f"ETA: {end_time}")
            print(iy)
            
    
    img = Image.new("RGB", (CANVAS_SIZE,CANVAS_SIZE))
    img.putdata(pixels)
    img.save("C:/Users/tommy/Documents/GitHub/DSD-Y1/Random Test Stuff/Mandelbrot Fractal/image.jpg")
    print("Image Saved!")

GenMandelbrotImage()