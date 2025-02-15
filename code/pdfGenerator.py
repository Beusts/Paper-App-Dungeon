from shop import *
from level import Level
from player import Player
import os
from fpdf import FPDF

class PdfGenerator(pygame.sprite.Sprite):

    def __init__(self, level_files, shop_files):
        self.clock = pygame.time.Clock()
        dt = self.clock.tick(FPS) / 1000
        self.player = Player()

        save_path = "recorded_frames"

        # Create folder if it not exist
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        shop_index = 0
        level_index = 0
        nb_files = len(level_files) + len(shop_files)
        print(len(level_files) + len(shop_files))

        for frame_count in range(nb_files):

            current_stage = Level(f"{level_files[level_index]}", self.player)

            if frame_count % FREQUENCY_SPAWN_SHOP == 1 and shop_index < len(shop_files) :
                    current_stage = Shop(f"{shop_files[shop_index]}", self.player)
                    shop_index += 1
            else:
                level_index += 1

            current_stage.run(dt)
            pygame.display.update()

            # Screen shot in memory
            frame_path = os.path.join(save_path, f"frame_{frame_count:03d}.png")
            pygame.image.save(screen, frame_path)
            pygame.display.update()

        pdf = FPDF()
        image_files = sorted(os.listdir(save_path))

        for image_file in image_files:
            img_path = os.path.join(save_path, image_file)
            pdf.add_page()
            pdf.image(img_path, x=10, y=10, w=180)  # manage image size in PDF

            if os.path.exists(save_path):
                os.remove(img_path)

        pdf.output("game_frames.pdf")

