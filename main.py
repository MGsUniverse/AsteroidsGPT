import tkinter as tk
import random

class Spaceship:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.id = canvas.create_polygon(10, 10, 10, 50, 60, 30, fill="blue")
        self.canvas.move(self.id, x, y)
        self.velocity_x = 0
        self.velocity_y = 0
        self.canvas.bind_all("<KeyPress-Left>", self.move_left)
        self.canvas.bind_all("<KeyPress-Right>", self.move_right)
        self.canvas.bind_all("<KeyPress-Up>", self.move_up)
        self.canvas.bind_all("<KeyPress-Down>", self.move_down)
        self.canvas.bind_all("<KeyPress-space>", self.fire)

        self.bullets = []

    def move_left(self, event):
        self.velocity_x = -2

    def move_right(self, event):
        self.velocity_x = 2

    def move_up(self, event):
        self.velocity_y = -2

    def move_down(self, event):
        self.velocity_y = 2

    def fire(self, event):
        coords = self.get_coords()
        if coords:
            x = (coords[0] + coords[2]) / 2
            y = (coords[1] + coords[3]) / 2
            bullet = Bullet(self.canvas, x, y)
            self.bullets.append(bullet)

    def update(self):
        self.canvas.move(self.id, self.velocity_x, self.velocity_y)

        # Check boundaries
        coords = self.canvas.coords(self.id)
        if coords:
            right, bottom = coords[2], coords[3]
            if right < 0:
                self.canvas.move(self.id, WIDTH + 60, 0)
            elif right > WIDTH:
                self.canvas.move(self.id, -WIDTH - 60, 0)
            if bottom < 0:
                self.canvas.move(self.id, 0, HEIGHT + 60)
            elif bottom > HEIGHT:
                self.canvas.move(self.id, 0, -HEIGHT - 60)

        # Update bullets
        for bullet in self.bullets:
            bullet.update()
            if bullet.is_destroyed():
                self.bullets.remove(bullet)

    def get_coords(self):
        return self.canvas.coords(self.id)


class Bullet:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.id = canvas.create_oval(0, 0, 10, 10, fill="yellow")
        self.canvas.move(self.id, x, y)
        self.velocity = 5
        self.destroyed = False

    def update(self):
        self.canvas.move(self.id, 0, -self.velocity)
        coords = self.canvas.coords(self.id)
        if coords and coords[1] < 0:
            self.destroyed = True
            self.canvas.delete(self.id)

    def is_destroyed(self):
        return self.destroyed


# Window dimensions
WIDTH = 800
HEIGHT = 600

# Game loop
# Game loop
def game_loop():
    window = tk.Tk()
    window.title("Asteroid Dodge")

    canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT)
    canvas.pack()

    spaceship = Spaceship(canvas, WIDTH // 2, HEIGHT // 2)

    asteroids = []
    for _ in range(10):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        dx = random.uniform(-1, 1)
        dy = random.uniform(-1, 1)
        asteroid = canvas.create_oval(10, 10, 60, 60, fill="red")
        canvas.move(asteroid, x, y)
        asteroids.append((asteroid, dx, dy))

    def check_collision():
        spaceship_coords = spaceship.get_coords()
        for asteroid in asteroids:
            asteroid_coords = canvas.coords(asteroid[0])
            if spaceship_coords and asteroid_coords:
                x_collision = (
                    spaceship_coords[0] <= asteroid_coords[2]
                    and spaceship_coords[2] >= asteroid_coords[0]
                )
                y_collision = (
                    spaceship_coords[1] <= asteroid_coords[3]
                    and spaceship_coords[3] >= asteroid_coords[1]
                )
                if x_collision and y_collision:
                    print("Game Over!")
                    window.quit()

                # Check bullet collisions
                for bullet in spaceship.bullets:
                    bullet_coords = canvas.coords(bullet.id)
                    if bullet_coords and asteroid_coords:
                        x_collision = (
                            bullet_coords[0] <= asteroid_coords[2]
                            and bullet_coords[2] >= asteroid_coords[0]
                        )
                        y_collision = (
                            bullet_coords[1] <= asteroid_coords[3]
                            and bullet_coords[3] >= asteroid_coords[1]
                        )
                        if x_collision and y_collision:
                            spaceship.bullets.remove(bullet)
                            canvas.delete(bullet.id)
                            canvas.delete(asteroid[0])
                            asteroids.remove(asteroid)
                            break

    def update_game():
        # Update spaceship
        spaceship.update()

        # Update asteroids
        for asteroid in asteroids:
            canvas.move(asteroid[0], asteroid[1], asteroid[2])
            asteroid_coords = canvas.coords(asteroid[0])
            if asteroid_coords:
                right, bottom = asteroid_coords[2], asteroid_coords[3]
                if right < 0:
                    canvas.move(asteroid[0], WIDTH + 60, 0)
                elif right > WIDTH:
                    canvas.move(asteroid[0], -WIDTH - 60, 0)
                if bottom < 0:
                    canvas.move(asteroid[0], 0, HEIGHT + 60)
                elif bottom > HEIGHT:
                    canvas.move(asteroid[0], 0, -HEIGHT - 60)

        # Check collisions
        check_collision()

        # Repeat the game loop
        canvas.after(10, update_game)

    update_game()

    window.mainloop()


# Start the game loop
game_loop()
