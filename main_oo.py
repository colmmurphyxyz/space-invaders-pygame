# Colm Murphy
# Student no. 121356486
# sprites taken from https://opengameart.org/content/pixel-space-invaders
# font taken from https://www.1001fonts.com/joystix-font.html

import sys
import pygame
from typing import Optional


class GameObjectState(object):
    def __init__(self, xpos, ypos, width, height):
        self._x = xpos
        self._y = ypos
        self._width = width
        self._height = height

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def coords(self):
        return self._x, self._y

    def collides_with(self, other: "GameObjectState") -> bool:
        """Returns True if two game objects are overlapping each other"""
        if (self.x < other.x + other.width and
                self.x + self.width > other.x and
                self.y < other.y + other.height and
                self.height + self.y > other.y):
            return True
        return False


class Game(object):
    def __init__(self, game_width, game_height):
        self._size = self._width, self._height = game_width, game_height
        self._colors = {
            "black": (0, 0, 0),
            "white": (255, 255, 255)
        }

        self._screen = pygame.display.set_mode(self._size)
        # load the ship
        self._ship_view = pygame.image.load("sprite_ship.png")
        self._ship_model = ShipState(self._width // 2, self._height - self._ship_view.get_height(),
                                     self._width - self._ship_view.get_width(),
                                     self._ship_view.get_width(), self._ship_view.get_height())
        # load the aliens
        self._alien_view = pygame.image.load("sprite_alien.png")
        self._aliens: list[AlienState] = []
        # aliens that spawn further from the player will award more points when killed
        for row in range(4):
            for column in range(8):
                points_on_kill = (4 - row) * 10
                self._aliens.append((
                    AlienState(10 + (column * 45), 60 + (row * 45), 1,
                               self._alien_view.get_width(), self._alien_view.get_height(),
                               points_on_kill=points_on_kill)
                ))

        # player bullet logic
        self._player_bullet_view = pygame.image.load("sprite_player_bullet.png")
        self._player_bullet: Optional[BulletState] = None
        # alien bullet logic
        self._alien_bullet_view = pygame.image.load("sprite_alien_bullet.png")
        self._alien_bullets: list[BulletState] = []

        # score
        self._score = 0
        # load font
        self._font = pygame.font.Font("joystix_monospace.ttf", 28)

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        # self._ship_model.handle_move_left()
                        self._ship_model.ship_change = -1
                    if event.key == pygame.K_RIGHT:
                        # self._ship_model.handle_move_right()
                        self._ship_model.ship_change = 1
                    if event.key == pygame.K_SPACE:
                        # if the player has no bullet on-screen, fire a bullet
                        if self._player_bullet is None:
                            self._player_bullet = BulletState(
                                self._ship_model.x + self._ship_view.get_width() // 2
                                - self._player_bullet_view.get_width() // 2,
                                self._ship_model.y - self._player_bullet_view.get_height(),
                                self._player_bullet_view.get_width(),
                                self._player_bullet_view.get_height()
                            )
                if event.type == pygame.KEYUP:
                    self._ship_model.ship_change = 0

            self._screen.fill(self._colors["black"])
            # update the alien positions move them down if necessary
            move_aliens_down = False
            for alien in self._aliens:
                alien.handle_move()
                # if bullet in contact with alien
                if self._player_bullet is not None and self._player_bullet.collides_with(alien):
                    # remove the alien hit, delete the bullet that hit it, and award points to the player
                    # player will get more points if the alien is far away from the ship
                    self._aliens.remove(alien)
                    self._player_bullet = None
                    points = (self._screen.get_height() - alien.y) // 10
                    # round down to the nearest 10
                    points = (points // 10) * 10
                    self._score += alien.points_on_kill + points
                    # if no aliens are left, the player wins
                    if len(self._aliens) == 0:
                        self._player_win()
                    continue
                # if an alien is colliding with the ship, or if the alien is at the bottom of the screen, game over
                if alien.collides_with(self._ship_model) or\
                        alien.y > (self._screen.get_height() - self._alien_view.get_height()):
                    self._game_over()
                # if an alien is at the edge of the screen
                if alien.x not in range(5, self._screen.get_width() - self._alien_view.get_width()):
                    move_aliens_down = True
            # if any alien is at the edge of the screen, move all aliens down and change their direction
            if move_aliens_down:
                for alien in self._aliens:
                    alien.move_down(self._alien_view.get_height() // 8)
                    alien.change_direction()
                    alien.handle_move()
            # update bullet position, remove them if they are off screen, then draw them to the screen
            if self._player_bullet is not None:
                self._player_bullet.handle_move()
                self._screen.blit(self._player_bullet_view, self._player_bullet.coords)
                if self._player_bullet.y < -self._player_bullet_view.get_height():
                    self._player_bullet = None
            # draw the ship
            self._ship_model.handle_move()
            self._screen.blit(self._ship_view, self._ship_model.coords)
            # draw the aliens
            for alien in self._aliens:
                self._screen.blit(self._alien_view, alien.coords)
            # draw the score at the stop of the screen
            message = f"SCORE: {self._score}"
            text = self._font.render(message, True, self._colors["white"])
            text_rect = text.get_rect()
            text_rect.center = (text_rect.width // 2, text_rect.height // 2)
            self._screen.blit(text, text_rect)
            # render
            pygame.display.flip()

    # code from https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
    def _show_end_screen(self, message: str):
        self._screen.fill(self._colors["black"])
        font_large = pygame.font.Font("joystix_monospace.ttf", 64)
        text = font_large.render(message, True, self._colors["white"])
        text_rect = text.get_rect()
        # place text on the center of the screen
        text_rect.center = (self._screen.get_width() // 2, self._screen.get_height() // 2)
        # render final score
        score = f"Final score: {self._score}"
        score_text = self._font.render(score, True, self._colors["white"])
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (self._screen.get_width() // 2, self._screen.get_height() // 2 + 48)
        # (press any key to play again)
        play_again = self._font.render("press any key to play again", True, self._colors["white"])
        play_again_rect = play_again.get_rect()
        play_again_rect.center = (self._screen.get_width() // 2, (self._screen.get_height() // 2) + 80)
        while True:
            self._screen.fill(self._colors["black"])
            self._screen.blit(text, text_rect)
            self._screen.blit(score_text, score_text_rect)
            self._screen.blit(play_again, play_again_rect)
            # wait for user to exit the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    main()
            pygame.display.flip()

    def _player_win(self):
        self._show_end_screen("You Win!")

    def _game_over(self):
        self._show_end_screen("Game Over :(")


class BulletState(GameObjectState):
    def __init__(self, xpos: int, ypos: int, width: int, height: int):
        super().__init__(xpos, ypos, width, height)

    def handle_move(self):
        self._y -= 0.4


class AlienState(GameObjectState):
    def __init__(self, xpos: int, ypos: int, speed, width: int, height: int, points_on_kill: int):
        super().__init__(xpos, ypos, width, height)
        self._xchange = speed
        # amount of points to give the player when this alien is killed
        self.points_on_kill = points_on_kill
        # we only want to update the alien's position every 10 frames
        self._frame_counter = 0

    def handle_move(self):
        if self._frame_counter == 9:
            self._x += self._xchange
        self._frame_counter += 1
        self._frame_counter %= 10

    def change_direction(self):
        self._xchange = self._xchange * -1

    def move_down(self, ychange: int):
        self._y += ychange


class ShipState(GameObjectState):
    def __init__(self, xpos: int, ypos: int, max_x_pos: int, width: int, height: int):
        super().__init__(xpos, ypos, width, height)
        self.max_x: int = max_x_pos
        self.ship_change: int = 0

    def handle_move(self):
        if self._x + self.ship_change in range(0, self.max_x):
            self._x += self.ship_change

    def handle_move_left(self):
        if self._x - self.ship_change > 0:
            self._x -= self.ship_change

    def handle_move_right(self):
        if self._x + self.ship_change < self.max_x:
            self._x += self.ship_change

    def handle_stop_move(self):
        self._x = self._x


def main():
    pygame.init()
    game: Game = Game(640, 480)
    game.run_game()


if __name__ == "__main__":
    main()
