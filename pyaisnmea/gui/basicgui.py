"""
A GUI for the AIS decoder written with tkinter
"""

import datetime
import logging
import multiprocessing
import threading
import time
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import tkinter.scrolledtext
import tkinter.ttk

import pyaisnmea.ais as ais
import pyaisnmea.capturefile as capturefile
import pyaisnmea.livekmlmap as livekmlmap
import pyaisnmea.nmea as nmea
import pyaisnmea.network as network

import pyaisnmea.gui.aismessagetab as aismessagetab
import pyaisnmea.gui.exporttab as exporttab
import pyaisnmea.gui.guihelp as guihelp
import pyaisnmea.gui.shipstab as shipstab
import pyaisnmea.gui.statstab as statstab
import pyaisnmea.gui.stationinfotab as stationinfotab

AISLOGGER = logging.getLogger(__name__)


class TabControl(tkinter.ttk.Notebook):
    """
    organise the main tabs

    Note:
        tabs are numbered left to right

    Args:
        window(tkinter.Tk): the main window this spawns from
    """

    def __init__(self, window):
        tkinter.ttk.Notebook.__init__(self, window)
        self.window = window
        self.statstab = statstab.StatsTab(self)
        self.add(self.statstab, text='Stats')
        self.shipstab = shipstab.ShipsTableTab(self)
        self.add(self.shipstab, text='Ships')
        self.exporttab = exporttab.ExportTab(self)
        self.add(self.exporttab, text='Export')
        self.messagetab = aismessagetab.AISMessageTab(self)
        self.add(self.messagetab, text='Message Log')
        self.stninfotab = stationinfotab.StationInfoTab(self)
        self.add(self.stninfotab, text='Station Information')


class NetworkSettingsWindow(tkinter.Toplevel):
    """
    window to configure network settings

    Args:
        window(tkinter.Tk): the main window this spawns from
    """

    def __init__(self, window):
        tkinter.Toplevel.__init__(self, window)
        self.window = window
        self.network_settings_group()
        self.nmea_settings_group()
        self.kml_settings_group()

    def network_settings_group(self):
        """
        group all the network settings within a tkinter LabelFrame
        """
        netgroup = tkinter.LabelFrame(
            self, text="Network settings", padx=10, pady=10)
        netgroup.pack(fill="both", expand="yes")
        serverhostlabel = tkinter.Label(netgroup, text='Server IP')
        serverhostlabel.pack()
        self.serverhost = tkinter.Entry(netgroup)
        self.serverhost.insert(0, self.window.netsettings['Server IP'])
        self.serverhost.pack()
        serverportlabel = tkinter.Label(netgroup, text='Server Port')
        serverportlabel.pack()
        self.serverport = tkinter.Entry(netgroup)
        self.serverport.insert(0, self.window.netsettings['Server Port'])
        self.serverport.pack()
        self.chk = tkinter.Checkbutton(
            netgroup, text='forward NMEA Sentences to a remote host',
            var=self.window.forwardsentences)
        self.chk.pack()
        remotehostlabel = tkinter.Label(netgroup, text='Remote Server IP')
        remotehostlabel.pack()
        self.remotehost = tkinter.Entry(netgroup)
        self.remotehost.insert(0, self.window.netsettings['Remote Server IP'])
        self.remotehost.pack()
        remoteportlabel = tkinter.Label(netgroup, text='Remote Server Port')
        remoteportlabel.pack()
        self.remoteport = tkinter.Entry(netgroup)
        self.remoteport.insert(
            0, self.window.netsettings['Remote Server Port'])
        self.remoteport.pack()

    def nmea_settings_group(self):
        """
        group all the nmea settings within a tkinter LabelFrame
        """
        nmeagroup = tkinter.LabelFrame(
            self, text="NMEA logging settings", padx=20, pady=20)
        nmeagroup.pack(fill="both", expand="yes")
        loglabel = tkinter.Label(nmeagroup, text='Log NMEA Sentences')
        loglabel.pack()
        self.logpath = tkinter.Entry(nmeagroup)
        self.logpath.insert(0, self.window.netsettings['Log File Path'])
        self.logpath.pack()
        logpathbutton = tkinter.Button(
            nmeagroup, text='Choose Log Path', command=self.set_log_path)
        logpathbutton.pack()

    def kml_settings_group(self):
        """
        group all the kml settings within a tkinter LabelFrame
        """
        kmlgroup = tkinter.LabelFrame(
            self, text="Live KML map settings", padx=20, pady=20)
        kmlgroup.pack(fill="both", expand="yes")
        kmllabel = tkinter.Label(kmlgroup, text='Ouput Live KML Map')
        kmllabel.pack()
        self.kmlpath = tkinter.Entry(kmlgroup)
        self.kmlpath.insert(0, self.window.netsettings['KML File Path'])
        self.kmlpath.pack()
        kmlpathbutton = tkinter.Button(
            kmlgroup, text='Choose KML Path', command=self.set_kml_path)
        kmlpathbutton.pack()
        self.kmzchk = tkinter.Checkbutton(
            kmlgroup, text='KMZ map (full colour icons)',
            var=self.window.kmzlivemap)
        self.kmzchk.pack()

        savesettingsbutton = tkinter.Button(
            self, text='Save Settings', command=self.save_settings)
        savesettingsbutton.pack()
        self.transient(self.window)

    def set_log_path(self):
        """
        open a dialogue box to choose where we save NMEA sentences to
        """
        outputfile = tkinter.filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=(("nmea text file", "*.txt"),
                       ("All Files", "*.*")))
        self.logpath.insert(0, outputfile)

    def set_kml_path(self):
        """
        open a dialogue box to choose where we save KMl data to
        """
        outputdir = tkinter.filedialog.askdirectory()
        self.kmlpath.insert(0, outputdir)

    def save_settings(self):
        """
        get the settings from the form
        """
        if self.window.serverrunning:
            tkinter.messagebox.showwarning(
                'Network Settings',
                'cannot change settings whilst server is running')
        else:
            self.window.netsettings['Server IP'] = self.serverhost.get()
            self.window.netsettings['Server Port'] = int(self.serverport.get())
            self.window.netsettings['Remote Server IP'] = self.remotehost.get()
            self.window.netsettings['Remote Server Port'] = int(
                self.remoteport.get())
            self.window.netsettings['Log File Path'] = self.logpath.get()
            self.window.netsettings['KML File Path'] = self.kmlpath.get()
            tkinter.messagebox.showinfo(
                'Network Settings', 'Network Settings Saved', parent=self)
        self.destroy()


class BasicGUI(tkinter.Tk):
    """
    a basic GUI using tkinter to control the program

    Attributes:
        nmeatracker(nmea.NMEAtracker): deals with the NMEA sentences
        aistracker(ais.AISTracker): decodes the AIS messages
        messagedict(dict): stores all the messages
        statuslabel(tkinter.Label): forms the status bar at the top of the
                                    main window
        mpq(multiprocessing.Queue): used to communicate with the
                                      server process
        updateguithread(threading.Thread): updates the GUI, is None on init
        refreshguithread(threading.Thread):refreshes the GUI, is None on init
        serverprocess(multiprocessing.Process): process that listens for AIS
            sentences on the network, is None on init
        serverrunning(bool): true if the server is running
        stopevent(threading.Event): stop even to stop the threads
        forwardsentences(tkinter.BooleanVar): should sentences be
                                              forwarded to another server
        livemap(bool): should a live KML map be created
    """

    netsettings = {
        'Server IP': '127.0.0.1',
        'Server Port': 10110,
        'Remote Server IP': '127.0.0.1',
        'Remote Server Port': 10111,
        'Log File Path': '',
        'KML File Path': ''}

    def __init__(self):
        tkinter.Tk.__init__(self)
        self.nmeatracker = nmea.NMEAtracker()
        self.aistracker = ais.AISTracker()
        self.messagedict = {}
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.title('AIS NMEA 0183 Decoder')
        self.statuslabel = tkinter.Label(self, text='', bg='light grey')
        self.statuslabel.pack(fill=tkinter.X)
        self.tabcontrol = TabControl(self)
        self.tabcontrol.pack(expand=1, fill='both')
        self.top_menu()
        self.mpq = multiprocessing.Queue()
        self.updateguithread = None
        self.refreshguithread = None
        self.serverprocess = None
        self.serverrunning = False
        self.stopevent = threading.Event()
        self.forwardsentences = tkinter.BooleanVar()
        self.forwardsentences.set(0)
        self.kmzlivemap = tkinter.BooleanVar()
        self.kmzlivemap.set(0)
        self.livemap = None

    def clear_gui(self):
        """
        clear the gui of all data
        """
        res = tkinter.messagebox.askyesno('Clearing GUI', 'Are you sure?')
        if res:
            if self.serverrunning:
                tkinter.messagebox.showwarning(
                    'WARNING', 'Cannot clear GUI whilst server is running')
            else:
                self.statuslabel.config(text='', bg='light grey')
                self.tabcontrol.statstab.aismsgtotal.configure(text='')
                self.tabcontrol.statstab.nmeasentencetotal.configure(text='')
                self.tabcontrol.statstab.nmeamultipartassembled.configure(
                    text='')
                self.tabcontrol.statstab.totalstns.configure(text='')
                self.tabcontrol.statstab.starttime.configure(text='')
                self.tabcontrol.statstab.latesttime.configure(text='')
                self.tabcontrol.statstab.msgstatstxt.delete(1.0, tkinter.END)
                self.tabcontrol.statstab.shiptypestxt.delete(1.0, tkinter.END)
                self.tabcontrol.statstab.flagstxt.delete(1.0, tkinter.END)
                self.tabcontrol.shipstab.tree.delete(
                    *self.tabcontrol.shipstab.tree.get_children())
                self.tabcontrol.messagetab.tree.delete(
                    *self.tabcontrol.messagetab.tree.get_children())
                self.tabcontrol.stninfotab.stnoptions['values'] = []
                self.aistracker.stations.clear()
                self.aistracker.messages.clear()
                self.aistracker.timings.clear()
                self.aistracker.messagesprocessed = 0
                self.nmeatracker.multiparts.clear()
                self.nmeatracker.channelcounter.clear()
                self.nmeatracker.sentencecount = 0
                self.nmeatracker.reassembled = 0
                self.messagedict.clear()

    def top_menu(self):
        """
        format and add the top menu to the main window
        """
        menu = tkinter.Menu(self)
        openfileitem = tkinter.Menu(menu, tearoff=0)
        openfileitem.add_command(label='Open', command=self.open_file)
        openfileitem.add_command(label='Clear GUI', command=self.clear_gui)
        openfileitem.add_command(label='Quit', command=self.quit)
        menu.add_cascade(label='File', menu=openfileitem)
        networkitem = tkinter.Menu(menu, tearoff=0)
        networkitem.add_command(
            label='Settings', command=self.network_settings)
        networkitem.add_command(
            label='Start Network Server', command=self.start_server)
        networkitem.add_command(
            label='Stop Network Server', command=self.stop_server)
        menu.add_cascade(label='Network', menu=networkitem)
        helpitem = tkinter.Menu(menu, tearoff=0)
        helpitem.add_command(label='Help', command=self.help)
        helpitem.add_command(label='About', command=self.about)
        menu.add_cascade(label='Help', menu=helpitem)
        self.config(menu=menu)

    def network_settings(self):
        """
        open the network settings window
        """
        NetworkSettingsWindow(self)

    def about(self):
        """
        display version, licence and who created it
        """
        messagewindow = aismessagetab.MessageWindow(self)
        messagewindow.msgdetailsbox.append_text(guihelp.LICENCE)

    def help(self):
        """
        display the help window
        """
        guihelp.HelpWindow(self)

    def start_server(self):
        """
        start the server
        """
        self.serverrunning = True
        self.tabcontrol.statstab.starttime.configure(
            text=datetime.datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S'))
        if self.netsettings['KML File Path'] != '':
            if self.kmzlivemap.get() == 1:
                kmzoutput = True
            else:
                kmzoutput = False
            self.livemap = livekmlmap.LiveKMLMap(
                self.netsettings['KML File Path'], kmzoutput=kmzoutput)
            self.livemap.create_netlink_file()
        if self.forwardsentences.get() == 1:
            print('forwarding sentences')
            self.serverprocess = multiprocessing.Process(
                target=network.mpserver,
                args=[self.mpq, self.netsettings['Server IP'],
                      self.netsettings['Server Port'],
                      self.netsettings['Remote Server IP'],
                      self.netsettings['Remote Server Port']],
                kwargs={'logpath': self.netsettings['Log File Path']})
        else:
            self.serverprocess = multiprocessing.Process(
                target=network.mpserver,
                args=[self.mpq, self.netsettings['Server IP'],
                      self.netsettings['Server Port']],
                kwargs={'logpath': self.netsettings['Log File Path']})
        self.serverprocess.start()
        tkinter.messagebox.showinfo('Network', 'Server Started')
        self.updateguithread = threading.Thread(
            target=self.updategui, args=(self.stopevent,))
        self.updateguithread.setDaemon(True)
        self.updateguithread.start()
        self.refreshguithread = threading.Thread(
            target=self.refreshgui, args=(self.stopevent,))
        self.refreshguithread.setDaemon(True)
        self.refreshguithread.start()
        self.statuslabel.config(
            text='AIS Server Listening on {} port {}'.format(
                self.netsettings['Server IP'],
                self.netsettings['Server Port']),
            fg='black', bg='green2')

    def stop_server(self):
        """
        stop the server
        """
        self.serverrunning = False
        self.serverprocess.terminate()
        self.stopevent.set()
        self.updateguithread.join(timeout=1)
        self.refreshguithread.join(timeout=1)
        self.serverprocess = None
        self.updateguithread = None
        self.refreshguithread = None
        tkinter.messagebox.showinfo('Network', 'Server Stopped')
        self.statuslabel.config(text='', bg='light grey')
        self.stopevent.clear()

    def open_file(self):
        """
        pop open a file browser to allow the user to choose which NMEA 0183
        text file they want to process and then process it
        """
        if self.serverrunning:
            tkinter.messagebox.showwarning(
                'WARNING', 'Stop Server First')
        else:
            inputfile = tkinter.filedialog.askopenfilename(
                filetypes=(
                    ("NMEA 0183 text files", "*.txt *.nmea"),
                    ("pyaisnmea DEBUG comma seperated values", "*.csv"),
                    ("pyaisnmea DEBUG JSON lines", "*.jsonl")))
            self.statuslabel.config(
                text='Loading capture file - {}'.format(inputfile),
                fg='black', bg='gold')
            self.update_idletasks()
            try:
                if inputfile.endswith('.csv'):
                    self.aistracker, self.messagedict = \
                        capturefile.aistracker_from_csv(inputfile)
                    self.nmeatracker.sentencecount = 'N/A'
                    self.nmeatracker.reassembled = 'N/A'
                elif inputfile.endswith('.jsonl'):
                    self.aistracker, self.messagedict = \
                        capturefile.aistracker_from_json(inputfile)
                    self.nmeatracker.sentencecount = 'N/A'
                    self.nmeatracker.reassembled = 'N/A'
                else:
                    self.aistracker, self.nmeatracker, self.messagedict = \
                        capturefile.aistracker_from_file(inputfile, debug=True)
            except (FileNotFoundError, TypeError):
                self.statuslabel.config(text='', bg='light grey')
                return
            self.tabcontrol.stninfotab.stn_options()
            try:
                self.tabcontrol.statstab.starttime.configure(
                    text=self.aistracker.timings[0])
            except IndexError:
                self.tabcontrol.statstab.starttime.configure(
                    text='Unavailable')
            self.tabcontrol.statstab.write_stats()
            self.tabcontrol.statstab.write_stats_verbose()
            self.tabcontrol.shipstab.create_ship_table()
            self.tabcontrol.messagetab.create_message_table()
            for payload in self.messagedict:
                latestmsg = [payload, self.messagedict[payload].description,
                             self.messagedict[payload].mmsi,
                             self.messagedict[payload].rxtime]
                self.tabcontrol.messagetab.add_new_line(latestmsg)
            self.statuslabel.config(
                text='Loaded capture file - {}'.format(inputfile),
                fg='black', bg='light grey')

    def updategui(self, stopevent):
        """
        update the nmea and ais trackers from the network

        run in another thread whist the server is running and
        recieving packets, get NMEA sentences from the queue and process them

        Args:
            stopevent(threading.Event): a threading stop event
        """
        while not stopevent.is_set():
            qdata = self.mpq.get()
            if qdata:
                try:
                    payload = self.nmeatracker.process_sentence(qdata)
                    if payload:
                        currenttime = datetime.datetime.utcnow().strftime(
                            '%Y/%m/%d %H:%M:%S')
                        try:
                            msg = self.aistracker.process_message(
                                payload, timestamp=currenttime)
                        except (IndexError, KeyError) as err:
                            errmsg = '{} - error with - {}'.format(
                                str(err), payload)
                            AISLOGGER.error(errmsg)
                        self.messagedict[payload] = msg
                        latestmsg = [payload, msg.description,
                                     msg.mmsi, currenttime]
                        self.tabcontrol.messagetab.add_new_line(latestmsg)
                        self.tabcontrol.statstab.write_stats()
                except (nmea.NMEAInvalidSentence, nmea.NMEACheckSumFailed,
                        ais.UnknownMessageType, ais.InvalidMMSI) as err:
                    AISLOGGER.debug(str(err))
                    continue
                except IndexError:
                    AISLOGGER.debug('no data on line')
                    continue

    def refreshgui(self, stopevent):
        """
        refresh and update the gui every 10 seconds, run in another thread

        Args:
            stopevent(threading.Event): a threading stop event
        """
        while not stopevent.is_set():
            currenttime = datetime.datetime.utcnow().strftime(
                '%Y/%m/%d %H:%M:%S')
            if currenttime.endswith('5'):
                self.tabcontrol.shipstab.create_ship_table()
                self.tabcontrol.statstab.write_stats_verbose()
                self.tabcontrol.stninfotab.stn_options()
                self.tabcontrol.stninfotab.show_stn_info()
                if self.livemap:
                    self.aistracker.create_kml_map(
                        self.livemap.kmlpath, kmzoutput=self.livemap.kmzoutput,
                        linestring=False, livemap=True,
                        livemaptimeout=480)
                time.sleep(1)

    def quit(self):
        """
        open a confirmation box asking if the user wants to quit if yes then
        stop the server and exit the program
        """
        res = tkinter.messagebox.askyesno('Exiting Program', 'Are you sure?')
        if res:
            if self.serverrunning:
                self.stop_server()
            self.destroy()
