from django.utils.module_loading import import_string
from django.conf import settings


class BaseCallback:
    id = 'callback_id'
    description = 'Callback description'
    aggregable = False
    @staticmethod
    def run(**kwargs):
        assert kwargs.has_key('job')
        assert kwargs.has_key('data')
        pass

def get_callback(callback_id):
    callback_dictionaries = getattr(settings,'COMPUTE_JOB_CALLBACKS')
    for callback_dictionary in callback_dictionaries:
        callbacks = import_string(callback_dictionary)
        if callbacks.has_key(callback_id):
            return callbacks[callback_id]
    return False