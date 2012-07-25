import sys

def primes(n):
    for i in xrange(2,n):
        for j in xrange(2,i):
            if i%j == 0:
                break
        else:
            yield i

if __name__=='__main__':
     v = int(sys.argv[1])
     prm = [p for p in primes(v)]



