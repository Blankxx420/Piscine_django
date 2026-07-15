from antigravity import geohash
import sys

def check_arguments():
    if len(sys.argv) != 4:
        sys.stderr.write("Error: Wrong number of arguments. Expected Latitude, Longitude, Dow Jone of the combined with date")
        sys.exit(1)

def convert_arguments():
    try:
        latitude = float(sys.argv[1])
        longitude = float(sys.argv[2])
        dow_jones = sys.argv[3].encode('utf-8')
        geohash(latitude, longitude, dow_jones)
    except ValueError:
        sys.stderr.write("Error: Latitude and Longitude must be numbers.\n")
        sys.exit(1)

if __name__ == "__main__":
    check_arguments()
    convert_arguments()