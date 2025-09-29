import sys
import time

program_message = \
    '''
프로그램 실행결과입니다.
-------------------------------------
{0}
-------------------------------------
이용해 주셔서 감사합니다.
'''

def display_message():
    message = program_message.format('\n'.join(sys.argv[1:])).split('\n')
    delay = 1.8 / len(message)

    for line in message:
        print(line)
        time.sleep(delay)
