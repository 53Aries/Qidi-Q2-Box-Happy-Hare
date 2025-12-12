# AHT20_F Humidity Patch for Mainsail
#
# The compiled aht20_f.so module doesn't expose humidity in get_status()
# This patches the module's class to include humidity data

import logging

def load_config(config):
    # Import the compiled aht20_f module
    try:
        from . import aht20_f as aht20_f_module
    except ImportError as e:
        raise config.error(f"Could not import aht20_f module: {e}")
    
    # Get the sensor class from the module
    sensor_class = None
    for attr_name in dir(aht20_f_module):
        attr = getattr(aht20_f_module, attr_name)
        if isinstance(attr, type) and attr_name not in ['load_config']:
            sensor_class = attr
            break
    
    if sensor_class is None:
        raise config.error("Could not find sensor class in aht20_f module")
    
    # Store the original get_status method
    original_get_status = getattr(sensor_class, 'get_status', None)
    
    # Create patched get_status that includes humidity
    def patched_get_status(self, eventtime):
        status = {}
        
        # Call original if it exists
        if original_get_status:
            try:
                status = original_get_status(self, eventtime)
            except:
                pass
        
        # Add temperature if available
        if 'temperature' not in status:
            if hasattr(self, 'temperature'):
                status['temperature'] = round(float(self.temperature), 2)
            elif hasattr(self, 'temp'):
                status['temperature'] = round(float(self.temp), 2)
        
        # Add humidity if available
        if 'humidity' not in status:
            if hasattr(self, 'humidity'):
                status['humidity'] = round(float(self.humidity), 1)
            elif hasattr(self, 'hum'):
                status['humidity'] = round(float(self.hum), 1)
        
        return status
    
    # Patch the class method
    sensor_class.get_status = patched_get_status
    
    # Now register the patched sensor factory
    pheater = config.get_printer().lookup_object("heaters")
    pheater.add_sensor_factory("AHT20_F", sensor_class)




