#!/usr/bin/python

import sys
import os
from   subprocess   import call
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
        # This two buttons have parent! now I can disable and enable theme.
        self.start_button = QPushButton(self.tr("&Start"))
        self.interrupt_button = QPushButton(self.tr("&Interrupt"))
        close_button = QPushButton(self.tr("&Close"))
        reset_button = QPushButton(self.tr("&Reset"))

        # it's the operations flag. it has three types: pomo, rest, long-rest
        self.flag = None

        # it's the number of done pomodoros. if total_pomo % 4 == 0 then user can
        # tak a long rest.
        self.total_pomo = 0
        self.start_label = QLabel()
        self.stop_label = QLabel()
        self.status_label = QLabel()
        self.total_label = QLabel()

        # This is the pomodoro timers progress bar
        self.pomo_time_progress = QProgressBar()
        # This is the rest timers progress bar
        self.rest_time_progress = QProgressBar()

        # rest/pomo timers. I will use them to take time for pomodoros and rests times.
        self.pomo_timer = QTimer()
        self.rest_timer = QTimer()
        # initializing variables. I use it to make reseting theme easy ;-)
        self.var_init()

        # Radio buttons initialized. and long rest radio button is checked
        self.rdobtn_short_rest = QRadioButton(self.tr("&Short Rest (15 min)"))
        self.rdobtn_long_rest = QRadioButton(self.tr("&Long Rest (25 min)"))
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
        prog_layout.addWidget(self.pomo_time_progress)
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
        
        layout = QGridLayout()
        layout.addWidget(time_group, 0, 0, 1, 2)
        layout.addLayout(prog_layout, 1, 0)
        layout.addWidget(state_group, 1, 1)
        layout.addWidget(rest_rdo_group, 2, 0, 1, 2)
        layout.addLayout(btn_layout, 3, 0, 1, 2)
        self.setLayout(layout)

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
        self.interrupt_button.setEnabled(True)

        # Set the flag to retrive currct information in update_labels function
        self.flag = 'Pomodoro'
        self.update_labels(self.flag)
        # Every seccond it will generate a self.pomo_timer.timeout() after evry
        # Signal update_pomo_prog will call.
        self.pomo_timer.start(1000)
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
            self.interrupt_button.setEnabled(False)
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
        # use mplayer to play ding sound
        call(["mplayer", self.ding_sound_path]) # this is subprocess call function
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
        self.start_button.setEnabled(True)
        # It has to be here. After a reset you'll need it :D
        self.sys_try_icon.setIcon(QIcon(self.red_icon_path))
        
    def reset_func(self):
        # Stop every thing and make program clean!
        self.rest_timer.stop()
        self.pomo_timer.stop()
        self.var_init()

    def chat_answer_machine(self):
        message = str(self.stop_time.toString())
        answering_machine.DBus_Answer(message)
        
def main():
    app = QApplication(sys.argv)
    run = Form()
    run.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()