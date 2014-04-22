#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from l_bcolors import bcolors as bc
    from time import strftime       # use for bash time
except ImportError as err:
    print err

import cmd
import os


class TinkerCli(cmd.Cmd):
    """Simple command processor example."""

    def do_status(self, target):
        "Greet the target"
        if target and target in self.STATI:
            pass
            #greeting = 'hi, %s!' % target
        elif target:
            print 'not found!'
        else:
            self.master.status()

    def complete_status(self, text, line, begidx, endidx):
        if not text:
            completions = self.STATI[:]
        else:
            completions = [f
                           for f in self.STATI
                           if f.startswith(text)
                           ]
        return completions

    def help_status(self):
        print '\n'.join(['status [device/app]',
                         'Get Status of givven Device / App',
                         ])

    def prompt(self, line):
        "Change the interactive prompt"
        self.prompt = line + ': '

    # Override - STARTS the CMDLOOP - equal to handle like __init__
    def cmdloop(self, user, enumInstance, intro=None):
        #print 'cmdloop(%s)' % intro
        self.user = user
        self.master = enumInstance
        return cmd.Cmd.cmdloop(self, intro)

    # Override
    def preloop(self):

        time = bc.DkRed + strftime('%H:%M') + bc.end
        user = bc.BgBlack + bc.LtCyan + self.user + bc.end
        self.prompt = user + ' at ' + time + ' # '
        self.intro = bc.LtCyan + "### Welcome to the Command Line Client \n"
        self.intro += bc.LtCyan + "### Of your Tinkerforge Devices " + bc.end

        self.doc_header = bc.BgLtBlack + bc.LtGreen + 'Available Commands: help <cmd>' + bc.end
        self.undoc_header = bc.LtBlack + 'beta commands' + bc.end

        self.ruler = '.'

        self.ipcon = self.master.ipcon

        self.STATI = ['sdoor', 'gdoor', 'light', 'all']

        #print 'preloop()'

    # Override - Runs BEFORE every PROMPT EXCEPT the FIRST!
    def precmd(self, line):
        time = bc.DkRed + strftime('%H:%M') + bc.end
        user = bc.BgBlack + bc.LtCyan + self.user + bc.end
        self.prompt = user + ' at ' + time + ' # '
        return cmd.Cmd.precmd(self, line)

    # Override - PREVENT reuse of old input
    def emptyline(self):
        pass
        #print 'emptyline()'
        #return cmd.Cmd.emptyline(self)

    def do_q(self, line):
        return True

    def help_q(self):
        print 'q - to close this application!'

    # Override - Runs on closing the cmd instance
    def postloop(self):
        print 'closing bash!'

# really early testing
#if __name__ == '__main__':
#    TinkerCli().cmdloop('LimeBlack', 'instance')
