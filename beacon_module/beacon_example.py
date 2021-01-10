import bluetooth._bluetooth as bluez
import struct


def decode(packet):
    """
    Returns the string representation of a raw HCI packet.
    """
    return ''.join('%02x' % struct.unpack("B", bytes([x]))[0] for x in packet)


class Beacon:

    def _set_up_sock(self):
        flt = bluez.hci_filter_new()  # очищается и создается новый фильтр
        bluez.hci_filter_all_events(flt)  # применять фильтр ко всем событиям
        bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)  # выбор типа пакета (hci packet type)
        self.sock.setsockopt(bluez.SOL_HCI, bluez.HCI_FILTER,
                             flt)  # применение фильтра к сокету (sol_hci уровень сокета, опция и значение)
        return self.sock

    def _hci_toggle_le_scan(self, enable):
        cmd_pkt = struct.pack("<BB", enable, 0x00)  # создает байт строку указанного формата
        bluez.hci_send_cmd(self.sock, self.OGF_LE_CTL, self.OCF_LE_SET_SCAN_ENABLE,
                           cmd_pkt)  # передает HCI команду сокету

    def __init__(self, dev_id=0):
        self.dev_id = dev_id
        self.sock = bluez.hci_open_dev(dev_id)  # создание  экземпляра класса bluetooth
        self.OGF_LE_CTL = 0x08
        self.OCF_LE_SET_SCAN_ENABLE = 0x0C
        self._hci_toggle_le_scan(0x01)
        self.dist = 0

    def _distance(self, rssi, tx):
        ratio = (255 - rssi) / tx
        if ratio < 1:
            return ratio ** 10
        return 0.89976 * (ratio ** 7.7095) + 0.111

    def recieve(self, beacon_id, tx):
        self.sock = self._set_up_sock()
        while True:
            packet = self.sock.recv(255)
            data = decode(packet)
            if data.find(beacon_id) != -1:
                dist = self._distance(int(decode(packet[-1:]), 16), tx)
                print(data, self.exponentially_weighted_average(dist))
                # TODO send distance to server
                # TODO exponentially weighted average could be on server???

    def disable(self):
        self._hci_toggle_le_scan(0x00)

    def exponentially_weighted_average(self, distance, betta=0.8):
        return betta * self.dist + (1 - betta) * distance


try:
    beacon = Beacon(0)
    print("Seaching Beacons\n")
    beacon.recieve("798e456b", -70)
    # TODO Tx on phone -65, but distance is wrong. If set tx on raspberry as -70 everything is okay
except KeyboardInterrupt as e:
    beacon.disable()
except:
    print("Error accessing bluetooth")
