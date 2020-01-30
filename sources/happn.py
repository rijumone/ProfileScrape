import time
from loguru import logger
from .profile_base import ProfileBase

class Happn(ProfileBase):

    source_name = 'happn'
    package_name = '\'com.ftw_and_co.happn/.ui.splash.SplashActivity\''
    crops = {
        'main_image': (
            0.025, 
            0.90,
            ),
        'raw': (
            0.2, 
            0.916666667,
            ),
        'stop_check': (
            0.15, 
            0.0, 
            0.85, 
            0.4,
            )
    }
    initial_tap_coords = (
        0.25, 
        0.50, 
        )
    reset_tap_coords = (
        0.694444444, 
        0.8671875, 
        )
    bio_swipe_coords = {
        'from': 0.78125,
        'to': 0.6,
        'duration': None
    }

    stop_condition_check_texts = [
        'do you want unlimited likes',
        'No one in sight?',
        'Explore your Map to find the happners you\'ve Liked or go out fora',
        'stroll and cross paths with some fresh faces!',
        ]
    
    
    # def is_stop_condition(self):
    #     return False
    
    def process_stop_condition(self):
        pass

    def get_to_ready_state(self):
        logger.info('sleeping for 1.5 seconds...')
        time.sleep(1.5)
        return True