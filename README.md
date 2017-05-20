# subrute.py

This is a script that attempts to brute force passwords using /bin/su. It requires
pexpect. Hopefully it will be installed already. Otherwise, you may have to use pip:

	$ pip install --user pexpect

You can also pipe in input from stdin. This is nice when using cewl or davenavarrosgoatee.py:

	$ ./davenavarrosgoatee.py -p /home/user --stdout | ./subrute.py -u guest -w -

# Limitations

This takes an average of 2 seconds per password attempted. This will take a really long time
in many cases. Using an extremely large wordlist is foolish. This works well when you already
have a few known passwords on a network to test for password reuse, but not for general purpose
brute forcing.

Using this script is also very loud. Each failed attempt generates logs.

This also hasn't been tested on many systems yet. If the output for /bin/su is different,
pexpect will fail to match patterns and the script will break. Please submit a PR or issue
if anyone actually uses this and runs into this issue.

