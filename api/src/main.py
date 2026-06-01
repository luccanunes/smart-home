import threading
from classes import Lamp, RoutineBehaviour
from utils import read_config
from time import sleep
from datetime import datetime, time, timedelta

def main():
    lamp_list = [Lamp(lamp_dict) for lamp_dict in read_config()]
    wake_up_time = time(6, 30)
    routine_duration_minutes = 30

    print("[INFO] Solar Automation Service started.")
    print(f"[INFO] Sunrise target: {wake_up_time}")

    last_execution = {
        RoutineBehaviour.NORMAL: None,
        RoutineBehaviour.DELAYED: None
    }

    while True:
        now = datetime.now()
        today = now.date()
        
        wake_up_dt = datetime.combine(today, wake_up_time)
        normal_start_time = wake_up_dt - timedelta(minutes=routine_duration_minutes)
        delayed_start_time = wake_up_dt - timedelta(minutes=routine_duration_minutes / 2)
        grace_period = wake_up_dt + timedelta(minutes=2)
        
        if now >= normal_start_time and now <= grace_period and last_execution[RoutineBehaviour.NORMAL] != today:
            print(f"\n[TRIGGER] {now.strftime('%H:%M')} - Starting NORMAL sunrise routines!")
            last_execution[RoutineBehaviour.NORMAL] = today
            
            for lamp in lamp_list:
                if lamp.sunrise_behaviour == RoutineBehaviour.NORMAL:
                    t = threading.Thread(target=lamp.execute_sunrise_routine, args=(routine_duration_minutes,))
                    t.start()

        if now >= delayed_start_time and now <= grace_period and last_execution[RoutineBehaviour.DELAYED] != today:
            print(f"\n[TRIGGER] {now.strftime('%H:%M')} - Starting DELAYED sunrise routines!")
            last_execution[RoutineBehaviour.DELAYED] = today
            
            for lamp in lamp_list:
                if lamp.sunrise_behaviour == RoutineBehaviour.DELAYED:
                    t = threading.Thread(target=lamp.execute_sunrise_routine, args=(routine_duration_minutes / 2,))
                    t.start()

        sleep(5)

if __name__ == "__main__":
    main()