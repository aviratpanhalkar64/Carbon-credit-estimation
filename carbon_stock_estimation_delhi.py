#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import librarires 
import ee
import pandas as pd


# In[3]:


#Need to authnicate and intialize the earth engine
ee.Authenticate()
ee.Initialize()


# In[5]:


#Area of intrest is Delhi
aoi = ee.Geometry.Rectangle([80.0584, 12.8224, 80.2943, 13.1956])


# In[7]:


#Import land cover and NDVI dataset(MODIS)
landcover = ee.ImageCollection("MODIS/006/MCD12Q1").first().select('LC_Type1')
#NDVI clip by aoi
ndvi = ee.ImageCollection("MODIS/006/MOD13A2").select('NDVI').mean().clip(aoi)


# In[8]:


#Define biomass factors
biomass_factors = {
    1: 300,  # Forest
    2: 150,  # Shrubland
    3: 100,  # Grassland
    4: 200,  # Cropland
    5: 50,   # Urban/Built-up
    6: 0,    # Water
    7: 50,   # Barren
    8: 75,   # Snow and Ice
}


# In[9]:


#calculate biomass for each pixel
biomass_remap = landcover.remap(
    list(biomass_factors.keys()),
    list(biomass_factors.values())
)


# In[11]:


# Define carbon stock conversion factor (50% of biomass is carbon)
carbon_conversion_factor = 0.5

# Calculate carbon stock
carbon_stock = biomass_remap.multiply(carbon_conversion_factor)


# In[12]:


# Aggregate results over the area of interest
carbon_stock_total = carbon_stock.reduceRegion(
    reducer=ee.Reducer.sum(),
    geometry=aoi,
    scale=500,
    maxPixels=1e9
)


# In[15]:


# Extract the carbon stock value based on the key
carbon_stock_key = list(carbon_stock_total_info.keys())[0]
carbon_stock_value = carbon_stock_total_info[carbon_stock_key]


# In[14]:


# Carbon stock total info
carbon_stock_total_info = carbon_stock_total.getInfo()
print("Carbon Stock Total Info:", carbon_stock_total_info)


# In[16]:


# Extract the carbon stock value based on the key
carbon_stock_key = list(carbon_stock_total_info.keys())[0]
carbon_stock_value = carbon_stock_total_info[carbon_stock_key]


# In[18]:


# Convert the result to a pandas DataFrame
df = pd.DataFrame({'Total Carbon Stock (Mg C)': [carbon_stock_value]})
# Save the DataFrame as a CSV file locally
csv_file = 'carbon_stock_delhi.csv'
df.to_csv(csv_file, index=False)
print(f"The estimated total carbon stock in the specified area is {carbon_stock_value} megagrams of carbon (Mg C).")


# In[ ]:




