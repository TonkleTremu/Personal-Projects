import math

max_iterations = 1000

x = 0

prime_lengths = []
non_prime_lengths = []

while(x < 1000000):
    x+=1
    cx = x
    iteration = 0
    oddsevens = ""
    flag = False
    while(cx != 1 and iteration < max_iterations):
        if(cx % 2 == 0):
            cx = cx/2
            oddsevens += "E"
        else:
            cx = 3*cx + 1
            oddsevens += "O"
        iteration += 1
    if(cx != 1):
        print(f"{x} is the one!")
        break
    else:
        for i in range(2, math.ceil(x/2)+1):
            if(x%i==0):
                flag = True
                break
        if(flag):
            #print(f"{x,oddsevens}")
            non_prime_lengths.append(len(oddsevens))
        else:
            #print(f"Prime: {x,oddsevens}")
            prime_lengths.append(len(oddsevens))
        if(x % 100 == 0):
            print(f"{x}th number checked.")
print(sum(prime_lengths)/len(prime_lengths)) # Average for 1,000,000 values: 136.41103708327495
print(sum(non_prime_lengths)/len(non_prime_lengths)) # Average for 1,000,000 values: 131.01048615248382
