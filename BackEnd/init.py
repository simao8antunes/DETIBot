from Services import MySql,Loading
from datetime import datetime,timedelta
import logging
#works but it needs real life work.....
db = MySql()
load = Loading()

logging.basicConfig(level=logging.DEBUG)
logging.debug("Automated updater initialized, %s",datetime.now())
#updates the timestamps that are saved
logging.debug("Refresh the date of the update_time table where id=1, result: %s; %s",db.update_time(1),datetime.now())
logging.debug("Refresh the date of the update_time table where id=2, result: %s; %s",db.update_time(2),datetime.now())
logging.debug("Refresh the date of the update_time table where id=3, result: %s; %s",db.update_time(3),datetime.now())
logging.debug("Refresh the date of the update_time table where id=4, result: %s; %s",db.update_time(4),datetime.now())