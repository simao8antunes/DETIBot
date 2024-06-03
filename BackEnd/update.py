from Services import URL_Source,Loading,MySql,QStore
from datetime import datetime

import logging
#works but it needs real life work.....
qd = QStore()
db = MySql()
load = Loading()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

logging.info("Starting the update")

date = datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
result_time_table = db.get("SELECT id FROM update_time WHERE update_period <= %s",[date])
logging.info("Query result for date: %s is: %s",date,result_time_table)

for i in result_time_table:
    result_source_table = db.get("SELECT * FROM url_source WHERE update_period_id = %s",[i[0]])
    logging.info("Query result for update_period_id:%s is: %s",i,result_source_table)

    if result_source_table:
        for item in result_source_table:
            logging.info("The following Source is being updated: %s",item)
            child_links = db.get("SELECT url_link FROM url_child_source WHERE parent_id = %s",[item[0]])
            qd.delete_vectors(item[1])
            if child_links:
                for link in child_links:
                    qd.delete_vectors(link[0])
                db.delete_url_child_source(item[0])

            if item[2] == '':
                link_paths = []
            else:    
                link_paths = item[2].split(',')

            logging.info(f"[URL]: {item[1]},[paths]: {link_paths},[period]]: {item[6]},[descpr]: {item[3]},[wait]: {item[4]},[recur]: {bool(item[5])}")
            fonte = URL_Source(url=item[1],paths=link_paths,update_period=item[6],description=str(item[3]),wait_time=item[4],recursive=bool(item[5]))
            load.url_loader(fonte)

for i in result_time_table:
    logging.info("Refresh the date of the update_time table where id=%s, result: %s",i[0],db.update_time(i[0]))

logging.info("Update process finished")

