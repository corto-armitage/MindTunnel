import math
import random
import colorsys
from datetime import datetime

import pygame

WIDTH, HEIGHT = 900, 675
TAU = math.tau


def hsv(hue, saturation, brightness):
    rgb = colorsys.hsv_to_rgb(
        (hue % 360) / 360,
        saturation,
        brightness,
    )
    return tuple(round(channel * 255) for channel in rgb)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(
        "MindTunnel Bands | F: FPS | Space: pause | L: light | R: colors | S: save"
    )
    timer = pygame.time.Clock()
    fps_font = pygame.font.Font(None, 26)
    show_fps = False

    animation_time = 0.0
    palette = 0.0
    twist = 1.0
    petals = 6.0
    quality = 0.6
    average_fps = 60.0
    frame_count = 0

    paused = False
    light_mode = False
    running = True

    cached_key = None
    cached_angles = []

    while running:
        elapsed = max(timer.tick(60) / 1000.0, 0.001)
        dt = min(elapsed, 0.05)
        save_requested = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    palette = random.uniform(0, 360)
                elif event.key == pygame.K_l:
                    light_mode = not light_mode
                elif event.key == pygame.K_f:
                    show_fps = not show_fps
                elif event.key == pygame.K_s:
                    save_requested = True

        if not running:
            break

        if not paused:
            frame_count += 1
            average_fps += (
                min(1.0 / elapsed, 120) - average_fps
            ) * 0.04

            if frame_count > 90:
                if average_fps < 50:
                    quality -= dt * 0.18
                elif average_fps > 58:
                    quality += dt * 0.04
                quality = max(0.0, min(1.0, quality))

            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_held = any(pygame.mouse.get_pressed())
            animation_time += dt * (1.5 if mouse_held else 0.38)

            response = 1 - math.exp(-dt * 2.2)
            target_twist = -3 + 6 * max(0, min(WIDTH, mouse_x)) / WIDTH
            target_petals = 3 + 7 * max(0, min(HEIGHT, mouse_y)) / HEIGHT

            twist += (target_twist - twist) * response
            petals += (target_petals - petals) * response

        detail = 0.0 if light_mode else quality
        rings = 32
        points = 16 * round(4 + 3 * detail)
        petal_count = round(petals)

        # Cache all angle calculations used inside the vertex loop.
        cache_key = (points, petal_count)
        if cache_key != cached_key:
            cached_key = cache_key
            cached_angles = []

            for p in range(points):
                angle = TAU * p / points
                cached_angles.append((
                    math.cos(angle),
                    math.sin(angle),
                    math.cos(angle * 3),
                    math.sin(angle * 3),
                    math.cos(angle * petal_count),
                    math.sin(angle * petal_count),
                ))

        screen.fill(hsv(palette + animation_time * 35, 0.85, 0.95))
        t = animation_time

        global_rotation = 0.12 * math.sin(t * 0.5)
        cg = math.cos(global_rotation)
        sg = math.sin(global_rotation)
        center_x, center_y = WIDTH / 2, HEIGHT / 2

        # Paint large contours first; smaller contours leave broad colored bands.
        # Exponential spacing makes bands widen toward the viewer.
        depths = sorted(
            ((ring / rings + t * 0.19) % 1.0 for ring in range(rings)),
            reverse=True,
        )
        for depth in depths:
            radius = 8 * 190 ** depth
            hue = palette + depth * 300 + t * 35

            # Keep the bands bright throughout the tunnel.
            color = hsv(hue, 0.88, 0.86 + 0.14 * math.sin(depth * TAU * 6) ** 2)

            rotation = twist * depth * 3 + t * 0.25
            cr = math.cos(rotation + global_rotation)
            sr = math.sin(rotation + global_rotation)

            phase = depth * 12 - t * 2
            cp, sp = math.cos(phase), math.sin(phase)

            phase3 = -t + depth * 9
            c3, s3 = math.cos(phase3), math.sin(phase3)

            ox = radius * 0.19 * math.sin(depth * 5 + t)
            oy = radius * 0.19 * math.cos(depth * 4 - t * 0.8)
            offset_x = ox * cg - oy * sg
            offset_y = oy * cg + ox * sg

            vertices = []
            for x, y, cos3, sin3, cos_petal, sin_petal in cached_angles:
                ripple = (
                    1
                    + 0.18 * (sin_petal * cp + cos_petal * sp)
                    + 0.07 * (sin3 * c3 + cos3 * s3)
                )
                r = radius * ripple

                vertices.append((
                    center_x + (x * cr - y * sr) * r + offset_x,
                    center_y + (y * cr + x * sr) * r + offset_y,
                ))

            pygame.draw.polygon(screen, color, vertices)

        pygame.draw.circle(screen, (3, 1, 8), (round(center_x), round(center_y)), 5)

        if show_fps:
            label = fps_font.render(f"{timer.get_fps():.1f} FPS", True, (255, 255, 255))
            box = label.get_rect(topleft=(18, 16)).inflate(16, 10)
            pygame.draw.rect(screen, (12, 12, 20), box, border_radius=5)
            screen.blit(label, (18, 16))

        if save_requested:
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            filename = f"MindTunnel-Bands-{stamp}.png"
            pygame.image.save(screen, filename)
            print(f"Saved {filename}")

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
