import shutil
import os
import subprocess
import tempfile
import pymongo
import time
from pymongo import MongoClient
from arctic import Arctic

class MongoTemporaryInstance(object):

    def __init__(self,MONGODB_TEST_PORT):
        self._tmpdir = tempfile.mkdtemp()
        self._process = subprocess.Popen(['mongod', '--bind_ip', 'localhost',
                                          '--port', str(MONGODB_TEST_PORT),
                                          '--dbpath', self._tmpdir,
                                          '--nojournal', '--nohttpinterface',
                                          '--noauth', '--smallfiles',
                                          '--syncdelay', '0',
                                          '--maxConns', '10',
                                          '--nssize', '1', ],
                                         stdout=open(os.devnull, 'wb'),
                                         stderr=subprocess.STDOUT)

        # XXX: wait for the instance to be ready
        #      Mongo is ready in a glance, we just wait to be able to open a
        #      Connection.
        for i in range(3):
            time.sleep(0.1)
            try:
                client = MongoClient('localhost',MONGODB_TEST_PORT)
                print(client.server_info())
                # self.arctic = Arctic(MongoClient('localhost',MONGODB_TEST_PORT))

            except pymongo.errors.ConnectionFailure:
                continue
            else:
                break
        else:
            assert False, 'Cannot connect to the mongodb test instance'


    def shutdown(self):
        if self._process:
            self._process.terminate()
            self._process.wait()
            self._process = None
            shutil.rmtree(self._tmpdir, ignore_errors=True)


