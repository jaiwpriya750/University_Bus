
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

W, H = 1200, 700
bus_x = 0
speed = 2
angle = 0
paused = False

# -------- BASIC FUNCTIONS --------

def rect(x1,y1,x2,y2,c):
    glColor3f(*c)
    glBegin(GL_QUADS)
    for x,y in [(x1,y1),(x2,y1),(x2,y2),(x1,y2)]:
        glVertex2f(x,y)
    glEnd()

def circle(x,y,r,c):
    glColor3f(*c)
    glBegin(GL_POLYGON)
    for i in range(32):
        a=2*math.pi*i/32
        glVertex2f(x+r*math.cos(a),y+r*math.sin(a))
    glEnd()

def line(x1,y1,x2,y2,c,w=2):
    glColor3f(*c)
    glLineWidth(w)
    glBegin(GL_LINES)
    glVertex2f(x1,y1)
    glVertex2f(x2,y2)
    glEnd()

def text(x,y,s,font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glRasterPos2f(x,y)
    for ch in s:
        glutBitmapCharacter(font,ord(ch))

# -------- BACKGROUND --------

def background():
    # Sky
    rect(0,400,W,H,(0.42,0.82,0.97))
    circle(1000,570,38,(1,0.88,0.15))

    # Clouds
    for x,y in [(150,550),(450,510),(850,560)]:
        circle(x,y,22,(1,1,1))
        circle(x+25,y+10,27,(1,1,1))
        circle(x+50,y,22,(1,1,1))

    # Green field
    rect(0,190,W,420,(0.32,0.68,0.22))

    # Trees
    for x in [200,800,1000]:
        rect(x-8,200,x+8,350,(0.35,0.18,0.06))
        circle(x,370,50,(0.04,0.40,0.06))
        circle(x-30,380,35,(0.08,0.52,0.08))
        circle(x+30,380,35,(0.08,0.52,0.08))

    # Grass
    rect(0,170,W,200,(0.18,0.55,0.10))

    # Fixed road
    rect(0,35,W,165,(0.20,0.20,0.20))
    rect(0,160,W,165,(1,1,1))
    rect(0,35,W,40,(1,1,1))

    # Static road markings
    for x in range(0,W,180):
        rect(x,95,x+85,103,(1,0.85,0))

# -------- PASSENGER --------

def passenger(x,shirt):
    # Seat
    rect(x-30,365,x+30,375,(0.12,0.18,0.25))

    # Head
    circle(x,430,13,(0.72,0.43,0.26))
    circle(x-2,440,13,(0.08,0.05,0.03))

    # Neck and body
    rect(x-5,416,x+5,425,(0.72,0.43,0.26))
    rect(x-17,390,x+17,420,shirt)

    # Arms
    line(x-14,410,x-22,385,(0.72,0.43,0.26),5)
    line(x+14,410,x+22,385,(0.72,0.43,0.26),5)

# -------- DRIVER --------

def driver():
    # Driver seat
    rect(320,370,380,380,(0.12,0.12,0.15))

    # Head and hair
    circle(350,430,16,(0.70,0.42,0.25))
    circle(348,441,16,(0.04,0.03,0.02))

    # Body
    rect(344,405,356,420,(0.65,0.40,0.20))
    rect(325,380,370,410,(0.15,0.28,0.75))

    # Arms
    line(330,405,310,390,(0.15,0.28,0.75),9)
    line(310,390,290,405,(0.70,0.42,0.25),6)
    line(365,405,370,390,(0.15,0.28,0.75),9)
    line(370,390,385,405,(0.70,0.42,0.25),6)

    # Steering wheel
    circle(290,405,13,(0.08,0.08,0.08))
    circle(290,405,9,(0.65,0.65,0.65))

    # Legs
    line(340,380,335,350,(0.08,0.12,0.35),10)

# -------- WHEELS --------

def wheel(x,y):
    circle(x,y,43,(0.03,0.03,0.03))
    circle(x,y,34,(0.65,0.65,0.65))
    circle(x,y,27,(0.12,0.12,0.12))

    glColor3f(0.85,0.85,0.85)
    glLineWidth(2)
    glBegin(GL_LINES)
    for i in range(12):
        a=angle+i*math.pi/6
        glVertex2f(x,y)
        glVertex2f(x+27*math.cos(a),y+27*math.sin(a))
    glEnd()

    circle(x,y,7,(0.8,0.8,0.8))

# -------- UNIVERSITY BUS --------

def bus():
    glPushMatrix()
    glTranslatef(bus_x,0,0)

    # Main body
    rect(-400,180,400,510,(0.02,0.25,0.65))

    # Roof
    rect(-400,500,400,515,(1,0.82,0.02))

    # Passenger windows
    for x in [-370,-260,-150,-40,70,180]:
        rect(x,385,x+95,480,(0.58,0.86,0.98))

    # Passengers
    passenger(-325,(0.90,0.15,0.15))
    passenger(-215,(0.95,0.70,0.05))
    passenger(-105,(0.15,0.55,0.25))
    passenger(5,(0.65,0.20,0.65))
    passenger(115,(0.95,0.35,0.10))
    passenger(225,(0.15,0.35,0.75))

    # Window borders
    for x in [-370,-260,-150,-40,70,180]:
        rect(x-3,380,x+3,490,(1,0.82,0.02))
        rect(x+95,380,x+100,490,(1,0.82,0.02))

    # Driver cabin
    rect(300,385,390,485,(0.58,0.86,0.98))
    driver()

    # Front windshield borders
    rect(295,380,305,490,(1,0.82,0.02))
    rect(390,380,400,490,(1,0.82,0.02))

    # Door
    rect(-395,190,-315,370,(0.01,0.18,0.50))
    rect(-380,220,-330,355,(0.58,0.86,0.98))

    # Yellow stripe
    rect(-400,350,400,365,(1,0.82,0.02))

    # University name
    text(-340,315,"Bangladesh Army University",
         GLUT_BITMAP_HELVETICA_18)

    text(-285,290,"of Science and Technology",
         GLUT_BITMAP_HELVETICA_18)

    # SAIDPUR
    glColor3f(1,0.90,0.05)
    glRasterPos2f(-75,225)
    for ch in "SAIDPUR":
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24,ord(ch))

    # Headlights
    circle(410,245,12,(1,1,0.3))
    circle(-410,245,10,(1,0.1,0.1))

    # Bumper
    rect(-425,180,425,195,(0.75,0.75,0.75))

    # Wheels
    wheel(-260,155)
    wheel(260,155)

    glPopMatrix()

# -------- DISPLAY --------

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    background()
    bus()

    glutSwapBuffers()

# -------- ANIMATION --------

def update(value):
    global bus_x,angle

    if not paused:
        bus_x += speed
        angle -= speed*0.06

        if bus_x > 850:
            bus_x = -850

    glutPostRedisplay()
    glutTimerFunc(16,update,0)

# -------- MOUSE CONTROL --------

def mouse(button,state,x,y):
    global bus_x

    if state == GLUT_DOWN:
        if button == GLUT_RIGHT_BUTTON:
            bus_x = min(750,bus_x+40)

        elif button == GLUT_LEFT_BUTTON:
            bus_x = max(-750,bus_x-40)

    glutPostRedisplay()

# -------- KEYBOARD --------

def keyboard(key,x,y):
    global paused

    if key == b'\r':
        paused = not paused

    elif key == b'\x1b':
        glutLeaveMainLoop()

def special(key,x,y):
    global speed

    if key == GLUT_KEY_UP:
        speed = min(10,speed+1)

    elif key == GLUT_KEY_DOWN:
        speed = max(1,speed-1)

# -------- MAIN --------

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGB)
    glutInitWindowSize(W,H)
    glutInitWindowPosition(50,30)
    glutCreateWindow(b"BAUST University Bus Simulation")

    glClearColor(0.4,0.8,0.95,1)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0,W,0,H)

    glMatrixMode(GL_MODELVIEW)

    glutDisplayFunc(display)
    glutMouseFunc(mouse)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special)
    glutTimerFunc(16,update,0)

    glutMainLoop()

if __name__=="__main__":
    main()
