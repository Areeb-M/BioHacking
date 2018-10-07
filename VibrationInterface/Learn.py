from Locals import *
import pygame
import time
from random import randrange


# Learning Module
window = None
alive = True
font_id = 0
scene_id = 0
characters = 'abcdefghijklmnopqrstuvwxyz1234567890'


def setup_pygame():
    global window
    pygame.init()
    window = pygame.display.set_mode(WINDOW_SIZE)


class Scene:
    def draw(self, draw_window):
        raise NotImplementedError("Please implement a draw function.")

    def update(self):
        raise NotImplementedError("Please implement an update function.")

    def switch_scene(self, scene):
        raise NotImplementedError("Please implement a switch_scene function.")


class MainMenu(Scene):
    def __init__(self):
        self.bg_color = WHITE
        self.l_color = BLACK
        self.t_color = BLACK
        self.q_color = BLACK
        self.l_rect = pygame.Rect(0, 0, 0, 0)
        self.t_rect = pygame.Rect(0, 0, 0, 0)
        self.q_rect = pygame.Rect(0, 0, 0, 0)

    def draw(self, draw_window):
        global font_id
        draw_window.fill(self.bg_color)
        draw_window.blit(font_render(font_id, LARGE, BLACK, "Vibration Interface"), (50, 100))
        self.l_rect = draw_window.blit(font_render(font_id, LARGE, self.l_color, "Learn"), (400, 200))
        self.t_rect = draw_window.blit(font_render(font_id, LARGE, self.t_color, "Test"), (400, 300))
        self.q_rect = draw_window.blit(font_render(font_id, LARGE, self.q_color, "Quit"), (400, 400))
        pygame.display.flip()

    def update(self):
        global alive
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                alive = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.q_color == GRAY:
                    alive = False
                    self.q_color = BLACK
                    return
                elif self.l_color == GRAY:
                    self.switch_scene(1)
                    self.l_color = BLACK
                    return
                elif self.t_color == GRAY:
                    self.switch_scene(2)
                    self.t_color = BLACK
                    return

        mouse_pos = pygame.mouse.get_pos()
        if self.l_rect.collidepoint(mouse_pos):
            self.l_color = GRAY
        else:
            self.l_color = BLACK

        if self.t_rect.collidepoint(mouse_pos):
            self.t_color = GRAY
        else:
            self.t_color = BLACK

        if self.q_rect.collidepoint(mouse_pos):
            self.q_color = GRAY
        else:
            self.q_color = BLACK

    def switch_scene(self, scene):
        global scene_id, scenes
        scenes[1] = Learn()
        scenes[2] = Test()
        scene_id = scene


class Learn(Scene):
    def __init__(self):
        global characters
        self.current_character = randrange(0, len(characters))
        self.start = time.time()
        self.delay = time.time()
        self.hint_period = 5
        self.transmitting = False
        self.mute = True

        self.bg_color = WHITE
        self.hint_color = BLACK
        self.text_color = BLACK

    def draw(self, draw_window):
        global font_id
        if self.delay > time.time():
            return

        draw_window.fill(self.bg_color)
        if time.time() - self.start < self.hint_period:
            draw_window.blit(font_render(font_id, NORMAL, self.hint_color, "Press Escape to Return."), (220, 50))
            draw_window.blit(font_render(font_id, NORMAL, self.hint_color, "    Press M to Mute.   "), (220, 75))

        render = font_render(font_id, GIANT, self.text_color, characters[self.current_character])
        draw_window.blit(render, (300 - render.get_width()/2, 300 - render.get_height()/2))

        pygame.display.flip()

    def update(self):
        global alive, characters, window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                alive = False
                return
            if self.delay > time.time():
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.switch_scene(0)
                elif event.key == pygame.K_m:
                    self.mute = not self.mute
            elif event.type == pygame.MOUSEBUTTONUP:
                self.current_character = randrange(0, len(characters))
                self.transmitting = False

        if not self.transmitting:
            if not self.mute:
                sound = get_audio(characters[self.current_character])
                sound.play()
                self.draw(window)
                self.delay = time.time() + sound.get_length()
            transmit_letter(characters[self.current_character])
            self.transmitting = True

    def switch_scene(self, scene):
        global scene_id, scenes
        scenes[0] = MainMenu()
        scenes[2] = Test()
        scene_id = scene
        clear()


class Test(Scene):
    def __init__(self):
        global characters
        self.question = []
        self.question_rectangle = [pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0)]
        self.question_color = []
        self.answer = 0
        self.transmitting = False
        self.generate_question()

        self.start = time.time()
        self.delay = time.time()

        self.bg_color = WHITE
        self.text_color = BLACK
        self.hint_color = BLACK
        self.correct_color = GREEN
        self.wrong_color = RED
        self.highlight_color = GRAY

    def generate_question(self):
        global characters
        self.question = []
        for i in range(4):
            rand = randrange(0, len(characters))
            while rand in self.question:
                rand = randrange(0, len(characters))
            self.question.append(rand)
        self.answer = randrange(0, 4)
        self.question_color = [BLACK, BLACK, BLACK, BLACK]

    def draw(self, draw_window):
        global font_id, characters

        if self.delay > time.time():
            return

        draw_window.fill(self.bg_color)

        if time.time() - self.start < 5:
            draw_window.blit(font_render(font_id, NORMAL, self.hint_color, "Press Any Key to Return."), (220, 50))

        self.question_rectangle[0] = draw_window.blit(font_render(font_id, GIANT, self.question_color[0], characters[self.question[0]]), (200, 100))
        self.question_rectangle[1] = draw_window.blit(font_render(font_id, GIANT, self.question_color[1], characters[self.question[1]]), (400, 100))
        self.question_rectangle[2] = draw_window.blit(font_render(font_id, GIANT, self.question_color[2], characters[self.question[2]]), (200, 300))
        self.question_rectangle[3] = draw_window.blit(font_render(font_id, GIANT, self.question_color[3], characters[self.question[3]]), (400, 300))

        pygame.display.flip()

    def update(self):
        global alive, window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                alive = False
                return
            if self.delay > time.time():
                return
            if event.type == pygame.KEYDOWN:
                self.switch_scene(0)
            elif event.type == pygame.MOUSEBUTTONUP:
                for i in range(len(self.question_rectangle)):
                    if self.question_rectangle[i].collidepoint(event.pos):
                        if i == self.answer:
                            self.question_color[i] = self.correct_color
                            self.draw(window)
                            self.delay = time.time() + 1
                            self.generate_question()
                            self.transmitting = False
                        else:
                            self.question_color[i] = self.wrong_color
                        break

        if self.delay > time.time():
            return

        mouse_pos = pygame.mouse.get_pos()

        for i in range(len(self.question_rectangle)):
            if self.question_color[i] == self.wrong_color:
                continue
            if self.question_rectangle[i].collidepoint(mouse_pos):
                self.question_color[i] = self.highlight_color
            else:
                self.question_color[i] = self.text_color

        if not self.transmitting:
            transmit_letter(characters[self.question[self.answer]])
            self.transmitting = True

    def switch_scene(self, scene):
        global scene_id, scenes
        scenes[0] = MainMenu()
        scenes[1] = Learn()
        scene_id = scene
        clear()

scenes = [MainMenu(), Learn(), Test()]


def run():
    global alive, scene_id, window
    setup_controller()
    setup_pygame()
    while alive:
        scenes[scene_id].update()
        scenes[scene_id].draw(window)


def main():
    try:
        run()
    except Exception as e:
        print(e)
    clear()

if __name__ == '__main__':
    main()
