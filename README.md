PyPOMO
=====

Pypomo is a small software to help you in more focus in your work.
it uses pomodoro technique that you can find here:
http://www.pomodorotechnique.com/

after installation you can start it from you terminal like this:
       
    $ pypomo

Snapshot
=====
![My image](https://raw.github.com/shahinism/PyPomo/master/Snapshots/window.png)

Changes
=====
v0.6.3, Wed Sep 19 13:06:13 IRDT 2012

* Answering machine now can be disabled!

v0.6.0, Tue Sep 18 15:49:04 IRDT 2012

* Minimize to system try added. All close action except
   close button will minimize the window.

* System tray icon has a control menu that can be use to control
   PyPomo

* Answering machine added. for now it can answer pidgin chat. and
   user can't disable it.

* instead of playing sound with mplayer in last version, now it uses
   PyQt4.phonon module to play sounds.

v0.5.0, Tue Sep 10 18:12:26 IRDT 2012 -- Initial release.

Installation
=====

To install PyPomo in a linux distribution you need pysetuptools
and pyqt4. install this requirements and after that run this commands:

    $ git clone https://github.com/shahinism/PyPomo.git
    $ cd PyPomo
    $ sudo python setup.py install

Usage
=====

Oh come on! this is a GUI program. but away PyPomos systemtry icon may
need some description. it has three state (color):

* Red: this color means you need to do your job. there are a lot of 
  pomodoros you need to do.

* Green: this means it's your rest time. Enjoy it. I know you will love it :D

* Yellow: this means you did an interrupt. Go back in your work as soon as you 
  can!

Thanks to:
=====

I have to say thank you to "Francesco Cirillo" for inventing this great time
management system. then, Thank you Francesco :-*

Known bugs:
=====

fixed:
* The answering machine can't disable after the first run! 