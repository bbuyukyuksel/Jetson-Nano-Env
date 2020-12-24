import time
import i2c
import crcmod.predefined

'''
Requirements
sudo apt-get install crcmod
sudo apt-get install i2c-tools

'''

class Omrond6t(object):
    def __init__(self, bus=1, omronAddress=0x0A, arraySize=16):
        self.MAX_RETRIES = 5
        self.omronAddress = omronAddress
        self.arraySize = arraySize

        self.BUFFER_LENGTH = (arraySize * 2) + 3 # data buffer size
        
        self.CRC_ERROT_BIT = 0x04                # the third bit: 0b0000 0100
        self.CRC = 0xA4 / (16/arraySize)

        time.sleep(0.1)

        self.retries = 0
        self.result = 0

        self.handle = i2c.I2C(omronAddress, bus)
        for i in range(0, self.MAX_RETRIES):
            time.sleep(0.05)
            try:
                self.handle.write([0x4C])
            except:
                print("Handle error!")
                self.retries += 1
            break
    
    def close(self):
        self.handle.close()

    def read(self):
        self.temperature_data_raw = [0  ]*self.BUFFER_LENGTH
        self.temperature          = [0.0]*self.arraySize
        self.values               = [0  ]*self.BUFFER_LENGTH

        retries = 0
        for i in range(self.MAX_RETRIES):
            time.sleep(0.05)
            try:
                self.temperature_data_raw =  self.handle.read(self.BUFFER_LENGTH)
                self.bytes_read = len(self.temperature_data_raw)
                # Handle i2c error transmissions
                if self.bytes_read != self.temperature_data_raw:
                    self.retries += 1

                if self.bytes_read == self.BUFFER_LENGTH:
                    # Good Byte, check PEC
                    t = (self.temperature_data_raw[1] << 8) | self.temperature_data_raw[0]
                    self.tPATc = float(t)/10

                    # Convert raw values to temperature
                    index = 0
                    for i in range(2, self.BUFFER_LENGTH-2, 2):
                        self.temperature[index] = float((self.temperature_data_raw[i+1] << 8) | self.temperature_data_raw[i])/10
                        index += 1

                    # Calculate the CRC error check code
                    '''
                    # PEC (packer error code) byte is appended at the end of each transaction.
                    # The byte is calculated as CRC-8 checksum,
                    # calculated over the entire message including the address and read/write bit.
                    # The polynomial used is x8+x2+x+1 (the CRC-8-ATM HEC algorithm, initialized to zero)
                    '''

                    self.crc8_func = crcmod.predefined.mkCrcFun('crc-8')

                    for i in range(self.bytes_read):
                        self.values[i] = self.temperature_data_raw[i]
                    
                    self.string = "".join(chr(i) for i in self.values)
                    self.crc = self.crc8_func(self.string.encode())

                    if crc != self.CRC:
                        print("Omron CRC Error!")
                        self.retries += 1
                        self.bytes_read = 0
                    else:
                        break
            except:
                pass
        return self.temperature

if __name__ == '__main__':
    import datetime
    print("Test code is running...")
    dev_omrond6t = Omrond6t(bus=1, omronAddress=0x0A, arraySize=8)

    #Control
    MAX = 20
    for i in range(20):
        temperatures = dev_omrond6t.read()
        print(str(i).rjust(4, ' ') ,datetime.datetime.now(), end=' >> ')
        for temperature in temperatures:
            print("{:<5}".format(temperature), end='#')
        print('', end='\r')
    
    dev_omrond6t.close()
    print("\n", "Finished.")

