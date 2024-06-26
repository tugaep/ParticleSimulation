import numpy as np
import pygame
import sys
import random
# Constants
WIDTH, HEIGHT = 1000, 1000
BACKGROUND_COLOR = (0, 0, 0)
PARTICLE_COLOR = (255, 255, 255)
FPS = 60

class Particle:
    def __init__(self, position, velocity, color,  mass=1.0, bounds=(0, WIDTH, 0, HEIGHT)):
        self.position = np.array(position, dtype='float64')
        self.velocity = np.array(velocity, dtype='float64')
        self.mass = mass
        self.color = color
        self.bounds = bounds

    def update(self, force, dt):
        acceleration = force / self.mass
        self.velocity += acceleration * dt
        self.position += self.velocity * dt
        self.check_boundaries()

    def check_boundaries(self):
        xmin, xmax, ymin, ymax = self.bounds
        if self.position[0] <= xmin or self.position[0] >= xmax:
            self.velocity[0] *= -1
        if self.position[1] <= ymin or self.position[1] >= ymax:
            self.velocity[1] *= -1

def handle_input():
    keyboard_force = np.array([0.0, 0.0])
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        keyboard_force[1] = -100
    if keys[pygame.K_s]:
        keyboard_force[1] = 100
    if keys[pygame.K_a]:
        keyboard_force[0] = -100
    if keys[pygame.K_d]:
        keyboard_force[0] = 100
    return keyboard_force
def random_particle_color():
   return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Particle Simulation")
    clock = pygame.time.Clock()

    num_particles = 10000
    particles = [Particle(position=np.random.rand(2) * [WIDTH, HEIGHT], 
                          velocity=(np.random.rand(2) - 0.5) * 2, 
                          color=random_particle_color()) for _ in range(num_particles)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        dt = clock.get_time() / 1000.0  # Convert milliseconds to seconds

        # Handle input
        force = handle_input()
        
        # Update particles
        for particle in particles:
            particle.update(force, dt)

        # Clear screen
        screen.fill(BACKGROUND_COLOR)

        # Draw particles
        for particle in particles:
             pygame.draw.circle(screen, particle.color, particle.position.astype(int), 2)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()