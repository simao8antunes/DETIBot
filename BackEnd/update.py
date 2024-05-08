from Services import MySql,Loading
from datetime import datetime
import logging
#works but it needs real life work.....
db = MySql()
load = Loading()

logging.basicConfig(level=logging.DEBUG)

logging.debug("Starting the update; %s",datetime.now())

date = datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
result_time_table = db.get("SELECT id FROM update_time WHERE update_period <= %s",[date])
logging.debug("Query result for date: %s is: %s; %s",date,result_time_table,datetime.now())

for i in result_time_table:
    result_source_table = db.get("SELECT url_path,loader_type FROM source WHERE update_period_id = %s",[i[0]])
    logging.debug("Query result for update_period_id:%s is: %s; %s",i,result_source_table,datetime.now())

    for item in result_source_table:
        logging.debug("The following Source is being updated: %s; %s",item[0],datetime.now())
        load.loader(item[0],item[1])

for i in result_time_table:
    logging.debug("Refresh the date of the update_time table where id=%s, result: %s; %s",i[0],db.update_time(i[0]),datetime.now())

logging.debug("Update process finished; %s",datetime.now())

