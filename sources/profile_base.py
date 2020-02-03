import os
import time
import uuid 
import pytesseract
from abc import ABCMeta, abstractmethod
from PIL import Image 
from loguru import logger

from models import session
from models import Person, Picture
# from constants import PIXEL_MAP_SCALE

class ProfileBase(metaclass=ABCMeta):
    
    device = None
    source_name = None
    package_name = None
    crops = {
        'main_image': (None, None),
        'raw': (None, None),
        'is_ad': (None, None, None, None),
        'stop_check': (None, None, None, None),
    }
    initial_tap_coords = (None, None, )
    reset_tap_coords = (None, None, )
    bio_swipe_coords = {
        'from': None,
        'to': None,
        'duration': None
    }
    remove_these = []
    stop_condition_check_texts = []
    screen_resolution_width = None
    screen_resolution_height = None

    def __init__(self):
        pass

    def launch_app(self):
        return self.device.shell('am start -n {}'.format(self.package_name)) 
    
    def get_to_ready_state(self):
        logger.info('sleeping for 5 seconds...')
        time.sleep(5)
        # while self.is_ad():
        #     time.sleep(1)
        try:
            cmd = 'input tap {} {}'.format(
                int(self.screen_resolution_height * (self.initial_tap_coords[0])), 
                int(self.screen_resolution_height * (self.initial_tap_coords[1])), 
            )
            logger.debug(cmd)
            self.device.shell(cmd)
            time.sleep(1)
            return True
        except Exception as e:
            logger.critical('!! get_to_ready_state')
            logger.error(str(e))
            return False
    
    # @abstractmethod
    def is_stop_condition(self):
        self.tmp_image_path = "media/tmp.png"
        self.device.shell("screencap -p /sdcard/screen.png")
        self.device.pull("/sdcard/screen.png", self.tmp_image_path)
        with Image.open(self.tmp_image_path) as tmp_image:
            # logger.warning(tuple(int(self.screen_resolution_width * _) for _ in self.crops['stop_check']) )
            tmp_image_crop = tmp_image.crop(
                # tuple(int(self.screen_resolution_width * _) for _ in self.crops['stop_check']) ,
                    (
                        int(self.screen_resolution_width * self.crops['stop_check'][0]),
                        int(self.screen_resolution_height * self.crops['stop_check'][1]),
                        int(self.screen_resolution_width * self.crops['stop_check'][2]),
                        int(self.screen_resolution_height * self.crops['stop_check'][3]),
                    )
                )
            tmp_image_crop.save(self.tmp_image_path)

        raw_text = pytesseract.image_to_string(tmp_image_crop)
        logger.debug(raw_text)
        for stop_condition_check_text in self.stop_condition_check_texts:
            if stop_condition_check_text.lower() in raw_text.lower():
                return True
        self._uuid = str(self.generate_uuid()) + '_' + str(int(time.time()))
        self.main_image_path = "media/{}.png".format(self._uuid)
        self.crop_image_path = "media/{}_crop.jpg".format(self._uuid)
        self.tmp_image_path = "media/{}_tmp.png".format(self._uuid)
        self.raw_image_path = "media/{}_raw.png".format(self._uuid)        
        self.get_to_ready_state()
        return False
    
    @abstractmethod
    def process_stop_condition(self):
        pass

    # @abstractmethod
    def collect_data(self):
        self.device.shell("screencap -p /sdcard/screen.png")
        self.device.pull("/sdcard/screen.png", self.main_image_path)

        with Image.open(self.main_image_path) as main_image:
            
            main_image_crop = main_image.crop((
                0, 
                int(self.screen_resolution_height * (self.crops['main_image'][0])), 
                self.screen_resolution_width, 
                int(self.screen_resolution_height * (self.crops['main_image'][1])), 
            ))
            main_image_crop_jpg = main_image_crop.convert('RGB')
            main_image_crop_jpg.save(self.crop_image_path)

        # scroll down to bio # TINDER SPECIFIC, move to child class
        self.get_bio_page_ready()
        self.device.shell("screencap -p /sdcard/screen.png")
        self.device.pull("/sdcard/screen.png", self.tmp_image_path)
        with Image.open(self.tmp_image_path) as tmp_image:
            raw_crop = tmp_image.crop((
                0, 
                int(self.screen_resolution_height * (self.crops['raw'][0])), 
                self.screen_resolution_width, 
                int(self.screen_resolution_height * (self.crops['raw'][1])), 
            ))

            raw_crop.save(self.raw_image_path)
        # convert main_image
        raw_text = pytesseract.image_to_string(Image.open(self.raw_image_path))
        # logger.debug(raw_text)
        clean_data = self.cleanse_data(raw_text)
        logger.debug(clean_data)
        os.remove(self.main_image_path)
        os.remove(self.raw_image_path)
        os.remove(self.tmp_image_path)
        # initing db row for Person
        person = Person(
            gender='female',
            raw=clean_data,
            result=True,
            source_name=self.source_name,
        )
        session.add(person)
        session.commit()

        # adding row for picture
        picture = Picture(
            person_id=person.id,
            _uuid=str(self._uuid),
        )
        session.add(picture)
        session.commit()



        # @abstractmethod
        # def get_pictures(self):
        #     pass

        # @abstractmethod
        # def get_raw(self):
        #     pass

    def reset(self):
        cmd = 'input tap {} {}'.format(
            int(self.screen_resolution_width * (self.reset_tap_coords[0])), 
            int(self.screen_resolution_height * (self.reset_tap_coords[1])), 
        )
        logger.debug(cmd)
        self.device.shell(cmd)
        logger.info('waiting to reset...')
        time.sleep(1)
        # self.get_to_ready_state()

    def is_ad(self):
        self.device.shell("screencap -p /sdcard/screen.png")
        # self.tmp_image_path = "media/{}_tmp.png".format(_uuid)
        self.device.pull("/sdcard/screen.png", self.tmp_image_path)
        # print(int(self.screen_resolution_height * (self.crops['is_ad'][0])), 
        #         int(self.screen_resolution_height * (self.crops['is_ad'][1])), 
        #         int(self.screen_resolution_height * (self.crops['is_ad'][2])), 
        #         int(self.screen_resolution_height * (self.crops['is_ad'][3])), )
        with Image.open(self.tmp_image_path) as tmp_image:
            raw_crop = tmp_image.crop((
                int(self.screen_resolution_height * (self.crops['is_ad'][0])), 
                int(self.screen_resolution_height * (self.crops['is_ad'][1])), 
                int(self.screen_resolution_height * (self.crops['is_ad'][2])), 
                int(self.screen_resolution_height * (self.crops['is_ad'][3])), 
            ))

            raw_crop.save(self.tmp_image_path)
        # convert main_image
        raw_text = pytesseract.image_to_string(Image.open(self.tmp_image_path))
        logger.debug(raw_text)
        return True


    
    def set_device(self, device):
        self.device = device

    def set_user(self, user, PIXEL_MAP_SCALE):
        self.screen_resolution_width = user.screen_resolution_width * (PIXEL_MAP_SCALE[user.screen_resolution_width])
        self.screen_resolution_height = user.screen_resolution_height * (PIXEL_MAP_SCALE[user.screen_resolution_height])

    def generate_uuid(self):
        return uuid.uuid1()

    def cleanse_data(self, raw_text):
        for _ in self.remove_these:
            raw_text = raw_text.replace(_, '')
        # remove \ns
        return '\n'.join([_ for _ in raw_text.split('\n') if len(_) > 0])

    def exit_app(self):
        # for _ in range(5):
        #     cmd = 'input keyevent 4'
        #     self.device.shell(cmd)
        #     time.sleep(0.1)
        cmd = 'input keyevent KEYCODE_APP_SWITCH'
        self.device.shell(cmd)
        time.sleep(0.1)
        cmd = 'input touchscreen swipe {} {} {} {} 100'.format(
            int(self.screen_resolution_width / 2),
            int(self.screen_resolution_height * (self.bio_swipe_coords['from'] - 0.1)), 
            int(self.screen_resolution_width / 2),
            int(self.screen_resolution_height * (self.bio_swipe_coords['to'] - 0.2)), 
        )
        logger.debug(cmd)
        self.device.shell(cmd)
        

    def get_bio_page_ready(self):
        cmd = 'input touchscreen swipe {} {} {} {}'.format(
            int(self.screen_resolution_width / 2),
            int(self.screen_resolution_height * (self.bio_swipe_coords['from'])), 
            int(self.screen_resolution_width / 2),
            int(self.screen_resolution_height * (self.bio_swipe_coords['to'])), 
        )
        # logger.debug(cmd)
        self.device.shell(cmd)

# class 