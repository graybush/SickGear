import warnings
warnings.filterwarnings('ignore', module=r'.*fuz.*', message='.*Sequence.*')
warnings.filterwarnings('ignore', module=r'.*connectionpool.*', message='.*certificate verification.*')
warnings.filterwarnings('ignore', module=r'.*zoneinfo.*', message='.*no such file.*')

import unittest
import test_lib as test
import os.path
import datetime
from lib.dateutil import tz
import sickgear
from sickgear import network_timezones, helpers
# noinspection PyPep8Naming
import encodingKludge as ek


class NetworkTimezoneTests(test.SickbeardTestDBCase):
    @classmethod
    def tearDownClass(cls):
        super(NetworkTimezoneTests, cls).tearDownClass()
        cls.remove_zoneinfo()
        try:
            os.rmdir(sickgear.ZONEINFO_DIR)
        except (BaseException, Exception):
            pass

    @classmethod
    def setUpClass(cls):
        super(NetworkTimezoneTests, cls).setUpClass()
        os.makedirs(sickgear.ZONEINFO_DIR)
        cls.remove_zoneinfo()

    @classmethod
    def remove_zoneinfo(cls):
        # delete all existing zoneinfo files
        for (path, dirs, files) in ek.ek(os.walk, helpers.real_path(sickgear.ZONEINFO_DIR)):
            for filename in files:
                if filename.endswith('.tar.gz'):
                    file_w_path = ek.ek(os.path.join, path, filename)
                    try:
                        ek.ek(os.remove, file_w_path)
                    except (BaseException, Exception):
                        pass

    def test_timezone(self):
        network_timezones.update_network_dict()
        network_timezones.SG_TIMEZONE = tz.gettz('CET', zoneinfo_priority=True)
        d = datetime.date(2018, 9, 2).toordinal()
        t = 'Monday 9:00 PM'
        network = 'NBC'
        r = network_timezones.parse_date_time(d, t, network)
        local_date = datetime.datetime(2018, 9, 3, 3, 0, 0).replace(tzinfo=tz.gettz('CET', zoneinfo_priority=True))
        self.assertEqual(r, local_date)


if '__main__' == __name__:
    suite = unittest.TestLoader().loadTestsFromTestCase(NetworkTimezoneTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
