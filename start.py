__author__ = 'mailmeonriju@gmail.com'

import time
from loguru import logger
from models import *
from sources.tantan import Tantan
from constants import SOURCE_MAP, PIXEL_MAP_SCALE

from ppadb.client import Client as AdbClient

logger.add(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log.log'), rotation="10 MB", retention="10 days")

def main():
    
    
    # sources = session.query(Source).filter(Source.name=='tinder').all()
    # sources = session.query(Source).filter(Source.name=='happn').all()
    # sources = session.query(Source).filter(Source.name=='tantan').all()
    sources = session.query(
        Source
        ).filter(
            Source.is_active==True
            ).order_by(
            Source.call_order.asc()
            ).all()
    for source in sources:
        
        source_obj = SOURCE_MAP[source.name]()

        for user in session.query(User).filter(User.is_active==True).all():
            # log run to db
            run = Run(
                source_name=source.name,
                user_name=user.name,
            )
            # print(user)
            session.add(run)
            session.commit()
            source_obj.set_device(device=get_device(user.device_id))
            source_obj.set_user(user, PIXEL_MAP_SCALE)
            
            # launching app
            r = source_obj.launch_app()
            # print(r)
            if not source_obj.get_to_ready_state():
                continue

            while True:
                # check for stop condition
                if source_obj.is_stop_condition():
                    logger.debug('is_stop_condition for {}, exiting app...'.format(
                        source_obj.source_name
                    ))
                    source_obj.exit_app()
                    break
                # import pdb; pdb.set_trace()
                source_obj.collect_data()
                source_obj.reset()
                # time.sleep(5)
                # logger.info('sleeping for 5 seconds')
                


def get_device(device_id):
    client = AdbClient(host="127.0.0.1", port=5037)    
    return client.device(device_id)

if __name__ == '__main__':
    main()
