import pygame as pg
import sys

pg.init()

# Creates Canvas for display
screen = pg.display.set_mode((288, 512))
while True:
    # Input and pre-defined events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    # Update adds any image/object on the predefined canvas
    pg.display.update()

