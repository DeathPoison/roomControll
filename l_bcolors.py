#!/usr/bin/env python
# -*- coding: utf-8 -*-


class bcolors:  # Class to color output under Linux Systems - other not tested Mac OS shoud work!

    end = "\033[00m"

    LtBlack =   "\033[1;30m"
    LtRed =     "\033[1;31m"
    LtGreen =   "\033[1;32m"
    LtYellow =  "\033[1;33m"
    LtBlue =    "\033[1;34m"
    LtMagenta = "\033[1;35m"
    LtCyan =    "\033[1;36m"
    LtWhite =   "\033[1;37m"

    Black =   "\033[22;30m"
    Red =     "\033[22;31m"
    Green =   "\033[22;32m"

    Yellow =  "\033[22;33m"
    Blue =    "\033[22;34m"
    Magenta = "\033[22;35m"
    Cyan =    "\033[22;36m"
    White =   "\033[22;37m"

    DkBlack =   "\033[2;30m"
    DkRed =     "\033[2;31m"
    DkGreen =   "\033[2;32m"
    DkYellow =  "\033[2;33m"
    DkBlue =    "\033[2;34m"
    DkMagenta = "\033[2;35m"
    DkCyan =    "\033[2;36m"
    DkWhite =   "\033[2;37m"

    BgLtBlack =   "\033[1;40m"
    BgLtRed =     "\033[1;41m"
    BgLtGreen =   "\033[1;42m"
    BgLtYellow =  "\033[1;43m"
    BgLtBlue =    "\033[1;44m"
    BgLtMagenta = "\033[1;45m"
    BgLtCyan =    "\033[1;46m"
    BgLtWhite =   "\033[1;47m"

    BgBlack =   "\033[22;40m"
    BgRed =     "\033[22;41m"
    BgGreen =   "\033[22;42m"
    BgYellow =  "\033[22;43m"
    BgBlue =    "\033[22;44m"
    BgMagenta = "\033[22;45m"
    BgCyan =    "\033[22;46m"
    BgWhite =   "\033[22;47m"

    BgDkBlack =   "\033[2;40m"
    BgDkRed =     "\033[2;41m"
    BgDkGreen =   "\033[2;42m"
    BgDkYellow =  "\033[2;43m"
    BgDkBlue =    "\033[2;44m"
    BgDkMagenta = "\033[2;45m"
    BgDkCyan =    "\033[2;46m"
    BgDkWhite =   "\033[2;47m"

    '''
            print bc.LtBlack + 'Some Text to check the Color: Lt Black' + bc.end
            print bc.LtRed + 'Some Text to check the Color: Lt Red' + bc.end
            print bc.LtGreen + 'Some Text to check the Color: Lt Green' + bc.end
            print bc.LtYellow + 'Some Text to check the Color: Lt Yellow' + bc.end
            print bc.LtBlue + 'Some Text to check the Color: Lt Blue' + bc.end
            print bc.LtMagenta + 'Some Text to check the Color: Lt Magenta' + bc.end
            print bc.LtCyan + 'Some Text to check the Color: Lt Cyan' + bc.end
            print bc.LtWhite + 'Some Text to check the Color: Lt White' + bc.end

            print bc.Black + 'Some Text to check the Color:  Black' + bc.end
            print bc.Red + 'Some Text to check the Color:  Red' + bc.end
            print bc.Green + 'Some Text to check the Color:  Green' + bc.end
            print bc.Yellow + 'Some Text to check the Color:  Yellow' + bc.end
            print bc.Blue + 'Some Text to check the Color:  Blue' + bc.end
            print bc.Magenta + 'Some Text to check the Color:  Magenta' + bc.end
            print bc.Cyan + 'Some Text to check the Color:  Cyan' + bc.end
            print bc.White + 'Some Text to check the Color:  White' + bc.end

            print bc.DkBlack + 'Some Text to check the Color: Dk Black' + bc.end
            print bc.DkRed + 'Some Text to check the Color: Dk Red' + bc.end
            print bc.DkGreen + 'Some Text to check the Color: Dk Green' + bc.end
            print bc.DkYellow + 'Some Text to check the Color: Dk Yellow' + bc.end
            print bc.DkBlue + 'Some Text to check the Color: Dk Blue' + bc.end
            print bc.DkMagenta + 'Some Text to check the Color: Dk Magenta' + bc.end
            print bc.DkCyan + 'Some Text to check the Color: Dk Cyan' + bc.end
            print bc.DkWhite + 'Some Text to check the Color: Dk White' + bc.end

            print bc.BgLtBlack + 'Some Text to check the Color: Lt Black' + bc.end
            print bc.BgLtRed + 'Some Text to check the Color: Lt Red' + bc.end
            print bc.BgLtGreen + 'Some Text to check the Color: Lt Green' + bc.end
            print bc.BgLtYellow + 'Some Text to check the Color: Lt Yellow' + bc.end
            print bc.BgLtBlue + 'Some Text to check the Color: Lt Blue' + bc.end
            print bc.BgLtMagenta + 'Some Text to check the Color: Lt Magenta' + bc.end
            print bc.BgLtCyan + 'Some Text to check the Color: Lt Cyan' + bc.end
            print bc.BgLtWhite + 'Some Text to check the Color: Lt White' + bc.end

            print bc.BgBlack + 'Some Text to check the Color:  Black' + bc.end
            print bc.BgRed + 'Some Text to check the Color:  Red' + bc.end
            print bc.BgGreen + 'Some Text to check the Color:  Green' + bc.end
            print bc.BgYellow + 'Some Text to check the Color:  Yellow' + bc.end
            print bc.BgBlue + 'Some Text to check the Color:  Blue' + bc.end
            print bc.BgMagenta + 'Some Text to check the Color:  Magenta' + bc.end
            print bc.BgCyan + 'Some Text to check the Color:  Cyan' + bc.end
            print bc.BgWhite + 'Some Text to check the Color:  White' + bc.end

            print bc.BgDkBlack + 'Some Text to check the Color: Dk Black' + bc.end
            print bc.BgDkRed + 'Some Text to check the Color: Dk Red' + bc.end
            print bc.BgDkGreen + 'Some Text to check the Color: Dk Green' + bc.end
            print bc.BgDkYellow + 'Some Text to check the Color: Dk Yellow' + bc.end
            print bc.BgDkBlue + 'Some Text to check the Color: Dk Blue' + bc.end
            print bc.BgDkMagenta + 'Some Text to check the Color: Dk Magenta' + bc.end
            print bc.BgDkCyan + 'Some Text to check the Color: Dk Cyan' + bc.end
            print bc.BgDkWhite + 'Some Text to check the Color: Dk White' + bc.end
    '''