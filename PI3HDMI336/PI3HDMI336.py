import logging

# Default I2C address for the PI3HDMI336 (I2C_ADDR = 0)
PI3HDMI336_I2CADDR = 0x54

# Define the register
PI3HDMI336_REGISTER = 0x00
PI3HDMI336_OFFSET_BYTE0 = 0x00
PI3HDMI336_OFFSET_BYTE1 = 0x01
PI3HDMI336_OFFSET_BYTE2 = 0x02
PI3HDMI336_TOTAL_BYTES = 0x03

# Register bytes
PI3HDMI336_BYTE0_INPUT_PORT = (0x03 << 6)
PI3HDMI336_BYTE0_TMDS_OUTPUT_ENABLE = (0x01 << 5)
PI3HDMI336_BYTE0_HDP_INPUT = (0x01 << 4)
PI3HDMI336_BYTE0_HDP_OUTPUT_STAGE = (0x01 << 3)
PI3HDMI336_BYTE0_HDP_PORT_C = (0x01 << 2)
PI3HDMI336_BYTE0_HDP_PORT_B = (0x01 << 1)
PI3HDMI336_BYTE0_HDP_PORT_A = (0x01 << 0)


PI3HDMI336_BYTE1_RT_PORT_A = (0x01 << 7)
PI3HDMI336_BYTE1_RT_PORT_B = (0x01 << 6)
PI3HDMI336_BYTE1_RT_PORT_C = (0x01 << 5)
PI3HDMI336_BYTE1_5V_PORT_C = (0x01 << 4)
PI3HDMI336_BYTE1_5V_PORT_B = (0x01 << 3)
PI3HDMI336_BYTE1_5V_PORT_A = (0x01 << 2)
PI3HDMI336_BYTE1_INT_FLAG =  (0x01 << 1)
PI3HDMI336_BYTE1_DCC_CHANNEL = (0x01 << 0)

# TODO: define byte 3

PI3HDMI336_EQ_3DB = 0x00
PI3HDMI336_EQ_6DB = 0x01
PI3HDMI336_EQ_12DB = 0x02
PI3HDMI336_EQ_16DB = 0x03

class PI3HDMI336(object):
    PortA = 0
    PortB = 1
    PortC = 2
    """
        Class to interact with the PI3HDMI336 HDMI-switcher.
    """

    def __init__(self, address=PI3HDMI336_I2CADDR, i2c=None, **kwargs):
        """
        Initialize the device on the specified i2c address.
        :param address: the i2c address of the PI3HDMI336
        :param i2c:
        :param kwargs:
        """
        self._logger = logging.getLogger('PI3HDMI336.PI3HDMI336')
        if i2c is None:
            import Adafruit_GPIO.I2C as I2C
            i2c = I2C
        self._device = i2c.get_i2c_device(address, **kwargs)

    def get_input_port(self):
        """
        This function returns the current input port (byte 0, bit 6 & 7)
        :return: 0, 1 or 2 representing the ports A, B & C
                    -1 representing no port active
        """
        read = self._device.readRaw(PI3HDMI336_TOTAL_BYTES)
        result = int(read[PI3HDMI336_OFFSET_BYTE0] >> 6)
        assert 0 <= result <= 3
        if result == 3:
            return -1
        return result

    def get_tmds_output(self):
        """
        This function return the TMDS Output Enable bit
        :return: boolean
        """
        read = self._device.readRaw(PI3HDMI336_TOTAL_BYTES)
        return bool(read[PI3HDMI336_OFFSET_BYTE0] & PI3HDMI336_BYTE0_TMDS_OUTPUT_ENABLE != 0)

    def get_input_selection(self):
        """
        Returns the HPD input selection: 0, HPD_SINK or 1, I2C register setting from B0b[0:3]
        :return: 0 or 1
        """
        read = self._device.readRaw(PI3HDMI336_TOTAL_BYTES)
        return int(read[PI3HDMI336_OFFSET_BYTE0] & PI3HDMI336_BYTE0_HDP_INPUT != 0)

    def get_output_selection(self):
        """
        Returns the output stage selection. 0, Open Drain, 1 = Output Buffer
        :return: 0 or 1
        """
        read = self._device.readRaw(PI3HDMI336_TOTAL_BYTES)
        return int(read[PI3HDMI336_OFFSET_BYTE0] & PI3HDMI336_BYTE0_HDP_OUTPUT_STAGE != 0)

    def get_port_logic_setting(self, port):
        assert self.PortA <= port <= self.PortC
        read = self._device.readRaw(PI3HDMI336_TOTAL_BYTES)
        if port == self.PortA:
            return int(read[PI3HDMI336_OFFSET_BYTE0] & PI3HDMI336_BYTE0_HDP_PORT_A != 0)
        elif port == self.PortB:
            return int(read[PI3HDMI336_OFFSET_BYTE0] & PI3HDMI336_BYTE0_HDP_PORT_B != 0)
        else:
            return int(read[PI3HDMI336_OFFSET_BYTE0] & PI3HDMI336_BYTE0_HDP_PORT_C != 0)

    def get_port_resistor(self, port):
        """
        Get the connected resistor of a port (0 = RPd connected (200K Ohm), 1 = RT connected (50 Ohm))
        :param port: Port A, B, C
        :return: 0 = RPd connected (200K Ohm), 1 = RT connected (50 Ohm)
        """
        assert self.PortA <= port <= self.PortC
        read = self._device.readRaw(PI3HDMI336_TOTAL_BYTES)
        if port == self.PortA:
            return int(read[PI3HDMI336_OFFSET_BYTE1] & PI3HDMI336_BYTE1_RT_PORT_A != 0)
        elif port == self.PortB:
            return int(read[PI3HDMI336_OFFSET_BYTE1] & PI3HDMI336_BYTE1_RT_PORT_B != 0)
        else:
            return int(read[PI3HDMI336_OFFSET_BYTE1] & PI3HDMI336_BYTE1_RT_PORT_C != 0)

    def get_port_connected(self, port):
        """
        Return whether the chosen port is connected to 5V or not
        :param port: Port A, B, C
        :return: boolean (0 = disconnected, 1 = connected)
        """
        assert self.PortA <= port <= self.PortC
        read = self._device.readRaw(PI3HDMI336_TOTAL_BYTES)
        if port == self.PortA:
            return int(read[PI3HDMI336_OFFSET_BYTE1] & PI3HDMI336_BYTE1_5V_PORT_C != 0)
        elif port == self.PortB:
            return int(read[PI3HDMI336_OFFSET_BYTE1] & PI3HDMI336_BYTE1_5V_PORT_B != 0)
        else:
            return int(read[PI3HDMI336_OFFSET_BYTE1] & PI3HDMI336_BYTE1_5V_PORT_A != 0)

    def get_interrupt_flag(self):
        """
        Flag will be set from 0 to 1 when any 5V_Port has detected a plug or unplug transition action
        :return: boolean
        """
        read = self._device.readRaw(PI3HDMI336_TOTAL_BYTES)
        return bool(read[PI3HDMI336_OFFSET_BYTE0] & PI3HDMI336_BYTE1_INT_FLAG != 0)

    def get_dcc_selection(self):
        """
        Return the selected DCC channel.
        :return: 0 (Passive switch) or 1 (Active Switch Buffer)
        """
        read = self._device.readRaw(PI3HDMI336_TOTAL_BYTES)
        return int(read[PI3HDMI336_OFFSET_BYTE0] & PI3HDMI336_BYTE1_INT_FLAG != 0)

    def set_input_port(self, port):
        """
        Set the HDMI input port
        :param port: A, B, C or None
        :return:
        """
        assert -1 <= port <= 2
        if port == -1:
            port = 3
        read = bytearray(self._device.readRaw(PI3HDMI336_TOTAL_BYTES))
        read[PI3HDMI336_OFFSET_BYTE0] = (read[PI3HDMI336_OFFSET_BYTE0] & (~PI3HDMI336_BYTE0_INPUT_PORT)) | (port << 6)
        self._device.writeRaw(read)

    def set_tmds_output(self, value):
        """
        Set the TMDS output
        :param value: boolean 0 or 1
        :return:
        """
        assert type(value) is bool
        read = bytearray(self._device.readRaw(PI3HDMI336_TOTAL_BYTES))
        read[PI3HDMI336_OFFSET_BYTE0] = \
            (read[PI3HDMI336_OFFSET_BYTE0] & (~PI3HDMI336_BYTE0_TMDS_OUTPUT_ENABLE)) | (value << 5)
        self._device.writeRaw(read)

    def set_input_selection(self, value):
        """
        Set the HPD input selection.
        :param value: 0 = HPD_SINK 1 = I2C Register Setting from set_port_logic_setting
        :return:
        """
        assert type(value) is bool
        read = bytearray(self._device.readRaw(PI3HDMI336_TOTAL_BYTES))
        read[PI3HDMI336_OFFSET_BYTE0] = \
            (read[PI3HDMI336_OFFSET_BYTE0] & (~PI3HDMI336_BYTE0_HDP_INPUT)) | (value << 4)
        self._device.writeRaw(read)

    def set_output_selection(self, value):
        """
        Set HPD Output Stage selection
        :param value: 0 = Open Drain 1 = Output Buffer
        :return:
        """
        assert type(value) is bool
        read = bytearray(self._device.readRaw(PI3HDMI336_TOTAL_BYTES))
        read[PI3HDMI336_OFFSET_BYTE0] = \
            (read[PI3HDMI336_OFFSET_BYTE0] & (~PI3HDMI336_BYTE0_HDP_OUTPUT_STAGE)) | (value << 3)
        self._device.writeRaw(read)

    def set_port_logic_setting(self, port, value):
        """
        Set the HPD logic of a port. See the documentation for further details
        :param port: PortA, PortB or PortC
        :param value: boolean 0 or 1
        :return:
        """
        assert type(value) is bool
        assert 0 <= port <= 2
        read = bytearray(self._device.readRaw(PI3HDMI336_TOTAL_BYTES))
        read[PI3HDMI336_OFFSET_BYTE0] = \
            (read[PI3HDMI336_OFFSET_BYTE0] & (~(0x01 << port))) | (value << port)
        self._device.writeRaw(read)

    def set_port_resistor(self, port, value):
        """
        Set the resistor value of each individual port
        :param port: PortA, PortB or PortC
        :param value: 0 = Rpd connected, 1 = Rt connected
        :return:
        """
        assert type(value) is bool
        assert 0 <= port <= 2
        port = 7 - port
        read = bytearray(self._device.readRaw(PI3HDMI336_TOTAL_BYTES))
        read[PI3HDMI336_OFFSET_BYTE1] = \
            (read[PI3HDMI336_OFFSET_BYTE1] & (~(0x01 << port))) | (value << port)
        self._device.writeRaw(read)

    def set_dcc_selection(self, value):
        """
        Set the DCC channel
        :param value: 0 = passive 1 = active
        :return:
        """
        assert type(value) is bool
        read = bytearray(self._device.readRaw(PI3HDMI336_TOTAL_BYTES))
        read[PI3HDMI336_OFFSET_BYTE1] = \
            (read[PI3HDMI336_OFFSET_BYTE1] & (~PI3HDMI336_BYTE1_DCC_CHANNEL)) | value
        self._device.writeRaw(read)

