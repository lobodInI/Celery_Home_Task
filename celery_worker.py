import time
import sqlite3
from datetime import datetime
from resize_maker import resize
from celery import Celery


app = Celery('celery_worker', broker='pyamqp://guest@localhost//')


@app.task
def task1(image_path):
    time.sleep(10)
    resize(image_path)

    con = sqlite3.connect("celery_db")
    cur = con.cursor()
    cur.execute(f"""UPDATE info_process SET status = 'Done', 
                                            datetime = '{datetime.now().strftime("%d/%m/%Y  %H:%M:%S")}' 
                                        WHERE file_name = '{image_path}'""")
    con.commit()
    con.close()

    return True