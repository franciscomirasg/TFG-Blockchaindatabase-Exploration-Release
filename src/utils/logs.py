import logging
import sys
from config import global_settings

log = logging

if global_settings.debug_mode:
	log.basicConfig(
		format="[%(levelname)s]: %(message)s",
		handlers=[
			logging.StreamHandler(sys.stdout),
			logging.FileHandler("logs.log", mode="a+"),
		],
		level=logging.DEBUG
	)
else:
	log.basicConfig(
		format="[%(levelname)s]: %(message)s",
		handlers=[
			logging.FileHandler("logs.log", mode="a+"),
		],
		level=logging.INFO
	)