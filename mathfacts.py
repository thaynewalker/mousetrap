import random

while True:
    a = random.randint(1, 10)
    b = random.randint(4, 8)
    answer=int(raw_input("What is %dx%d? "%(a,b)))
    if answer==a*b:
        print "Yes!"
    else:
        print "No sireee!  It is ",(a*b)
