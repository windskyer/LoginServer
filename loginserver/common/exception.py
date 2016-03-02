import sys
import six

class Error(Exception):
    """Base class for cfg exceptions."""

    def __init__(self, msg=None):
        self.msg = msg                  

    def __str__(self):       
        return self.msg 

class LoginserverError(Exception):
    msg_fmt = ("An unknown exception occurred.")
    code = 500
    headers = {}
    safe = False
    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs
        if 'code' not in kwargs:
            try:
                self.kwargs['code'] = self.code
            except AttributeError:
                pass

        if not message:
            try:
               message = self.msg_fmt % kwargs
            except Exception:
                exc_info = sys.exc_info()
                LOG.exception('Exception in string format operation')
                for name, value in six.iteritems(kwargs):
                    LOG.error("%s: %s" % (name, value))
                six.reraise(*exc_info)

        self.message = message
        super(LoginserverError, self).__init__(message)
    
class LogConfigError(LoginserverError):
    msg_fmt = "Not Found %(binfile)s configfile"

class NoSuchOptError(LoginserverError):
    msg_fmt = "'module' object has no attribute %(key)s" 

class ConfigFileParseError(Error):
    """Raised if there is an error parsing a config file."""

    def __init__(self, config_file, msg):
        self.config_file = config_file
        self.msg = msg

    def __str__(self):
        return 'Failed to parse %s: %s' % (self.config_file, self.msg)
