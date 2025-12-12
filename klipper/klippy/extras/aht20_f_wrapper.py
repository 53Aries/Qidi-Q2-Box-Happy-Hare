# AHT20_F Humidity Wrapper for Mainsail
#
# The compiled aht20_f.so module doesn't properly expose humidity data
# to Mainsail. This wrapper intercepts sensor creation and patches it
# to ensure both temperature and humidity are available in the status API.

import logging

class AHT20F_Wrapper:
    def __init__(self, config):
        # Import and create the actual aht20_f sensor
        try:
            from . import aht20_f as aht20_f_module
            # Create the real sensor - this will register itself
            if hasattr(aht20_f_module, 'AHT20_F'):
                self.sensor = aht20_f_module.AHT20_F(config)
            else:
                raise config.error("aht20_f module has unexpected structure")
        except ImportError as e:
            raise config.error(f"Could not import aht20_f module: {e}")
        
        # Store original get_status if it exists
        self.original_get_status = getattr(self.sensor, 'get_status', None)
    
    def get_status(self, eventtime):
        status = {}
        
        # Get status from original sensor
        if self.original_get_status:
            status = self.original_get_status(eventtime)
        
        # Ensure temperature is included
        if 'temperature' not in status and hasattr(self.sensor, 'temperature'):
            status['temperature'] = round(self.sensor.temperature, 2)
        
        # Add humidity if available
        if 'humidity' not in status and hasattr(self.sensor, 'humidity'):
            status['humidity'] = round(self.sensor.humidity, 1)
        
        return status
    
    # Delegate all other method calls to the actual sensor
    def __getattr__(self, name):
        return getattr(self.sensor, name)

def load_config(config):
    # Register sensor factory that creates our wrapper
    pheater = config.get_printer().lookup_object("heaters")
    pheater.add_sensor_factory("AHT20_F", AHT20F_Wrapper)



