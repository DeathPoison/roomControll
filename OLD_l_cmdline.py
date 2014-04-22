#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from l_bcolors import bcolors as bc
    from time import strftime       # use for bash time
except Exception, err:
    print err


class cmdline():
    """cmdLine interface for tinkerclient"""
    def __init__(self, user, enumInstance):
        self.bashRunning = False
        self.user = user
        self.master = enumInstance
        self.ipcon = self.master.ipcon
        # self.bash()

        # Check for user and generate List of Commands for him!
        if self.user == 'LimeBlack':
            self.swap_dict = {
                'state': self.master.toggleState,
                'door': self.master.toggleDoor,
                'light': self.master.toggleLight,
            }
            self.cmd_dict = {
                'status': self.master.status,
            }

    def bashCommand(self, command):

        input = command.split(' ')
        self.input = input

        if self.user == 'LimeBlack':

            if input[0] == '':          # Prevent errors by false input
                pass

            elif input[0] == 'swap':    # swap switchable functions/variables
                if len(self.input) <= 1:
                    print self.swap_dict.keys()
                elif len(self.input) >= 2:
                    if input[1] == '?':
                        print self.swap_dict.keys()
                    elif input[1] in self.swap_dict:
                        self.swap_dict[input[1]]()

            elif input[0] in self.cmd_dict:
                self.cmd_dict[input[0]]()

            elif input[0] == 'set':
                if len(self.input) >= 3:
                    if input[1] == 'mode': self.master.mode = input[2]
                    print bc.LtCyan + 'Set mode to ' + input[2] + bc.end
                else:
                    print bc.BgDkRed + bc.Black + 'Use: set var value' + bc.end

            elif input[0] == 'q':
                self.bashRunning = False
            else:
                print bc.BgDkRed + bc.Black + 'command not found' + bc.end
                print bc.BgDkRed + bc.Black + 'Available are:' + bc.end
                print bc.BgDkRed + bc.Black + '\t swap' + bc.end
                print bc.BgDkRed + bc.Black + '\t status' + bc.end
        else:
            print bc.BgDkRed + bc.Black + 'command not found' + bc.end

        #if input[0] == 'q':
        #    self.bashRunning = False

        #if input[0] == 'cmd':
        #    print bc.BgDkRed + bc.Black + 'command not found' + bc.end

        #if input[0] == 'read':
        #    print self.user

        #if input[0] == 'set':
        #    if len(input) >= 2:
        #        if input[1] == 'user':
        #            self.user = input[2]

        #if input[0] == 'test':
        #    print bc.LtGreen + 'Some Text in Color: Lt Green' + bc.end
        #    print bc.LtCyan + ' Some Text in Color: Lt Cyan' + bc.end
        #    print bc.LtWhite + 'Some Text in Color: Lt White' + bc.end
        #
        #    print bc.Black + '  Some Text in Color:  Black' + bc.end
        #    print bc.Red + '    Some Text in Color:  Red' + bc.end
        #    print bc.Green + '  Some Text in Color:  Green' + bc.end
        #    print bc.Yellow + ' Some Text in Color:  Yellow' + bc.end
        #    print bc.Blue + '   Some Text in Color:  Blue' + bc.end
        #    print bc.Magenta + 'Some Text in Color:  Magenta' + bc.end
        #
        #    print
        #    print bc.BgLtGreen + 'Some Text in Color: Lt Green' + bc.end
        #    print bc.BgLtCyan + ' Some Text in Color: Lt Cyan' + bc.end
        #    print bc.BgLtWhite + 'Some Text in Color: Lt White' + bc.end
        #
        #    print bc.BgBlack + 'Some Text in Color:  Black' + bc.end
        #    print bc.BgRed + '  Some Text in Color:  Red' + bc.end

    def bash(self):

        self.bashRunning = True  # code from Evil ]=}
        self.master.status()     # show status on ~init!

        while self.bashRunning:

            mytime = bc.Green + strftime('%H:%M') + bc.end

            self.USER = bc.Red + self.user + bc.end
            if self.user == 'LimeBlack':
                self.USER = bc.BgCyan + bc.Black + self.user + bc.end

            input = raw_input(self.USER + ' at ' + mytime + ' # ')

            # Endless Loop for User Input!
            self.bashCommand(input)
        return 'Stopped'