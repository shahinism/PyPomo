#!/usr/bin/python

import sys
import os
import re
from   PyQt4.QtGui  import *
from   PyQt4.QtCore import *
import answering_machine

class Form(QDialog):
    def __init__(self, parent = None):
        super(Form, self).__init__(parent)
        # These variables will hold the local path of this source.
        src_dir, this_file = os.path.split(__file__)
        # This variables are my Icon and sound sources
        self.red_icon_path = os.path.join(src_dir, "graphics", "red_icon.svg")
        self.green_icon_path = os.path.join(src_dir, "graphics", "green_icon.svg")
        self.yellow_icon_path = os.path.join(src_dir, "graphics", "yellow_icon.svg")
        self.ding_sound_path = os.path.join(src_dir, "sounds", "ding.wav")

        # UI initializer
        self.setupUi()

    def systemtry_icon(self):
        # its icon initialized in self.var_init to automatic reset the icon after the reset pressed
        self.sys_try_icon = QSystemTrayIcon(self)
        self.sys_try_icon.setToolTip("PyPomo Time management system")
        self.sys_try_icon.setIcon(QIcon(self.red_icon_path))
        # Show systemtry icon
        self.sys_try_icon.show()
        
    def setupUi(self):
        # First of all setup the systemtry Icon
        self.systemtry_icon()

        # System tray menus actions:
        self.exit_action = QAction("Quit", self)
        self.start_action = QAction("Start", self)
        self.interrupt_action = QAction("Interrupt", self)
        self.reset_action = QAction("Reset", self)
        self.show_window_action = QAction("Show Window", self)
        # This two buttons have parent! now I can disable and enable theme.
        self.start_button = QPushButton(self.tr("&Start"))
        self.interrupt_button = QPushButton(self.tr("&Interrupt"))
        close_button = QPushButton(self.tr("&Quit"))
        reset_button = QPushButton(self.tr("&Reset"))

        # it's the operations flag. it has three types: pomo, rest, long-rest
        self.flag = None

        # Tab widget initializer:
        tab_widget = QTabWidget()
        main_tab = QWidget() # Main tab
        self.config_tab = QWidget() # config tab

        # it's the number of done pomodoros. if total_pomo % 4 == 0 then user can
        # tak a long rest.
        self.total_pomo = 0
        self.start_label = QLabel()
        self.stop_label = QLabel()
        self.status_label = QLabel()
        self.total_label = QLabel()
        self.am_text = QLineEdit() # Answering machines text.
        self.am_text.setText(self.tr("PyPomo: Hi, my master is not able to answer you right now, you have to wait. He may will be able at $AnswerTime"))
        am_label = QLabel(self.tr("&Answer:"))
        am_label.setBuddy(self.am_text)
        am_tip = QLabel(self.tr("<strong>Tip</strong>: You can use <strong>$AnswerTime</strong> tag to show your pomodoros end time! "))
        pomo_time_label = QLabel(self.tr("Pomodoro Timer:"))
        rest_time_label = QLabel(self.tr("Rest Timer:"))
        # This is the pomodoro timers progress bar
        self.pomo_time_progress = QProgressBar()
        # This is the rest timers progress bar
        self.rest_time_progress = QProgressBar()

        # This check box will appear in configure tab to help user to enable/disable
        # answering machine function
        self.am_enabler = QCheckBox(self.tr("&Enable Answering Machine"))
        self.am_enabler.setChecked(True)

        # rest/pomo timers. I will use them to take time for pomodoros and rests times.
        self.pomo_timer = QTimer()
        self.rest_timer = QTimer()
        # initializing variables. I use it to make reseting theme easy ;-)
        self.var_init()

        # Radio buttons initialized. and long rest radio button is checked
        self.rdobtn_short_rest = QRadioButton(self.tr("&Short (15 min)"))
        self.rdobtn_long_rest = QRadioButton(self.tr("&Long (25 min)"))
        self.rdobtn_long_rest.setChecked(True)

        rest_rdo_group = QGroupBox(self.tr("Long rest configuration"))
        rdo_layout = QHBoxLayout()
        rdo_layout.addWidget(self.rdobtn_long_rest)
        rdo_layout.addWidget(self.rdobtn_short_rest)
        rest_rdo_group.setLayout(rdo_layout)

        time_group = QGroupBox(self.tr("Session start/stop time"))
        time_label_layout = QHBoxLayout()
        time_label_layout.addWidget(self.start_label)
        time_label_layout.addWidget(self.stop_label)
        time_group.setLayout(time_label_layout)

        prog_layout = QVBoxLayout()
        prog_layout.addWidget(pomo_time_label)
        prog_layout.addWidget(self.pomo_time_progress)
        prog_layout.addWidget(rest_time_label)
        prog_layout.addWidget(self.rest_time_progress)

        state_group = QGroupBox(self.tr("State"))
        label_layout = QVBoxLayout()
        label_layout.addWidget(self.status_label)
        label_layout.addWidget(self.total_label)
        state_group.setLayout(label_layout)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.start_button)
        btn_layout.addWidget(self.interrupt_button)
        btn_layout.addWidget(reset_button)
        btn_layout.addWidget(close_button)

        # Answering machine configuration group:
        am_group = QGroupBox(self.tr("Answering machines massage"))
        am_group_layout = QVBoxLayout()
        am_group_layout.addWidget(am_label)
        am_group_layout.addWidget(self.am_enabler)
        am_group_layout.addWidget(self.am_text)
        am_group_layout.addWidget(am_tip)
        am_group.setLayout(am_group_layout)

        # Main_tab layout:
        mt_layout = QGridLayout(main_tab)
        mt_layout.addWidget(time_group, 0, 0, 1, 2)
        mt_layout.addLayout(prog_layout, 1, 0, 2, 1)
        mt_layout.addWidget(state_group, 1, 1, 2, 1)
        mt_layout.addLayout(btn_layout, 3, 0, 1, 2)

        # Config_tab layout:
        ct_layout = QGridLayout(self.config_tab)
        ct_layout.addWidget(rest_rdo_group, 0, 0, 1, 2)
        ct_layout.addWidget(am_group, 1, 0, 1, 2)

        # Add widgets to the tabs. 
        tab_widget.addTab(main_tab, self.tr("&Main"))
        tab_widget.addTab(self.config_tab, self.tr("&Configure"))

        # Add tab widget to the main dialog window
        main_layout = QVBoxLayout()
        main_layout.addWidget(tab_widget)

        self.setLayout(main_layout)

        try_menu = QMenu()
        try_menu.addAction(self.show_window_action)
        try_menu.addSeparator()
        try_menu.addAction(self.start_action)
        try_menu.addAction(self.interrupt_action)
        try_menu.addAction(self.reset_action)
        try_menu.addSeparator()
        try_menu.addAction(self.exit_action)
        self.sys_try_icon.setContextMenu(try_menu)
        
        # SIGNAL/SLOT:
        # Timeout signal for pomo and rest timer
        self.pomo_timer.timeout.connect(self.update_pomo_prog)
        self.rest_timer.timeout.connect(self.update_rest_prog)

        # Buttons clicked signals
        self.start_button.clicked.connect(self.run_pomo)
        self.interrupt_button.clicked.connect(self.interrupt_func)
        reset_button.clicked.connect(self.reset_func)
        close_button.clicked.connect(qApp.quit)
        self.sys_try_icon.activated['QSystemTrayIcon::ActivationReason'].connect(self.show_window)

        self.exit_action.triggered.connect(qApp.quit)
        self.start_action.triggered.connect(self.run_pomo)
        self.interrupt_action.triggered.connect(self.interrupt_func)
        self.reset_action.triggered.connect(self.reset_func)
        self.show_window_action.triggered.connect(lambda x: self.setVisible(True))
        
        # Root window property
        self.setWindowTitle(self.tr("PyPomo"))
        self.setWindowIcon(QIcon(self.red_icon_path))

    def show_window(self, reason):
        """
        This function will use to show the window again after user minimized it.
        """
        # The reason will send from QSystemTrayIcon::ActivationReason!
        if reason == QSystemTrayIcon.DoubleClick:
            self.setVisible(True)

    def closeEvent(self, event):
        """
        This function will re implement closeEvent function. This will happen
        when the user close the window by 'X' button or so.
        """
        # Here I ignored the event that will close the window
        event.ignore()
        # To have same effect I just called done function that who know what to do!
        self.done('closeEvent')
        
    def done(self, r):
        """
        This function will re implement done function. This will happen when the user
        use 'ESC' button to close the dialog window.
        """
        # This will make the dialog window invisible!
        self.setVisible(False)
        
    def run_pomo(self):
        # If it's pomodoro time start button has to be disabled and interrupt button
        self.start_button.setEnabled(False)
        self.start_action.setEnabled(False)
        self.interrupt_button.setEnabled(True)
        self.interrupt_action.setEnabled(True)
        self.config_tab.setEnabled(False)
        self.sys_try_icon.setIcon(QIcon(self.red_icon_path))
        # Set the flag to retrive currct information in update_labels function
        self.flag = 'Pomodoro'
        self.update_labels(self.flag)
        # Every seccond it will generate a self.pomo_timer.timeout() after evry
        # Signal update_pomo_prog will call.
        self.pomo_timer.start(1000)
        
        if self.am_enabler.isChecked():
            self.chat_answer_machine()

    def update_pomo_prog(self):
        # The following expression will calcualte that how much is 1 seccond from 25 minutes
        # then I will use this to increase pomo_time_progress bar ;-)
        self.pomo_step +=  100.00/1500.00
        self.pomo_time_progress.setValue(self.pomo_step)

        # If pomo_time_progress over flowed, then do this steps:
        if self.pomo_step >= 100:
            # add one to total_pomodoros counter
            self.total_pomo += 1
            # Play a ding sound
            self.play_ding()
            # generate the proper message in systemtry
            self.sys_try_icon.showMessage(self.tr("Done"),
                                          self.tr("Pomodoro number %d is finished.\
                                                  \nTake some rest." % self.total_pomo))
            self.pomo_time_progress.setValue(0)
            self.pomo_timer.stop()
            # Reset the pomo_step variable
            self.pomo_step = 0
            self.rest_time_func()

    def rest_time_func(self):
        # If user did 4 pomodoro, it's time to take a long rest!
        if self.total_pomo % 4 == 0:
            self.flag = 'Long Rest'
        else:
            self.flag = 'Rest'
        self.sys_try_icon.setIcon(QIcon(self.green_icon_path))
        self.update_labels(self.flag)
        self.rest_timer.start(1000)

    def update_rest_prog(self):
        # here pypomo will calculate users rest time. 5 minutes, 15 minutes or 20?
        # Radio buttons will help it to find right time for long rest.
        if self.flag == 'Rest':
            # The following expression will calcualte that how much is 1 seccond from 5 minutes
            self.rest_step += 100.00/300.00
        elif self.flag == 'Long Rest':
            # The following expression will calcualte that how much is 1 seccond from 15 minutes
            if self.rdobtn_short_rest.isChecked():
                self.rest_step += 100.00/900.00
            # The following expression will calcualte that how much is 1 seccond from 25 minutes
            elif self.rdobtn_long_rest.isChecked():
                self.rest_step += 100.00/1500.00
        self.rest_time_progress.setValue(self.rest_step)

        # If rest time ended, do this steps:
        if self.rest_step >= 100:
            self.play_ding()
            self.sys_try_icon.showMessage(self.tr("Done"),
                                          self.tr("Your rest time is finished.\
                                                  \nDo another pomodoro!"))
            self.rest_time_progress.setValue(0)
            self.rest_step = 0
            self.rest_timer.stop()
            # Enable start button and disable interrupt. 
            self.start_button.setEnabled(True)
            self.start_action.setEnabled(True)
            self.interrupt_button.setEnabled(False)
            self.interrupt_action.setEnabled(False)
            self.sys_try_icon.setIcon(QIcon(self.red_icon_path))

    def update_labels(self, flag):
        current_time = QTime.currentTime()
        if flag == 'Pomodoro':
            self.stop_time = current_time.addSecs(25 * 60) # it'll show 25 minutes later ;-)
        elif flag == 'Rest':
            self.stop_time = current_time.addSecs(5 * 60) # it'll show 5 minutes later
        elif flag == 'Long Rest':
            # calculate the proper stop time. it'll be different on rest times.
            if self.rdobtn_short_rest.isChecked():
                self.stop_time = current_time.addSecs(15 * 60)
            elif self.rdobtn_long_rest.isChecked():
                self.stop_time = current_time.addSecs(25 * 60) 

        self.start_label.setText(self.tr("Start Time: %s" % current_time.toString()))
        self.stop_label.setText(self.tr("Stop Time: %s" % self.stop_time.toString()))
        self.status_label.setText(self.tr("Status: %s" % flag))
        self.total_label.setText(self.tr("Pomodoros: %d" % self.total_pomo))

    def interrupt_func(self):
        """
        This function is a little wierd! I have to modify it later!
        """
        # Disable answering machine:
        answering_machine.connect_dbus(flag = 'block')
        # after interrupt user have to do another pomodoro!
        self.flag = "Pomodoro"
        # stop timers. Don't do anything else!
        self.rest_timer.stop()
        self.pomo_timer.stop()
        # to keep self.total_pomo unchanged!
        total_pomo = self.total_pomo
        self.var_init()
        self.total_pomo = total_pomo
        # I tried to do this some how else, but with no chance I lost!
        # This is a little ugly, but it'll work ;-)
        self.total_label.setText(self.tr("Pomodoros: %d" % self.total_pomo))

        # Change the icon color to yellow. this means user did an interrupt
        self.sys_try_icon.setIcon(QIcon(self.yellow_icon_path))
        
    def play_ding(self):
        try:
            from PyQt4.phonon import Phonon
            self.m_media = Phonon.MediaObject(self)
            audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
            Phonon.createPath(self.m_media, audioOutput)
            self.m_media.setCurrentSource(Phonon.MediaSource(Phonon.MediaSource(self.ding_sound_path)))
            self.m_media.play()
        except:
            print "I can't play sound. for that you need to install phonon on you distribution ;-)"

        # use mplayer to play ding sound
        #call(["mplayer", self.ding_sound_path]) # this is subprocess call function
                                             # and I used it to play a ding sound
        
    def var_init(self):
        self.flag = None # it's the operations flag. it has three types: pomo, rest, long-rest
        self.total_pomo = 0 # it's the number of done pomos
        self.start_label.setText(self.tr("Start Time: 00:00:00"))
        self.stop_label.setText(self.tr("stop Time: 00:00:00"))
        self.status_label.setText(self.tr("Status: Pomodoro"))
        self.total_label.setText(self.tr("Pomodoros: 0"))
        self.pomo_time_progress.setValue(0)
        self.rest_time_progress.setValue(0)
        self.pomo_step = 0
        self.rest_step = 0
        self.interrupt_button.setEnabled(False)
        self.interrupt_action.setEnabled(False)
        self.start_button.setEnabled(True)
        self.start_action.setEnabled(True)
        # It has to be here. After a reset you'll need it :D
        self.sys_try_icon.setIcon(QIcon(self.red_icon_path))
        self.config_tab.setEnabled(True)
        
    def reset_func(self):
        # Disable answering machine:
        answering_machine.connect_dbus(flag = 'block')
        # Stop every thing and make program clean!
        self.rest_timer.stop()
        self.pomo_timer.stop()
        self.var_init()

    def chat_answer_machine(self):
        # Here PyPomo will search if there is a tag like '$AnswerTime' replace it with current session stop time.
        message = str(self.am_text.text())
        time_tag = re.compile(r'\$AnswerTime')
        search_tag = re.search(time_tag, message)
        if search_tag:
            message = re.sub(r'\$AnswerTime', str(self.stop_time.toString()), message)
        answering_machine.connect_dbus(message)

        
def main():
    app = QApplication(sys.argv)
    run = Form()
    run.show()
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()
