# -*- coding: utf-8 -*-
# filename          : settings.py
# description       : Different options for main.py
# author            : Ian Ault
# email             : ianault2022@isd282.org
# date              : 03-29-2022
# version           : v1.0
# usage             : python main.py
# notes             : This file should not be run directly
# license           : MIT
# py version        : 3.10.2
#==============================================================================
# Sets the browser option "--headless", this will prevent the browser from
# opening a GUI window.
# Because of this, the "--disable-gpu" flag is also enabled when HEADLESS is
# set to True.
# The default value is True.
HEADLESS = True

# Sets the folder path of where the JSON files are stored.
# The directory should end in a "/" character to avoid errors.
# The default value is "logs/".
LOG_DIRECTORY = "logs/"
