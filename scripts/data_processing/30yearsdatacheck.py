import os
import shutil
import netCDF4 as nc
from datetime import datetime
source_dir = '/path/to/your/downloaded/HadISD/data'
dest_dir = '/path/to/your/processed/data'
if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)
def check_30_years_data(nc_file):
    try:
        with nc.Dataset(nc_file, 'r') as dataset:
            time_var = dataset.variables['time']
            time_units = time_var.units
            calendar = time_var.calendar
            time_values = nc.num2date(time_var[:], time_units, calendar=calendar)
            start_time = time_values[0]
            end_time = time_values[-1]
            start_30_years = datetime(1993, 1, 1)
            end_30_years = datetime(2023, 1, 1)
            if start_time <= start_30_years and end_time >= end_30_years:
                return True
            else:
                return False
    except Exception as e:
        print(f"Error processing {nc_file}: {e}")
        return False
def process_files_in_directory(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.nc'):  
                file_path = os.path.join(root, filename)
                if check_30_years_data(file_path):
                    #Move files to a new destination directory
                    shutil.move(file_path, os.path.join(dest_dir, filename))
                    print(f"Moved {filename} to {dest_dir}")
                else:
                    print(f"{filename} does not have 30 years of data.")
process_files_in_directory(source_dir)
