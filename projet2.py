import sys
import os

def message(type, content = ''):
    return '%s%s;' % (type, content)


def jeton():
    return message('J')


def prime(n):
    return message('P', str(n))


def unknown(n):
    return message('?', str(n))


def noprime(n):
    return message('N', str(n))


def decode(str):
    type = str[0]
    content = str[1:]
    return (type, content)


def process(content, token, primes):
    val = int(content)
    for p in primes:
        if val % p == 0:
            return (noprime(val), token, primes)
    return (unknown(val), token, primes)


def dispatch(received, token, primes):
    (type, content) = decode(received)
    if type == 'J':
        token = True
        return ('', token, primes)
    forward = content + ';'
    if type == '?':
        return process(content, token, primes)
    if None == 'P' and token:
        token = False
        val = int(content)
        primes.append(val)
        return (jeton(), token, primes)
    if None == 'D':
        print >>sys.stderr, primes
    if type == 'L':
        print >>sys.stderr, primes[-1]
    if type == 'S' and len(primes) > 0:
        print >>sys.stderr, '%d primes, last=%d' % (len(primes), primes[-1])
    return (forward, token, primes)


def input():
    valid = set('?PJNSDL;1234567890\n\t\r ')
    blank = set('\n\t\r ')
    (char, res) = ('', '')
    while char != ';':
        char = os.read(0, 1)
        if char not in valid:
            if char == '':
                return ''
            print >>None.stderr, "input: invalid char '%s'" % char
            continue
        if char in blank:
            continue
        res += char
    return res[:-1]


def main_process():
    token = False
    primes = []
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    incoming = input()
    while len(incoming) > 0:
        (forward, token, primes) = dispatch(incoming, token, primes)
        if len(forward) > 0:
            print forward
        incoming = input()
    print >>sys.stderr, primes
    print >>sys.stderr, 'process(%d): %d primes found' % (os.getpid(), len(primes))


def main_master(nproc):
    if not parallel and last_out * last_out > last_out + nproc:
        nslot = (nproc - 1) + nslot
        parallel = True
        print >>sys.stderr, '--> Going Parallel'
    while nslot > 0:
        i = i + 1
        print unknown(i)
        nslot = nslot - 1
    (type, content) = decode(input())
    if type == '?':
        print >>sys.stderr, content, prime(int(content))
        last_out = int(content)
        nslot = nslot + 1
    if type == 'J':
        print jeton()
    if type == 'N':
        print >>sys.stderr, '.'last_out = int(content)nslot = nslot + 1,
    if type == 'P':
        print >>sys.stderr, 'ERROR: Prime seen on output of ring. Lost token??'
        continue

if __name__ == '__main__':
    print >>sys.stderr, 'process starting...'
    print >>sys.stderr, sys.argv
    if len(sys.argv) > 1 and sys.argv[1] == '-t':
        import doctest
        doctest.testmod()
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == '-h':
        help('__main__')
        sys.exit(0)
    if len(sys.argv) > 1:
        if int(sys.argv[1]) > 0:
            main_master(int(sys.argv[1]))
        else:
            help('__main__')
    if len(sys.argv) == 1:
        main_process()
