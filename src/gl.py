''' 
--------------------------------------
  Universidad del Valle de Guatemala
  Author: Diego Cordova - 20212

  gl.py
  - Uses de Renderer Object to
    write bmp files

  Last modified (yy-mm-dd): 2022-07-24
--------------------------------------
'''

from .Render import Render
from .util import color
from .Vector import V3

def glInit():
  ''' Initialized Internal Render Object '''
  global SR
  SR = Render()

def sr_isInit():
  '''
    Checks if Internal Object is Initialized
    If not, reaises exception
  '''

  try:
    SR.current_color

  except NameError:
    raise Exception('ERROR: Software Renderer not initialized\n\
       execute glInit before any action\n\
    ')

def glCreateWindow(width: int, height: int):
  ''' Initialize Window of image '''
  sr_isInit()
  SR.initWindow(width=width, height=height)

def glCreateViewPort(width: int, height: int):
  ''' Initialize viewport of image '''
  sr_isInit()
  SR.initViewPort(width=width, height=height)

  global v_width_d
  global v_height_d
  global v_width_u
  global v_height_u
  global x_offset
  global y_offset 
  v_width_d = (SR.viewPort_w - 1) / 2
  v_height_d = (SR.viewPort_h - 1) / 2
  v_width_u = SR.viewPort_w / 2
  v_height_u = SR.viewPort_h / 2
  x_offset = round((SR.window_w - width) / 2)
  y_offset = round((SR.window_h - height) / 2)

def glClear():
  ''' Fills image with one plain color (clear_color)'''
  sr_isInit()
  SR.clear()

def glCLearColor(r, g, b):
  ''' changes clear_color'''
  sr_isInit()
  SR.set_clear_color(color(r, g, b))

def glColor(r, g, b):
  ''' changes the color for writting pixels '''
  sr_isInit()
  SR.set_current_color(color(r, g, b))

def glFinish(fileName):
  ''' Writes bmp file '''
  sr_isInit()
  try:
    SR.write(fileName + '.bmp')
    print('File', fileName + '.bmp written succesfully!!')
  except:
    print('ERROR during file writting')

def denormalize(x, y):
  ''' 
    Takes normalized coordinates and transforms
    them into coordinates for the framebuffer
    inside the viewport
  '''
  sr_isInit()

  actual_w = v_width_d if x <= 0 else v_width_u
  actual_h = v_height_d if y <= 0 else v_height_u

  y_normal = round(actual_h * (y + 1)) + y_offset
  x_normal = round(actual_w * (x + 1)) + x_offset
  return x_normal, y_normal

def glVertex(x, y, normalized:bool=True):
  ''' writes a pixel inside the viewport '''
  sr_isInit()
  if normalized:
    if x < -1 or x > 1: raise Exception('invalid coordinates:', [x, y])
    if y < -1 or y > 1: raise Exception('invalid coordinates:', [x, y])

  points = denormalize(x, y) if normalized else (x, y)
  SR.point(*points)

def glLine(x0, y0, x1, y1, normalized=False):
  '''
    Draws a line of pixels from point
    [x0, y0] to [x1, y1] on the viewport
  '''
  sr_isInit()

  if normalized:
    x0, y0 = denormalize(x0, y0)
    x1, y1 = denormalize(x1, y1)
    
  SR.line(x0, y0, y0, y1)

# ------------ Funciones para Relleno de Poligonos ------------

def denormalize_poly(p:list[list]) -> list[list]:
  temp_a = []

  for n in range(len(p)):
    temp_a.append([*denormalize(*p[n])])

  return temp_a

def perim_fig(p:list[list], normalized=True):
  ''' Draws the contorn of a polygon based a series of points '''
  if normalized == True:
    p = denormalize_poly(p)

  SR.draw_perim_fig(p)

def pintar(p:list[list], normalized=True):
  ''' Fills the area of a polygon with color '''
  if normalized == True:
    p = denormalize_poly(p)
  
  SR.paint_face(p)

def wireframe_model(
  model_path, transform, scale, 
  vertex_to_draw = (0, 1), option='draw'
):
  SR.wireframe_model(model_path, transform, scale, vertex_to_draw, option)

  #SR.draw_perim_fig([
  #  [A.x, A.y], [B.x, B.y], [C.x, C.y]
  #], color)