import sys
import pygame
from typing import Optional


class Game(object):
    def __init__(self, game_width, game_height):
        self._size = self._width, self._height = game_width, game_height
        self._colors = {
            "black": (0, 0, 0),
            "white": (255, 255, 255)
        }

        self._screen = pygame.display.set_mode(self._size)
        self._ship_view = pygame.image.load("sprite_ship.png")
        self._player_bullet_view = pygame.image.load("sprite_player_bullet.png")
        self._alien_bullet_view = pygame.image.load("sprite_alien_bullet.png")
        self._player_bullet: Optional[BulletState] = None
        self._alien_bullets: list[BulletState] = []
        self._ship_model = ShipState(self._width // 2, self._height - self._ship_view.get_height(),
                                     self._width - self._ship_view.get_width())

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
                                self._ship_model.y - self._player_bullet_view.get_height()
                            )
                if event.type == pygame.KEYUP:
                    self._ship_model.ship_change = 0

            self._screen.fill(self._colors["black"])
            self._ship_model.handle_move()
            # update bullet position, remove them if they are off screen, then draw them to the screen
            if self._player_bullet is not None:
                self._player_bullet.handle_move()
                self._screen.blit(self._player_bullet_view, self._player_bullet.coords)
                if self._player_bullet.y < -self._player_bullet_view.get_height():
                    self._player_bullet = None
            # draw the ship
            self._screen.blit(self._ship_view, self._ship_model.coords)
            pygame.display.flip()


class BulletState(object):
    def __init__(self, xpos: int, ypos: int):
        self._x = xpos
        self._y = ypos

    def handle_move(self):
        self._y -= 0.2

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def coords(self):
        return self._x, self._y


class ShipState(object):
    def __init__(self, xpos: int, ypos: int, max_x_pos: int):
        self._x: int = xpos
        self._y: int = ypos
        self.max_x: int = max_x_pos
        self.ship_change: int = 0

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def coords(self):
        return self._x, self._y

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
    game: Game = Game(640, 480)
    game.run_game()


if __name__ == "__main__":
    main()
