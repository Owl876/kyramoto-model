#все ориентируются на первого
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
import pygame
import math
import pygame_widgets
import itertools
import random
import numpy as np


class Operator:
    def __init__(self, name, freq, phase):
        self.name = name
        self.freq = freq    
        self.phase = phase  


class Settings:
    K = 0.3
    dt = 0.1
    dt_counter = 0
    syncTrue = False
    syncTime = 0
    run = True
    showSync = True
    syncStatus = 0
    max_distance = [[0, i, j, 0, 0] for i, j in itertools.combinations(range(6), 2)]


start_frequencies = np.random.normal(1, 0.15, 6)
operator1 = Operator("operator1", start_frequencies[0], round(random.random() * 2* math.pi, 2))
operator2 = Operator("operator2", start_frequencies[1], round(random.random() * 2* math.pi, 2))
operator3 = Operator("operator3", start_frequencies[2], round(random.random() * 2* math.pi, 2))
operator4 = Operator("operator4", start_frequencies[3], round(random.random() * 2* math.pi, 2))
operator5 = Operator("operator5", start_frequencies[4], round(random.random() * 2* math.pi, 2))
operator6 = Operator("operator6", start_frequencies[5], round(random.random() * 2* math.pi, 2))
allOperators = [operator1, operator2, operator3, operator4, operator5, operator6]
for i in range(0,6):
    print (allOperators[i].name, allOperators[i].freq, allOperators[i].phase)

def rk4(deriv, y, dt):
    k1 = dt * deriv(y)
    k2 = dt * deriv(y + k1 / 2)
    k3 = dt * deriv(y + k2 / 2)
    k4 = dt * deriv(y + k3)
    return (k1 + 2 * k2 + 2 * k3 + k4) / 6


def update():
    K = Settings.K
    dt = Settings.dt
    def dPhase(i, phase):
        d_phase = allOperators[i].freq
        for j, op in enumerate(allOperators):
            if j < i:
                d_phase += K * (1-i*0.05) * math.sin(allOperators[0].phase - phase)
        return d_phase / (i+1)

    for i, op in enumerate(allOperators):
        d_phase = rk4(lambda phase: dPhase(i, phase), op.phase, dt)
        op.phase += d_phase
        op.phase %= 2 * math.pi
        op.freq = d_phase / dt



def getPosition(operator: Operator) -> tuple[float, float]:
    x = -200 * math.cos(operator.phase) + 640
    y = 200 * math.sin(operator.phase) + 360
    return (x, y)


def draw_circles() -> None:
    op_colors = [(255, 0, 0), (255, 255, 0), (0, 0, 255), (255, 0, 255), (0, 255, 0), (0, 255, 255)]
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (0, 0, 0), (640, 360), 200, width=5)

    for i, operator in enumerate(allOperators):
        color = op_colors[i]
        pygame.draw.circle(screen, color, getPosition(operator), 10)



# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Kuramoto Model")

left_x_border = 0
left_y_border = -25

k_slider = Slider(screen, left_x_border + 50, left_y_border + 50, 200, 20, min=0, max=10,
                  step=0.001, initial=0.3, handleColour=(0, 0, 0))
K_text = TextBox(screen, left_x_border + 90, left_y_border +
                 80, 70, 30, fontSize=20, inputBox=True, inputType='numeric')
K_text.disable()



dt_slider = Slider(screen, left_x_border + 50, left_y_border + 150, 200, 20, min=0.001, max=1,
                   step=0.001, initial=0.01, handleColour=(0, 0, 0))
dt_text = TextBox(screen, left_x_border + 90, left_y_border +
                  180, 70, 30, fontSize=20, inputBox=True, inputType='numeric')
dt_text.disable()
clock = pygame.time.Clock()
op_colors = TextBox(screen, left_x_border + 50, left_y_border + 220, 150, 30, fontSize=20)
op_colors.setText("Цвета гребцов:")

op_text_colors = [
    (TextBox(screen, left_x_border + 50, left_y_border + 250 + i * 30, 150, 30, fontSize=20))
    for i in range(len(allOperators))
]

op_text_colors[0].setText("Red - 1 гребец")
op_text_colors[1].setText("Yellow - 2 гребец")
op_text_colors[2].setText("Blue - 3 гребец")
op_text_colors[3].setText("Purple - 4 гребец")
op_text_colors[4].setText("Green - 5 гребец")
op_text_colors[5].setText("Light blue - 6 гребец")


button_x = left_x_border + 50
button_y = left_y_border + 80

k_plusButton = Button(screen, button_x + 120, button_y, 30, 30, text='+', fontSize=20,
                      inactiveColour=(100, 100, 100), pressedColour=(150, 150, 150))
k_plusButton.setInactiveColour((200, 200, 200))

k_minusButton = Button(screen, button_x, button_y, 30, 30, text='-', fontSize=20,
                       inactiveColour=(100, 100, 100), pressedColour=(150, 150, 150))
k_minusButton.setInactiveColour((200, 200, 200))



dt_plusButton = Button(screen, button_x + 120, button_y + 100, 30, 30, text='+', fontSize=20,
                       inactiveColour=(100, 100, 100), pressedColour=(150, 150, 150))
dt_plusButton.setInactiveColour((200, 200, 200))

dt_minusButton = Button(screen, button_x, button_y + 100, 30, 30, text='-', fontSize=20,
                        inactiveColour=(100, 100, 100), pressedColour=(150, 150, 150))
dt_minusButton.setInactiveColour((200, 200, 200))

while Settings.run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Settings.run = False
    update()
    draw_circles()

    if k_plusButton.clicked:
        k_slider.setValue(k_slider.getValue() + 0.0001)
    if k_minusButton.clicked:
        k_slider.setValue(k_slider.getValue() - 0.0001)
    if dt_plusButton.clicked:
        dt_slider.setValue(dt_slider.getValue() + 0.001)
    if dt_minusButton.clicked:
        dt_slider.setValue(dt_slider.getValue() - 0.001)

    k_plusButton.draw()
    k_minusButton.draw()
    dt_plusButton.draw()
    dt_minusButton.draw()

    K_val = round(k_slider.getValue(), 3)
    K_text.setText(f"K = {K_val:.3f}")
    if K_val != Settings.K:
        Settings.syncTrue = False
        Settings.syncTime = 0
        Settings.showSync = False
    Settings.K = K_val

    dt_val = round(dt_slider.getValue(), 3)
    dt_text.setText(f"dt = {dt_val:.3f}")
    if dt_val != Settings.dt:
        Settings.syncTrue = False
        Settings.syncTime = 0
        Settings.showSync = False
    Settings.dt = dt_val

    Settings.dt_counter += dt_slider.getValue()
    font = pygame.font.SysFont("comicsansms", 20)
    text = font.render(
        f"Время = {round(Settings.dt_counter, 3):.2f}", True, (0, 0, 0))
    screen.blit(text, (1090, 200))

    text = font.render(f"Частота каждого гребца", True, (0, 0, 0))
    screen.blit(text, (1000, 10))
    string_to_render = f"1 = {abs(allOperators[0].freq):.3f}"
    text = font.render(string_to_render, True, (0, 0, 0))
    screen.blit(text, (1050, 35))
    string_to_render = f"2 = {abs(allOperators[1].freq):.3f}"
    text = font.render(string_to_render, True, (0, 0, 0))
    screen.blit(text, (1050, 60))
    string_to_render = f"3 = {abs(allOperators[2].freq):.3f}"
    text = font.render(string_to_render, True, (0, 0, 0))
    screen.blit(text, (1050, 85))
    string_to_render = f"4 = {abs(allOperators[3].freq):.3f}"
    text = font.render(string_to_render, True, (0, 0, 0))
    screen.blit(text, (1050, 110))
    string_to_render = f"5 = {abs(allOperators[4].freq):.3f}"
    text = font.render(string_to_render, True, (0, 0, 0))
    screen.blit(text, (1050, 135))
    string_to_render = f"6 = {abs(allOperators[5].freq):.3f}"
    text = font.render(string_to_render, True, (0, 0, 0))
    screen.blit(text, (1050, 160))

    pygame_widgets.update(pygame.event.get())

    pygame.display.flip()

pygame.display.quit()

pygame.quit()