from game import game
import logging
from datetime import datetime

if __name__ == "__main__":
    logging.basicConfig(filename=f"..//resources//logs//dog_simulation_{datetime.today}.log", level=logging.INFO, format = '%(levelname)s %(asctime)s %(message)s')
    game = game(4, 1000)
