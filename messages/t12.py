import binary

import messages.aismessage


class Type12AddressedSafetyMessage(messages.aismessage.AISMessage):
    """
    NO REAL LIFE TEST DATA FOUND YET!
    """
    def __init__(self, msgbinary):
        super().__init__(msgbinary)
        self.sequenceno = binary.decode_sixbit_integer(msgbinary, 38, 40)
        self.destinationmmsi = binary.decode_sixbit_integer(msgbinary, 40, 70)
        self.retransmitflag = self.binaryflag[binary.decode_sixbit_integer(
            msgbinary, 70, 71)]
        self.msgtext = binary.decode_sixbit_ascii(msgbinary, 72, 936).rstrip()

    def __str__(self):
        """
        describes the message object

        Returns:
            strtext(str): string containing information about the message
        """
        strtext = ('Addressed Safety Message - from MMSI: {}, to MMSI: {}, '
                   'Message: {}').format(self.mmsi, self.destinationmmsi,
                                         self.msgtext)
        return strtext

    def get_details(self):
        """
        get the most pertinent details of the message as a dictionary

        Returns:
            details(dict): most relevant information of this message
        """
        details = {}
        details['message from'] = self.mmsi
        details['message to'] = self.destinationmmsi
        details['retransmit'] = self.retransmitflag
        details['message'] = self.msgtext
        return details
