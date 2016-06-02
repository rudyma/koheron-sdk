#! /usr/bin/python

import requests
import time

class InstrumentManager:
    def __init__(self, ip, port=80):
        self.port = port
        self.url = 'http://' + ip + ':' + str(port)

    def set_ip(self, ip):
        self.url = 'http://' + ip + ':' + str(self.port)

    def get_bistream_id(self):
        r = requests.get(self.url + '/api/bitstream_id')
        return r.text

    def ping(self):
        r = requests.get(self.url + '/api/ping')
        
    def deploy_remote_instrument(self, name, version):
        """ Deploy a remotely available instrument. """
        zip_filename = name + '-' + version + '.zip'
        r = requests.get(self.url + '/api/deploy/remote/' + zip_filename)

    def deploy_local_instrument(self, name, version):
        """ Deploy a locally available instrument
            Return 0 on success, -1 else
        """
        zip_filename = name + '-' + version + '.zip'
        print('Deploying ' + zip_filename)
        try:
            r = requests.get(self.url + '/api/deploy/local/' + zip_filename)
            return int(r.text.split('status:')[1].strip())
        except Exception as e: 
            print("[error] " + str(e))
            return -1

    def remove_local_instrument(self, name, version):
        zip_filename = name + '-' + version + '.zip'
        r = requests.get(self.url + '/api/remove/local/' + zip_filename)
        return r.text

    def get_local_instruments(self):
        try:
            r = requests.get(self.url + '/api/get_local_instruments')
            return r.json()
        except Exception as e: 
            print("[error] " + str(e))
            return {}

    def get_current_instrument(self):
        try:
            r = requests.get(self.url + '/api/get_current_instrument')
            return r.json()
        except Exception as e: 
            print("[error] " + str(e))
            return {}

    def install_instrument(self, instrument_name, always_restart=False):
        if not always_restart:
            # Don't restart the instrument if already launched
            current_instrument = self.get_current_instrument()
            if current_instrument['name'] == instrument_name:
                return

        instruments = self.get_local_instruments()
        if instruments:
            for name, shas in instruments.items():
                if name == instrument_name and len(shas) > 0:
                    if self.deploy_local_instrument(name, shas[0]) < 0:
                        raise RuntimeError("Instrument " + instrument_name + " launch failed.")
                    return
        raise ValueError("Instrument " + instrument_name + " not found")

if __name__ == "__main__":
    host = os.getenv(HOST, '192.168.1.100')
    name = os.getenv(NAME, '')
    im = InstrumentManager(host)
    im.install_instrument(name)
    print('bitstream id = {}'.format(http.get_bistream_id()))
