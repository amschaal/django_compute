class JobAlreadyRunException(Exception):
    """This job has already been run"""
    pass

class JobTypeException(Exception):
    """Invalid job type"""
    pass

class JobTerminationException(Exception):
    """Job cannot be terminated"""
    pass