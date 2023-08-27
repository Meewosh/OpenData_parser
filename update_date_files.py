import wget
import zipfile
import os
from main import home


def download_file(url, directory_name):
    filename = wget.download(url, out=directory_name)
    print("\nDownloaded file: " + filename)
    unzip_file(directory_name, filename)
    

def unzip_file(directory_name, filename):
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(directory_name)
    print("\nUnzipped file: " + filename)
    remove_file(directory_name, filename)
    

def remove_file(directory_name, filename):
    pathname = os.path.abspath(os.path.join(directory_name, filename))
    if pathname.startswith(directory_name):
        os.remove(pathname)
    print("\nRemoved file: " + filename)
    

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# KRAKÓW
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
krakow_url_path_bus = 'https://gtfs.ztp.krakow.pl/GTFS_KRK_A.zip'
krakow_data_path_bus = home + "/data/Krakow/bus/"

krakow_url_path_tram = 'https://gtfs.ztp.krakow.pl/GTFS_KRK_T.zip'
krakow_data_path_tram = home + "/data/Krakow/tram/"

download_file(krakow_url_path_bus, krakow_data_path_bus)
download_file(krakow_url_path_tram, krakow_data_path_tram)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# POZNAŃ
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

poznan_url_path_ = 'https://www.ztm.poznan.pl/pl/dla-deweloperow/getGTFSFile'
poznan_data_path = home + "/data/Poznan/"


download_file(poznan_url_path_, poznan_data_path)
