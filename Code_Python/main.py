import setup
import Satellite_Loader
import Satellite_list
import Antenna_Site
import check_visibility
import position
import realtime_position
import Reservation
import Reservation_list


def main():
    setup.main()
    Reservation_list.EIRSAT_Obs1.virtual_observation()

if __name__ == "__main__":
    main()
