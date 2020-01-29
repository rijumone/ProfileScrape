from loguru import logger
from .profile_base import ProfileBase

class Tantan(ProfileBase):

    source_name = 'tantan'
    package_name = '\'com.p1.mobile.putong/.ui.splash.SplashProxyAct\''
    crops = {
        'main_image': (
            0.027, 
            0.68,
            ),
        'raw': (
            0.2, 
            0.916666667,
            ),
        'stop_check': (
            0.0, 
            0.6, 
            0.99999, 
            0.9,
            )
    }
    initial_tap_coords = (
        0.25, 
        0.50, 
        )
    reset_tap_coords = (
        0.902777778, 
        0.9375, 
        )
    bio_swipe_coords = {
        'from': 0.78125,
        'to': 0.6,
        'duration': None
    }
    
    stop_condition_check_text = 'There is no one new around you'
    
    # def is_stop_condition(self):
    #     return False
    
    def process_stop_condition(self):
        pass

    # def collect_data(self):

        
    #     # crop to dimensions
    #     pass

    # def reset(self):
    #     pass