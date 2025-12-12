# AHT20_F Humidity Wrapper for Mainsail
#
# The compiled aht20_f.so module doesn't properly expose humidity data
# to Mainsail. This wrapper monkey-patches the sensor's get_status method
# to ensure both temperature and humidity are available in the status API.

import logging

def load_config(config):
    # Import and create the compiled aht20_f sensor
    try:
        from . import aht20_f as aht20_f_module
        sensor = aht20_f_module.load_config(config)
    except ImportError as e:
        raise config.error(f"Could not import aht20_f module: {e}")
    
    # Store the original get_status method if it exists
    original_get_status = getattr(sensor, 'get_status', None)
    
    # Create an enhanced get_status method that exposes humidity
    def enhanced_get_status(eventtime):
        status = {}
        
        # Try to get status from original method
        if original_get_status:
            status = original_get_status(eventtime)
        
        # Ensure we have temperature
        if 'temperature' not in status and hasattr(sensor, 'temperature'):
            status['temperature'] = round(sensor.temperature, 2)
        
        # Add humidity if available but not in status
        if 'humidity' not in status and hasattr(sensor, 'humidity'):
            status['humidity'] = round(sensor.humidity, 1)
        
        return status
    
    # Replace the get_status method with our enhanced version
    sensor.get_status = enhanced_get_status
    
    # Return the patched sensor
    return sensor


