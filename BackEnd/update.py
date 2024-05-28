from Services import URL_Source,Loading,MySql,QStore
from datetime import datetime

import logging
#works but it needs real life work.....
qd = QStore()
db = MySql()
load = Loading()

logging.basicConfig(level=logging.DEBUG)

logging.debug("Starting the update; %s",datetime.now())

date = datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
result_time_table = db.get("SELECT id FROM update_time WHERE update_period <= %s",[date])
logging.debug("Query result for date: %s is: %s; %s",date,result_time_table,datetime.now())

for i in result_time_table:
    result_source_table = db.get("SELECT * FROM url_source WHERE update_period_id = %s",[i[0]])
    logging.debug("Query result for update_period_id:%s is: %s; %s",i,result_source_table,datetime.now())

    if result_source_table:
        for item in result_source_table:
            logging.debug("The following Source is being updated: %s; %s",item,datetime.now())
            child_links = db.get("SELECT url_link FROM url_child_source WHERE parent_id = %s",[item[0]])
            qd.delete_vectors(item[1])
            if child_links:
                for link in child_links:
                    qd.delete_vectors(link[0])
                db.delete_url_child_source(item[0])

            link_paths = item[2].split(',')
            fonte = URL_Source(url=item[1],paths=link_paths,update_period=item[3],description=item[4],wait_time=item[5],recursive=item[6])
            load.url_loader(fonte)

for i in result_time_table:
    logging.debug("Refresh the date of the update_time table where id=%s, result: %s; %s",i[0],db.update_time(i[0]),datetime.now())

logging.debug("Update process finished; %s",datetime.now())

