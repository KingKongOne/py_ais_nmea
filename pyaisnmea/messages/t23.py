import pyaisnmea.binary as binary

import pyaisnmea.messages.aismessage


class Type23GroupAssignmentCommand(pyaisnmea.messages.aismessage.AISMessage):
    """
    NO REAL LIFE TEST DATA FOUND YET!
    """

    def __str__(self):
        """
        describes the message object

        Returns:
            strtext(str): string containing information about the message
        """
        strtext = ('{} - source MMSI: {}'
                   '').format(self.description, self.mmsi)
        return strtext