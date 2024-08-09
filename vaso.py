import pygame as py

sensorUmidade=3
sensorLdr=3
sensorTemperatura=3
def draw_rect(x,y,sizex,sizey,color):
    py.draw.rect(screen,color,(x,y,sizex,sizey))
def draw_line(x,y,x2,y2,color):
    while x!=x2 and y!=y2:
        draw_rect(x,y,12.5,12.5,color)
        x+=12.5
        y-=12.5

def draw_face(how):
    draw_rect(400,300,200,50,(150,75,0))
    draw_rect(425,350,150,50,(150,75,0))
    draw_rect(450,400,100,50,(150,75,0))

    draw_line(525,300,600,225,(0,255,0))
    draw_rect(587.5,225,12.5,12.5,(0,255,0)) 
    

    if how=="nice":
        draw_rect(440,350,12.5,12.5,(255,255,255))
        draw_rect(452,338,25,12.5,(255,255,255))
        draw_rect(477,350,12.5,12.5,(255,255,255))

        draw_rect(515,350,12.5,12.5,(255,255,255))
        draw_rect(527,338,25,12.5,(255,255,255))
        draw_rect(552,350,12.5,12.5,(255,255,255))

        draw_rect(477,375,12.5,25,(255,255,255))
        draw_rect(487,400,25,12.5,(255,255,255))
        draw_rect(512,375,12.5,25,(255,255,255))


py.init()
screen = py.display.set_mode((1280, 720))
game_over=False


while not game_over:
    for event in py.event.get():
        if event.type == py.QUIT:
            game_over=True
    screen.fill((0,0,0))
    draw_face("nice")

    py.display.update()
py.quit()

