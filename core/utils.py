import sys
from time import sleep


def countdown(num_of_secs):
    while num_of_secs:
        m, s = divmod(num_of_secs, 60)
        sys.stdout.write("\rWe will try again in: {:02d}:{:02d}".format(m, s))
        sys.stdout.flush()
        sleep(60)
        num_of_secs -= 60
    print('\n')
