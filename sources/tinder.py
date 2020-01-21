from loguru import logger
from .profile_base import ProfileBase

class Tinder(ProfileBase):

    source_name = 'tinder'
    package_name = '\'com.tinder/.activities.MainActivity\''
    crops = {
        'main_image': [57, 1380],
        'raw': [1400, 1980],
    }
    initial_tap_coords = (540, 1826, )
    reset_tap_coords = (723, 2056, )

    
    def is_stop_condition(self):
        return False
    
    def process_stop_condition(self):
        pass

    # def collect_data(self):

        
    #     # crop to dimensions
    #     pass

    # def reset(self):
    #     pass