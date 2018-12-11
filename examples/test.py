from PI3HDMI336 import PI3HDMI336
import time

device = PI3HDMI336()

def print_all():
    print("----")
    print("Current selected output: {}" .format(device.get_input_port()))
    print("TMDS Output Enable: {}".format(device.get_tmds_output()))
    print("HPD Input Selection: {}".format("HPD_SINK" if device.get_input_selection() else "I2C register setting"))
    print("HPD Output Selection: {}".format("Open Drain" if device.get_output_selection() else "Output Buffer"))
    print("")
    print("HPD Port A Logic Setting: {}".format(device.get_port_logic_setting(PI3HDMI336.PortA)))
    print("HPD Port B Logic Setting: {}".format(device.get_port_logic_setting(PI3HDMI336.PortB)))
    print("HPD Port C Logic Setting: {}".format(device.get_port_logic_setting(PI3HDMI336.PortC)))
    print("")
    print("Port A resistor: {}".format("RT connected (50 Ohm)" if device.get_port_resistor(PI3HDMI336.PortA) else "RPd connected (200K Ohm)"))
    print("Port B resistor: {}".format("RT connected (50 Ohm)" if device.get_port_resistor(PI3HDMI336.PortB) else "RPd connected (200K Ohm)"))
    print("Port C resistor: {}".format("RT connected (50 Ohm)" if device.get_port_resistor(PI3HDMI336.PortC) else "RPd connected (200K Ohm)"))
    print("")
    print("5V Port A: {}".format("Connected" if device.get_port_connected(PI3HDMI336.PortA) else "Disconnected"))
    print("5V Port B: {}".format("Connected" if device.get_port_connected(PI3HDMI336.PortB) else "Disconnected"))
    print("5V Port C: {}".format("Connected" if device.get_port_connected(PI3HDMI336.PortC) else "Disconnected"))
    print("")
    print("Interrupt: {}".format("Set" if device.get_interrupt_flag() else "Clear"))
    print("DCC channel selection: {}".format("Active switch buffer" if device.get_dcc_selection() else "Passive switch"))
    print("----")


print_all()
