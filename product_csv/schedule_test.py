import schedule
import time


def job():
    print('Hello')


# schedule.every().day.at("03:54").do(job)
schedule.every().hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
