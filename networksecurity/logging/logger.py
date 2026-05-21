import logging
import os
from datetime import datetime

LOG_FILE=f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log"

logpath=os.path.join(os.getcwd(), "logs", LOG_FILE)

os.makedirs(os.path.dirname(logpath), exist_ok=True)

LOG_FILE_PATH=os.path.join(os.getcwd(), "logs", LOG_FILE)

logging.basicConfig(
filename=LOG_FILE_PATH,
level=logging.INFO,
format='%(asctime)s - %(levelname)s - %(message)s'

)