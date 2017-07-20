import datetime
import logging


# Device Class Definition *****************************************************
class Device(object):
    """ Class used to define the objects and methods associated with a physical
    device that will be interfaced to/from this application """
    def __init__(self, logger=None, **kwargs):
        # Configure logger
        self.logger = logger or logging.getLogger(__name__)
        self._name = str()
        self._devtype = str()
        self._address = str()
        self._status = str()
        self._status_mem = str()
        self._last_seen = datetime.datetime
        self._cmd = str()
        self._rule = str()
        # Process input variables if present
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "name":
                    self.name = value
                if key == "devtype":
                    self.devtype = value
                if key == "address":
                    self.address = value
                if key == "status":
                    self.status = value
                if key == "last_seen":
                    self.last_seen = value
                if key == "cmd":
                    self.cmd = value
                if key == "rule":
                    self.rule = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = str(value)

    @property
    def devtype(self):
        return self._devtype

    @devtype.setter
    def devtype(self, value):
        self._devtype = str(value)

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = str(value)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = str(value)

    @property
    def status_mem(self):
        return self._status_mem

    @status_mem.setter
    def status_mem(self, value):
        self._status_mem = str(value)

    @property
    def last_seen(self):
        return self._last_seen

    @last_seen.setter
    def last_seen(self, value):
        if isinstance(value, datetime.datetime):
            self._last_seen = value

    @property
    def cmd(self):
        return self._cmd

    @cmd.setter
    def cmd(self, value):
        self._cmd = str(value)

    @property
    def rule(self):
        return self._rule

    @rule.setter
    def rule(self, value):
        self._rule = str(value)