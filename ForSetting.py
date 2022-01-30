import os
import shutil

from run import delete_img, create_random_name, copy_image


imgs = ["cats/cat1.jpeg", "cats/cat2.jpeg", "cats/cat3.jpeg", "cats/cat4.jpg", "cats/cat5.jpg", "cats/cat6.jpg"]
for i in range(len(imgs)):
    print(copy_image(imgs[i], f"cat/cat_{i + 1}/{create_random_name(50)}.png"))