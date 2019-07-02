import binary

import messages.aismessage


class Type5StaticAndVoyageData(messages.aismessage.AISMessage):
    """
    detailed information sent by class A equipment

    Note:
        text fields are padded with whitespaces .rstrip() removes them

    Attributes:
        aisversion(int): the version of AIS being used
        imo(int): International Maritime Organisation number
                  this number identifies the vessel and doesn't change even if
                  the vessel changes names, flags or owner
        callsign(str): identifies the vessel over marine VHF voice comms
        name(str): the name of the vessel
        shiptype(str): the type of ship - lookup from self.shiptypes
        length(int): ship length in metres
        width(int): ship width in metres
        epfdfixtype(str): how the EPFD aquires its position fix
        eta(str): estimated time of arrival "%H:%M %d/%m"
        draught(float): draught of the ship
        destination(str): where the ship is going to
        dte(str): is device operating as Data Terminal Equipment
    """
    def __init__(self, msgbinary):
        super().__init__(msgbinary)
        self.aisversion = binary.decode_sixbit_integer(msgbinary, 38, 40)
        self.imo = binary.decode_sixbit_integer(msgbinary, 40, 70)
        self.callsign = binary.decode_sixbit_ascii(msgbinary, 70, 112).rstrip()
        self.name = binary.decode_sixbit_ascii(msgbinary, 112, 232).rstrip()
        self.shiptype = self.shiptypes[binary.decode_sixbit_integer(
            msgbinary, 232, 240)]
        tobow = binary.decode_sixbit_integer(msgbinary, 240, 249)
        tostern = binary.decode_sixbit_integer(msgbinary, 249, 258)
        toport = binary.decode_sixbit_integer(msgbinary, 258, 264)
        tostarboard = binary.decode_sixbit_integer(msgbinary, 264, 270)
        self.length = tobow + tostern
        self.width = toport + tostarboard
        self.epfdfixtype = self.epfdfixtypes[binary.decode_sixbit_integer(
            msgbinary, 270, 274)]
        etamonth = binary.decode_sixbit_integer(msgbinary, 274, 278)
        etaday = binary.decode_sixbit_integer(msgbinary, 278, 283)
        etahour = binary.decode_sixbit_integer(msgbinary, 283, 288)
        etamin = binary.decode_sixbit_integer(msgbinary, 288, 294)
        self.eta = '{}:{} {}/{}'.format(etahour, etamin, etaday, etamonth)
        self.draught = binary.decode_sixbit_integer(msgbinary, 294, 302) / 10
        self.destination = binary.decode_sixbit_ascii(
            msgbinary, 302, 422).rstrip()
        self.dte = self.dtevalues[binary.decode_sixbit_integer(
            msgbinary, 422, 423)]

    def __str__(self):
        """
        describes the message object

        Returns:
            strtext(str): string containing information about the message
        """
        strtext = ('Static and Voyage Data - MMSI: {}, Name: {}, '
                   'Ship Type: {}, Callsign: {}, Length: {}, Width: {},'
                   ' Draught: {}, ETA: {}, Destination: {}'
                   '').format(self.mmsi, self.name, self.shiptype,
                              self.callsign, self.length, self.width,
                              self.draught, self.eta, self.destination)
        return strtext

    def get_details(self):
        """
        get the most pertinent details of the message as a dictionary

        Returns:
            details(dict): most relevant information of this message
        """
        details = {}
        details['EPFD Fix type'] = self.epfdfixtype
        details['Callsign'] = self.callsign
        details['Width (m)'] = self.width
        details['Length (m)'] = self.length
        details['Draught (m)'] = self.draught
        details['Destination'] = self.destination
        details['ETA'] = self.eta
        details['IMO number'] = self.imo
        details['DTE'] = self.dte
        details['AIS version'] = self.aisversion
        return details
