from loguru import logger
from .profile_base import ProfileBase

class Tinder(ProfileBase):

    source_name = 'tinder'
    package_name = '\'com.tinder/.activities.MainActivity\''
    crops = {
        'main_image': (
            0.026388889, 
            0.72,
            ),
        'raw': (
            0.2, 
            0.916666667,
            ),
        'stop_check': (
            0.2, 
            0.0, 
            0.8, 
            0.3,
            ),
        'is_ad': (
            0.305555556, 
            0.78125, 
            0.694444444, 
            0.8671875,
            ),
    }
    initial_tap_coords = (
        0.25, 
        0.84537037, 
        )
    reset_tap_coords = (
        0.694444444, 
        0.951851852, 
        )
    bio_swipe_coords = {
        'from': 0.78125,
        'to': 0.6,
        'duration': None
    }
    remove_these = ['SEE WHAT A FRIEND THINKS', ]
    stop_condition_check_texts = [
        'Get Tinder Plus',
    ]
    tmp_image_path = None

    
    # def is_stop_condition(self):
    #     return False
    
    def process_stop_condition(self):
        pass

    
    # def collect_data(self):

        
    #     # crop to dimensions
    #     pass

    # def reset(self):
    #     pass