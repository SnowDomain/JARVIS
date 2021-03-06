#!/usr/bin/python
#
# Name: jarvis.py
# Description: This is the MAIN FILE for IDA's jarvis plugin
#

__VERSION__ = 0.5

import os

from idc import *
from idautils import *
from idaapi import *

from PySide import QtGui
from PySide.QtGui import QIcon

from jarvis.Config import JConfig

from jarvis.core.BinaryAnalysis import BinaryAnalysis
from jarvis.core.VulnDetection import VulnDetection
from jarvis.core.ImportExport import ImportExport

from jarvis.widgets.VulnDetectionWidget import VulnDetectionWidget
from jarvis.widgets.BinaryAnalysisWidget import BinaryAnalysisWidget
from jarvis.widgets.ImportExportWidget import ImportExportWidget
from jarvis.widgets.ScratchPadWidget import ScratchPadWidget
from jarvis.widgets.OptionsWidget import OptionsWidget

from jarvis.core.helpers.UI import install_ui_hooks


#################################################################
class JarvisPluginForm(PluginForm):
    """
    Jarvis main window.
    Setup of core modules and widgets is performed in here.
    """

    def __init__(self):
        """
        Initialization. Dough.
        """
        super(JarvisPluginForm, self).__init__()
        self.jarvisWidgets = []
        self.config = JConfig()
        self.iconp = self.config.icons_path


    def showBanner(self):
        """
        Old school is cool
        """
        banner = (
                "=============================================\n"
                "= Jarvis starting...\n\n"
                )

        print banner


    def OnCreate(self, form):
        """
        This is called on form creation (obviously)
        """
        self.showBanner()
        self.parent = self.FormToPySideWidget(form)
        self.parent.setWindowIcon(QIcon(self.iconp + 'user-ironman.png'))

        self.setupCore()
        self.setupWidgets()
        self.setupUI()


    def setupCore(self):
        """
        Initializes all internal functionality
        """
        print "= Instantiating core modules...\n"

        self.binary_analysis = BinaryAnalysis()
        self.vuln_detection = VulnDetection()
        self.import_export = ImportExport()


    def setupWidgets(self):
        """
        Instantiates all widgets
        """
        print "= Creating / Loading individual widgets..."

        # Append to the list every widget you have
        self.jarvisWidgets.append(BinaryAnalysisWidget(self))
        self.jarvisWidgets.append(VulnDetectionWidget(self))
        self.jarvisWidgets.append(ImportExportWidget(self))
        self.jarvisWidgets.append(ScratchPadWidget(self))
        self.jarvisWidgets.append(OptionsWidget(self))

        self.setupJarvisForm()


    def setupJarvisForm(self):
        """
        Already initialized widgets are arranged in tabs on the main window.
        """
        self.tabs = QtGui.QTabWidget()
        self.tabs.setTabsClosable(False)

        for widget in self.jarvisWidgets:
            self.tabs.addTab(widget, widget.icon, widget.name)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.tabs)

        self.parent.setLayout(layout)


    def setupUI(self):
        """
        Manages the IDA UI extensions / modifications
        """
        install_ui_hooks()


    def Show(self):
        """
        Overload this method to specify form options
        """
        return PluginForm.Show(self,
            ":: JARVIS ::",
            options = (
                PluginForm.FORM_CLOSE_LATER |
                PluginForm.FORM_RESTORE |
                PluginForm.FORM_SAVE
                )
            )


    def OnClose(self, form):
        """
        Perform some cleanup here, if necessary
        """
        print "= [*] JarvisPluginForm closed"
        print "=============================================\n"



#################################################################
class JarvisPlugin(plugin_t):
    """
    This is the skeleton plugin as seen by IDA
    """
    flags = 0
    comment = "Jarvis Plugin. Your personal IDA butler."
    help = "It saves time... and headaches."
    wanted_name = "JARVIS"
    wanted_hotkey = "Ctrl-Alt-F8"

    def init(self):
        self.icon_id = 0
        return PLUGIN_KEEP


    def run(self, arg = 0):
        f = JarvisPluginForm()
        f.Show()


    def term(self):
        idaapi.msg("[*] JarvisPlugin terminated")


#################################################################
def PLUGIN_ENTRY():
    """
    Entry point for IDA
    """
    return JarvisPlugin()



#################################################################
# Usage as script (through Alt+F7)
#################################################################
def main():

    global JARVIS

    try:
        # There is an instance, reload it
        JARVIS
        JARVIS.OnClose(JARVIS)
        JARVIS = JarvisPluginForm()

    except:
        # There is no instance yet
        JARVIS = JarvisPluginForm()


    JARVIS.Show()



if __name__ == '__main__':
    main()
