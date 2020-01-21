import os
import time
import uuid 
import pytesseract
from abc import ABCMeta, abstractmethod
from PIL import Image 
from loguru import logger

from models import session
from models import Person, Picture

class ProfileBase(metaclass=ABCMeta):
    
    device = None
    source_name = None
    package_name = None
    crops = {
        'main_image': (None, None),
        'raw': (None, None),
    }
    initial_tap_coords = (None, None, )
    reset_tap_coords = (None, None, )

    def launch_app(self):
        return self.device.shell('am start -n {}'.format(self.package_name)) 
    
    def get_to_ready_state(self):
        logger.info('sleeping for 1 seconds...')
        time.sleep(1)
        try:
            self.device.shell('input tap {} {}'.format(
                self.initial_tap_coords[0],
                self.initial_tap_coords[1],
            ))
            time.sleep(1)
            return True
        except:
            return False
    
    @abstractmethod
    def is_stop_condition(self):
        pass
    
    @abstractmethod
    def process_stop_condition(self):
        pass

    # @abstractmethod
    def collect_data(self):
        self.device.shell("screencap -p /sdcard/screen.png")
        _uuid = self.generate_uuid()
        main_image_path = "media/{}.png".format(_uuid)
        crop_image_path = "media/{}_crop.jpg".format(_uuid)
        raw_image_path = "media/{}_raw.png".format(_uuid)

        self.device.pull("/sdcard/screen.png", main_image_path)

        with Image.open(main_image_path) as main_image:
            
            main_image_crop = main_image.crop((
                0, 
                self.crops['main_image'][0], 
                1080, 
                self.crops['main_image'][1],
            ))
            main_image_crop_jpg = main_image_crop.convert('RGB')
            main_image_crop_jpg.save(crop_image_path)

            raw_crop = main_image.crop((
                0, 
                self.crops['raw'][0], 
                1080, 
                self.crops['raw'][1],
            ))

            raw_crop.save(raw_image_path)
        # convert main_image
        raw_text = pytesseract.image_to_string(Image.open(raw_image_path))
        logger.debug(raw_text)
        os.remove(raw_image_path)
        # initing db row for Person
        person = Person(
            gender='female',
            raw=raw_text,
            result=True,
            source_name=self.source_name,
        )
        session.add(person)
        session.commit()

        # adding row for picture
        picture = Picture(
            person_id=person.id,
            _uuid=str(_uuid),
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
        self.device.shell('input tap {} {}'.format(
            self.reset_tap_coords[0],
            self.reset_tap_coords[1],
        ))
        logger.info('waiting to reset...')
        time.sleep(1)
        self.get_to_ready_state()


    
    def set_device(self, device):
        self.device = device

    def generate_uuid(self):
        return uuid.uuid1()

# class 