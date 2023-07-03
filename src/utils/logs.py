import logging
import sys

log = logging
log.basicConfig(
	format="[%(levelname)s]: %(message)s",
	handlers=[
		logging.StreamHandler(sys.stdout),
		logging.FileHandler("logs.log", mode="a+"),
	],
	level=logging.DEBUG
)