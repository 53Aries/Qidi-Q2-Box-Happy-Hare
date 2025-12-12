# AHT20_F Humidity Wrapper for Mainsail
#
# The compiled aht20_f.so module doesn't properly expose humidity data
# to Mainsail. This wrapper ensures both temperature and humidity are
# available in the status API.

import logging

class AHT20F_Sensor:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.name = config.get_name().split()[-1]
        
        # Import and initialize the compiled aht20_f module
        try:
            from . import aht20_f as aht20_f_module
            # The compiled module should have a class or factory function
            # We need to create an instance
            if hasattr(aht20_f_module, 'AHT20_F'):
                self.sensor = aht20_f_module.AHT20_F(config)
            elif hasattr(aht20_f_module, 'load_config'):
                self.sensor = aht20_f_module.load_config(config)
            else:
                raise config.error("aht20_f module has unexpected structure")
        except ImportError as e:
            raise config.error(f"Could not import aht20_f module: {e}")
        
        # Register this wrapper to provide status
        self.printer.add_object("aht20_f " + self.name, self)
        
        self.temperature = 0.
        self.humidity = 0.
        
    def get_status(self, eventtime):
        # Try to get data from the underlying sensor
        if hasattr(self.sensor, 'get_status'):
            sensor_status = self.sensor.get_status(eventtime)
            if 'temperature' in sensor_status:
                self.temperature = sensor_status['temperature']
            if 'humidity' in sensor_status:
                self.humidity = sensor_status['humidity']
        
        # Also check if sensor has temperature/humidity attributes directly
        if hasattr(self.sensor, 'temperature'):
            self.temperature = self.sensor.temperature
        if hasattr(self.sensor, 'humidity'):
            self.humidity = self.sensor.humidity
            
        # Return both temperature and humidity for Mainsail
        return {
            'temperature': round(self.temperature, 2),
            'humidity': round(self.humidity, 1),
        }
    
    # Delegate all other method calls to the underlying sensor
    def __getattr__(self, name):
        return getattr(self.sensor, name)

def load_config(config):
    # Register sensor factory
    pheater = config.get_printer().lookup_object("heaters")
    pheater.add_sensor_factory("AHT20_F", AHT20F_Sensor)

