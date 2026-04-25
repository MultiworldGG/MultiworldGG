from BaseClasses import Location

SCORE_THRESHOLDS = [50, 100, 200, 400, 800, 1500, 3000, 5000, 7500, 10000, 14000]

LOCATION_NAME_TO_ID = {
    "Have a 2": 2,
    "Have a 4": 4,
    "Have a 8": 8,
    "Have a 16": 16,
    "Have a 32": 32,
    "Have a 64": 64,
    "Have a 128": 128,
    "Have a 256": 256,
    "Have a 512": 512,
    "Have a 1024": 1024,
    "Have a 2048": 2048,
}

for score in SCORE_THRESHOLDS:
    LOCATION_NAME_TO_ID[f"Reach {score} Points"] = score


class TwoThousandAndFortyEightLocation(Location):
    game = "2048"
