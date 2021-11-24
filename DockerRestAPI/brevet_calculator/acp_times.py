"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#

min_speed = [(1000, 13.333), (600, 11.428), (400, 15), (200, 15), (0, 15)]
max_speed = [(1000, 26), (600, 28), (400, 30), (200, 32), (0, 34)]


def calculate_time(control_dist, type: list, start_time):

    if isinstance(start_time, str):
        print("converting")
        try:
            start_time = arrow.get(start_time)
        except:  # just in case
            return start_time
            
    for i in type:
        if control_dist > i[0]:
            # print(f"From acp: {brevet_start_time}")
            checkpoint = control_dist - i[0]
            all_time = round(checkpoint / i[1], 2)
            hours = all_time // 1
            minutes = round((all_time % 1) * 60)
            # print(f"Hours: {hours}, Minutes: {minutes}")
            start_time = start_time.shift(hours=hours, minutes=minutes)
            control_dist -= checkpoint

    return start_time


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):  # max speed
    """l ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official)
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """

    return calculate_time(control_dist_km, max_speed,
                          brevet_start_time).isoformat()


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):  # min speed
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """

    return calculate_time(control_dist_km, min_speed,
                          brevet_start_time).isoformat()
