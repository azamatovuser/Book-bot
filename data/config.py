import os

from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("ip")
BASE_URL = env.str("BASE_URL")
CHANNELS = ['-1001852213398']
BOT_ID = os.environ.get('BOT_ID')