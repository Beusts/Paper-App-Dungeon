import csv
import os
import random


def create_shop_csv_file(name, number_of_items):
    output_dir = os.path.join("data", "shop")
    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, f"{name}.csv"), "w", newline="") as file:
        writer = csv.writer(file)

        items = [
            "Gambler",
            "Light Snack",
            "Medium Snack",
            "Hearty Snack",
            "Doubling Potion",
            "Scroll of Mulligan",
            "Coin Rush",
            "Break on Trought",
            "Teleport Scroll",
            "Magic Shield",
            "Weaklings"
        ]

        items = random.sample(items, number_of_items)

        for item in items:
            writer.writerow([item])
