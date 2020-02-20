import time
from loguru import logger
from .profile_base import ProfileBase

class Woo(ProfileBase):

    source_name = 'woo'
    package_name = '\'com.u2opia.woo/.activity.SplashActivity\''
    crops = {
        'main_image': (
            0.026388889, 
            0.8,
            ),
        'raw': (
            0.1, 
            0.916666667,
            ),
        'stop_check': (
            0.0, 
            0.0, 
            1.0, 
            1.0,
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
        'from': 0.65,
        'to': 0.35,
        'duration': None
    }
    remove_these = ['SEE WHAT A FRIEND THINKS', ]
    stop_condition_check_texts = [
        'Brand\'s Tags',
        'All out of likes',
        'Get more likes in',
        '#Increase visibility',
        'who visit your profile.',
        'your profile will increase your visibility',
        'by upto 20 times. Get unlimited access to all',
    ]
    tmp_image_path = None

    
    # def is_stop_condition(self):
    #     return False
    
    def process_stop_condition(self):
        pass

    # def exit_app(self):
    #     cmd = 'input tap {} {}'.format(
    #         int(self.screen_resolution_width * 0.5236), 
    #         int(self.screen_resolution_height * 0.6476), 
    #     )
    #     logger.debug(cmd)
    #     self.device.shell(cmd)
    #     for _ in range(4):
    #         cmd = 'input keyevent 4'
    #         self.device.shell(cmd)
    #         time.sleep(0.1)

    def get_bio_page_ready(self):
        for _ in range(3):
            cmd = 'input touchscreen swipe {} {} {} {}'.format(
                int(self.screen_resolution_width / 2),
                int(self.screen_resolution_height * (self.bio_swipe_coords['from'])), 
                int(self.screen_resolution_width / 2),
                int(self.screen_resolution_height * (self.bio_swipe_coords['to'])), 
            )
            # logger.debug(cmd)
            self.device.shell(cmd)
