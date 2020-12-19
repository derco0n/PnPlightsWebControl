import smbus2

class relayeight():
    """Class for communicating with the relay-board"""
    #bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

    def __init__(self):
        self.DEVICE_ADDRESS = 0x38     #7 bit address (will be left shifted to add the read write bit)
        self.ALTERNATE_DEVICE_ADDRESS = 0x20     #7 bit address (will be left shifted to add the read write bit)

        self.RELAY8_INPORT_REG_ADD = 0x00
        self.RELAY8_OUTPORT_REG_ADD = 0x01
        self.RELAY8_POLINV_REG_ADD = 0x02
        self.RELAY8_CFG_REG_ADD = 0x03
        self.relayMaskRemap = [0x01, 0x04, 0x02, 0x08, 0x40, 0x10, 0x20, 0x80] 
        self.relayChRemap = [0, 2, 1, 3, 6, 4, 5, 7]


    def __relayToIO(self, relay):
        val = 0
        for i in range(0, 8):
            if (relay & (1 << i)) != 0:
                val = val + self.relayMaskRemap[i]
        # print("DBG_Relay2IO: " +str(val))  # DEBUG
        return val
    
    def __IOToRelay(self, iov):
        val = 0
        for i in range(0, 8):
            if (iov & self.relayMaskRemap[i]) != 0:
                val = val + (1<< i)
        # print("DBG_IO2Relay: " + str(val))  # DEBUG
        return val

    def __check(self, bus, add):
        cfg = bus.read_byte_data(add, self.RELAY8_CFG_REG_ADD)
        if(cfg != 0):
            bus.write_byte_data(add, self.RELAY8_CFG_REG_ADD, 0)
            bus.write_byte_data(add, self.RELAY8_OUTPORT_REG_ADD, 0)
        return bus.read_byte_data(add, self.RELAY8_INPORT_REG_ADD)


    def set_one(self, stack, relay, value):
        """Sets the state of a specific relay"""
        if stack < 0 or stack > 7:
            raise ValueError('Invalid stack level!') 
        stack = 0x07 ^ stack
        if relay < 1:
            raise ValueError('Invalid relay number!')
        if relay > 8:
            raise ValueError('Invalid relay number!')
        bus = smbus2.SMBus(1)	
        hwAdd =  self.DEVICE_ADDRESS + stack
        try:	
            oldVal = __check(bus, hwAdd)
        except Exception as e:
            hwAdd = self.ALTERNATE_DEVICE_ADDRESS + stack
            try:
                oldVal = self.__check(bus, hwAdd)
            except Exception as e:
                bus.close()
                raise ValueError('8-relay card not detected!')	
        oldVal = self.__IOToRelay(oldVal)
        try:
            #print(str(hwAdd))  # DEBUG
            if value == 0:
                oldVal = oldVal & (~(1 << (relay - 1)))
                oldVal = self.__relayToIO(oldVal)
                bus.write_byte_data(hwAdd, self.RELAY8_OUTPORT_REG_ADD, oldVal)
            else:
                oldVal = oldVal | (1 << (relay - 1))
                oldVal = self.__relayToIO(oldVal)
                bus.write_byte_data(hwAdd, self.RELAY8_OUTPORT_REG_ADD, oldVal)
        except Exception as e:
            bus.close()
            raise ValueError('Fail to write relay state value!')			
        bus.close()

            
    def set_all(self, stack, value):
        if stack < 0 or stack > 7:
            raise ValueError('Invalid stack level!')
        stack = 0x07 ^ stack  
        if value > 255 :
            raise ValueError('Invalid relay value!')
        if value < 0:
            raise ValueError('Invalid relay value!')
            
        bus = smbus2.SMBus(1)		
        hwAdd =  self.DEVICE_ADDRESS + stack
        try:	
            oldVal = self.__check(bus, hwAdd)
        except Exception as e:
            hwAdd = self.ALTERNATE_DEVICE_ADDRESS + stack
            try:
                oldVal = self.__check(bus, hwAdd)
            except Exception as e:
                bus.close()
                raise ValueError('8-relay card not detected!')	
        value = self.__relayToIO(value)
        try:
            # print(str(hwAdd))  # DEBUG
            bus.write_byte_data(hwAdd, self.RELAY8_OUTPORT_REG_ADD, value)
        except Exception as e:
            bus.close()
            raise ValueError('Fail to write relay state value!')			
        bus.close()
        
    def get_one(self, stack, relay):
        """Gets the state of a specific relay"""
        if stack < 0 or stack > 7:
            raise ValueError('Invalid stack level!')
        stack = 0x07 ^ stack  
        if relay < 1:
            raise ValueError('Invalid relay number!')
        if relay > 8:
            raise ValueError('Invalid relay number!')
        bus = smbus2.SMBus(1)
        hwAdd =  self.DEVICE_ADDRESS + stack
        try:	
            val = __check(bus, hwAdd)
        except Exception as e:
            hwAdd = self.ALTERNATE_DEVICE_ADDRESS + stack
            try:
                val = self.__check(bus, hwAdd)
            except Exception as e:
                bus.close()
                raise ValueError('8-relay card not detected!')
                
        val = self.__IOToRelay(val) 
        val = val & (1 << (relay - 1))
        bus.close()
        if val == 0:
            return 0
        else:
            return 1
        
    def get_all(self, stack):
        """Gets all"""
        if stack < 0 or stack > 7:
            raise ValueError('Invalid stack level!')
        stack = 0x07 ^ stack
        bus = smbus2.SMBus(1)
        hwAdd =  self.DEVICE_ADDRESS + stack
        try:	
            val = self.__check(bus, hwAdd)
        except Exception as e:
            hwAdd = self.ALTERNATE_DEVICE_ADDRESS + stack
            try:
                val = self.__check(bus, hwAdd)
            except Exception as e:
                bus.close()
                raise ValueError('8-relay card not detected!')		 
        
        val = self.__IOToRelay(val) 
        bus.close()
        return val