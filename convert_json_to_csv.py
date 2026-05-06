import json
import csv

def get_categories(name):
    name = name.lower()
    cats = []

    # TYPE
    if any(x in name for x in ["chicken", "egg"]):
        cats.append("Non-Veg" if "chicken" in name else "Egg")
    else:
        cats.append("Veg")

    # FITNESS
    if any(x in name for x in ["chicken", "paneer", "egg", "soya", "tofu"]):
        cats.append("High Protein")

    if any(x in name for x in ["rice", "roti", "naan", "bread", "pav", "noodles", "pasta"]):
        cats.append("High Carb")

    if any(x in name for x in ["fried", "butter", "fries", "pizza", "burger", "pakora"]):
        cats.append("Junk")

    if any(x in name for x in ["salad", "sprouts", "boiled", "grilled"]):
        cats.append("Healthy")

    if any(x in name for x in ["coffee", "juice", "lassi", "drink", "cola"]):
        cats.append("Low Calorie" if "black coffee" in name else "Beverages")

    # STYLE
    if any(x in name for x in ["biryani", "dal", "chole", "rajma", "bhaji", "paneer"]):
        cats.append("Indian")

    if any(x in name for x in ["pav", "puri", "chaat", "misal"]):
        cats.append("Street Food")

    if any(x in name for x in ["burger", "pizza", "fries", "sandwich"]):
        cats.append("Fast Food")

    if any(x in name for x in ["noodles", "manchurian", "schezwan"]):
        cats.append("Chinese")

    if any(x in name for x in ["idli", "dosa", "upma"]):
        cats.append("South Indian")

    if any(x in name for x in ["cake", "chocolate", "sweet", "donut"]):
        cats.append("Desserts")

    if any(x in name for x in ["juice", "cola", "lassi", "coffee"]):
        cats.append("Beverages")

    # remove duplicates
    return ";".join(list(set(cats)))


# LOAD JSON
with open("foods.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# CREATE CSV
with open("newfoods.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow([
        "name",
        "calories_per_100g",
        "protein_per_100g",
        "calories_per_unit",
        "protein_per_unit",
        "unit_type",
        "serving_name",
        "serving_quantity",
        "image",
        "categories"
    ])

    for item in data:
        fields = item["fields"]
        name = fields.get("name", "")

        categories = get_categories(name)

        writer.writerow([
            name,
            fields.get("calories_per_100g", ""),
            fields.get("protein_per_100g", ""),
            fields.get("calories_per_unit", ""),
            fields.get("protein_per_unit", ""),
            fields.get("unit_type", ""),
            fields.get("serving_name", ""),
            fields.get("serving_quantity", ""),
            fields.get("image", ""),
            categories
        ])

print("✅ CSV with categories created!")