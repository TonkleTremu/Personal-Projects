from PIL import Image
import math
from datetime import datetime

BLACK = (0,0,0)
WHITE = (255,255,255)
CANVAS_SIZE = 51
max_iterations = 100

zoom = 1
offset_x = 0
offset_y = 0

def CheckMandelbrot(point: tuple):
    cx = point[0]
    cy = point[1]
    x = cx
    y = cy
    iteration = 2
    while(cx % iteration != 0 and iteration < x and x < CANVAS_SIZE-2):
        cx = (cx+cy)^(2)
        iteration += 1
    if(cx % (iteration-1) != 0):
        return((100,100,255))
    else:
        #print(cx, (x, y))
        return((50,0,50))
    
def GenMandelbrotImage():
    pixels = []
    start_time = datetime.now()
    for iy in range(round(CANVAS_SIZE)):
        for ix in range(round(CANVAS_SIZE)):
            pixels.append(CheckMandelbrot((ix,iy)))
        if(iy % 100 == 0):
            if(iy == CANVAS_SIZE/10):
                cur_time = datetime.now()
                end_time = datetime.now() + ((cur_time - start_time) * 10)
                print(f"ETA: {end_time}")
            print(iy)
            
    
    img = Image.new("RGB", (CANVAS_SIZE,CANVAS_SIZE))
    img.putdata(pixels)
    img.save("C:/Users/tommy/Documents/GitHub/Personal-Projects/Mandelbrot Fractal/image.jpg")
    print("Image Saved!")

GenMandelbrotImage()