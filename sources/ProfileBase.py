from abc import ABCMeta, abstractmethod

class ProfileBase(metaclass=ABCMeta):
    
    @abstractmethod
    def launch_app(self):
        pass
    
    @abstractmethod
    def get_to_ready_state(self):
        pass
    
    @abstractmethod
    def check_stop_condition(self):
        pass
    
    @abstractmethod
    def process_stop_condition(self):
        pass

    @abstractmethod
    def collect_data(self):
        pass

        @abstractmethod
        def get_pictures(self):
            pass

        @abstractmethod
        def get_raw(self):
            pass

    @abstractmethod
    def reset(self):
        pass


