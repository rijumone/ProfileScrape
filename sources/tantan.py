from loguru import logger
from .profile_base import ProfileBase

class Tantan(ProfileBase):

    source_name = 'tantan'
    package_name = '\'com.p1.mobile.putong/.ui.splash.SplashProxyAct\''
    crops = {
        'main_image': [57, 1130],
        'raw': [1180, 1980],
    }
    initial_tap_coords = (540, 1080, )
    reset_tap_coords = (965, 2042, )

    
    def is_stop_condition(self):
        return False
    
    def process_stop_condition(self):
        pass

    # def collect_data(self):

        
    #     # crop to dimensions
    #     pass

    # def reset(self):
    #     pass