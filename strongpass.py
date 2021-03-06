#!/usr/bin/env python3

# Program: strongpass.py
# Version: 3.6.1
# Description: Generate strong random passwords
#
# Copyright (C) 2015-2017 Brainfuck

# GNU GENERAL PUBLIC LICENSE
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# program informations
__program__ = "strongpass"
__version__ = "3.6.1"
__author__ = "Brainfuck"

""" For generate passwords, used new module 'secrets' instead of random,
so we have more entropy
https://docs.python.org/3/library/secrets.html
"""
import sys
import argparse
import secrets


class Strongpass:
    def banner(self):
        """Show banner"""
        print("{} {}".format(__program__, __version__))
        print("Generate strong random passwords")
        print("Copyright (C) 2015-2017 {}\n".format(__author__))
        return

    def print_version(self):
        """Print program version and exit"""
        self.banner()
        print("License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>")
        print("This is free software: you are free to change and redistribute it.")
        print("There is NO WARRANTY, to the extent permitted by law.")
        sys.exit(0)

    def check(self, input_args):
        """Function for check the user input, raise an error
        if user insert one integer greather than 254
        """
        input_args = int(input_args)
        if input_args > 254:
            raise argparse.ArgumentTypeError(
                "please enter an integer no more bigger than 254")
            sys.exit(1)
        else:
            return input_args

    def get_arguments(self):
        """Get command line arguments with argparse"""
        parser = argparse.ArgumentParser(
            formatter_class = argparse.RawDescriptionHelpFormatter)

        # type=check --> recall def check() function above
        parser.add_argument("-l", "--lenght", type=self.check,
            help="Lenght of passwords")
        parser.add_argument("-n", "--number", type=self.check,
            help="Number of passwords to generate")
        parser.add_argument("-m", "--mode", choices=["0", "1", "2"],
            help="Passwords generation mode: 0 only letters, 1 random, 2 alphanumeric")
        parser.add_argument("-v", "--version", action="store_true",
            help="display program version and exit")

        args = parser.parse_args()

        # -v, --version
        if args.version:
            self.print_version()

        # if no arguments are given, print banner and help
        if len(sys.argv) == 1:
            self.banner()
            parser.print_help()
            sys.exit(1)

        # check if all required arguments are passed
        if args.lenght and args.number and args.mode is not None:
            return args
        else:
            print("error: the following arguments are required: -l LENGHT, -n NUMBER, -m {0,1,2}")
            print("Use '{} -h, --help' for more informations.".format(__program__))
            sys.exit(1)

    def gen_password(self):
        """Generate password/s"""
        args = self.get_arguments()
        """characters excluded: "l0Oo`ìèéòçà°"
        TODO: add option to argparse for do this
        """
        letters = "abcdefghijkmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ"
        numbers = "123456789"
        special = "|\!$%&/()='?^~[]{}+*@#<>,;.:-_"

        for x in range(args.number):
            """Modes"""
            # 0 = only letters passwords
            if args.mode == "0":
                charset = letters

            # 1 = random passwords
            elif args.mode == "1":
                charset = letters + numbers + special

            # 2 = alphanumeric passwords
            elif args.mode == "2":
                charset = letters + numbers

            # print password/s
            password = "".join((secrets.choice(charset))
                for x in range(args.lenght))

            # add more entropy: at least one of all characters available
            if (any((letters) for c in password)
                and any((numbers) for c in password)
                and any((special) for c in password)):
                print(password)


def main():
    """main function"""
    strongpass = Strongpass()
    strongpass.gen_password()


if __name__ == '__main__':
    main()
