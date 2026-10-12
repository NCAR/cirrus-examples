import requests
import io
import gzip
import os
import shutil
import logging
import xarray as xr
import matplotlib.ft2font
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from urllib.parse import urlparse, parse_qs
from flask import request, make_response

def plot_cygnss_sm():
    """
    Downloads a .nc.gz file, uncompresses it, and plots the SM_daily variable 
    using a Mercator projection. Saves the result as a PNG.
    
    Parameters:
    url (str): The URL of the .nc.gz file.
    output_dir (str): The directory to save the output files.
    """

    
    try:
        file_url = parse_qs(request.query_string.decode('utf-8'))['fileurl']
        # If the environment returns a list of headers, take the first one
        if isinstance(file_url, list):
            file_url = file_url[0]
            
        logging.info(f"Processing URL from header: {file_url}")
    except KeyError:
        logging.error("X-Fission-Params-fileurl header not found.")
        return "Error: Missing file URL header."
    except Exception as e:
        logging.error(f"Error accessing HTTP headers: {e}")
        return "Error: Internal environment error."

    # Extract filename from URL and prepare output names
    filename = file_url.split('/')[-1]
    base_name = filename.replace('.gz', '')  # Name without .gz extension for output
    
    print(f"Downloading {filename}...")
    
    # Define temporary file paths
    temp_gz_filename = '/tmp/plot_input.nc.gz'
    temp_nc_filename = '/tmp/plot_input.nc'
    
    try:
        # 3. Download the file
        logging.info("Downloading file...")
        with requests.get(file_url, stream=True) as r:
            r.raise_for_status()
            with open(temp_gz_filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
    except Exception as e:
        print(e)
    
    print("File downloaded successfully.")
    
    # Uncompress the .gz file
    print(f"Uncompressing...")
    
    with gzip.open(temp_gz_filename, 'rb') as f_in:
        with open(temp_nc_filename, 'wb') as f_out:
            f_out.write(f_in.read())
            
    # Cleanup: Remove the .gz file to save space
    os.remove(temp_gz_filename)
    
    # Load the NetCDF dataset
    if True:
        ds = xr.open_dataset(temp_nc_filename)
        
        # Attempt to load the specific variables requested
        # Note: Check your specific file for exact variable names (case sensitive)
        sm_data = ds['SM_daily']
        lon_data = ds['longitude']
        lat_data = ds['latitude']
        
        print("Dataset loaded. Creating plot...")
        
        # Create the Plot with Mercator Projection
        fig = plt.figure(figsize=(12, 8))
        ax = plt.axes(projection=ccrs.Mercator())
        
        # Plotting using pcolormesh. 
        # shading='auto' handles the grid dimensions automatically.
        im = ax.pcolormesh(
            lon_data, 
            lat_data, 
            sm_data, 
            shading='auto', 
            cmap='viridis', 
            transform=ccrs.PlateCarree()
        )
        
        # Add map features
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.LAND, facecolor='lightgray', alpha=0.5)
        ax.add_feature(cfeature.OCEAN, facecolor='white')
        
        # Add Colorbar
        plt.colorbar(im, ax=ax, label='Soil Moisture (g/cm³ or similar)')
        
        # Set Title and Labels
        plt.title(f'Soil Moisture: {base_name}', fontsize=16)
        # Return Binary Image
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        plt.close(fig)
        
        
        # Close the plot to free memory
        response = make_response(buf.getvalue())
        response.headers.set('Content-Type', 'image/png')
        response.headers.set('Content-Disposition', 'inline', filename='image.png')
        return response
