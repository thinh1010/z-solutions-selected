#!/usr/bin/python3

#
#                  |
#                 >9< 
#             8    |    0  
#                  |
#          7       |       1        
#                  X                
#          6               2        
#                         ^^^
#             5         3           
#                  4                
#
#      Motivation
#     ============
#    - We have a bike lock with N wheels. Each wheel has ten numbers '0' to '9'.
#      (like the diagram above).
#    - Moving a single wheel one position counts as one move.
#    - How can we get between two codes (say) 9218.... and 2574....
#      in the fewest moves in total?
#    - The total sum of moves is equal to the sum of the moves required per wheel.
#    - Note that we can move each wheel either left or right.
#    - We can see one move left or right is like adding or subtracting 1.
#    - We perform our moves modulo 10 - e.g. 9 + 1 == 0 and 0 - 1 == 9.
#
#    - Note that the length of the route from where you start from
#      (eg '9' in diagram) to where you finish ('2' in diagram) is different
#      depending on which way you go (clockwise or anticlockwise).
#    - In this case '2' is three positions clockwise from '9'
#      (9 => 0 => 1 => 2)
#      or seven positions anticlockwise.
#      (9 => => 8 => 7 => 6 => 5 => 4 => 3 => 2)
#    - Note that both of our routes should add up to 0 or 10 (==0 modulo 10).
#    - We could either take the other route to get back to the starting point,
#      or alternatively we never moved (we were at '9 and wanted to get to '9').
#
#      Approach
#     ==========
#    - Implement distance function d(x,y) for a single wheel as a reusable function.
#    - Loop over from wheel 1 to wheel N.
#    - A 'wheel' in this example is like a digit in the question.
#
#      Extension
#     ===========
#    - The wheel or digit in this question behaves like the quotient group Z/10Z
#      (set of integers Z modulo 10).
#    - You probably don't need to know about groups before the first year of
#      university in a math based subject.
#    - If interested you could look at:
#      https://vi.wikipedia.org/wiki/Nh%C3%B3m_th%C6%B0%C6%A1ng or ask your
#      math teacher or read an "Introduction to group theory textbook".
#      I remember a little bit but my memory isn't that good and I would have to
#      study it again to explain it well. Maybe YouTube is also good.
#    - There are lots of programming situations where you can learn about a 
#      structure or algorithm as a tool, spot a pattern in your problem that looks
#      similar to the tool and then use the structure or algorithm as a building
#      block to solve part of the problem or modify it into an easier one.



# This is the distance function, d, in the question
def d(x,y):
    #set y to be the largest number as we only need to calculate distances from one starting point later
    if y<x:
        temp = y
        y = x
        x = temp

    # calculate distance to move one way round the circle of 10 nodes
    distance1 = abs(x-y)%10
    # now calculate distance the other way
    distance2 = abs(x-y+10)%10
    #find the minimum distance
    distance = min([distance1,distance2])
    # something went wrong if we add up the distances to go both ways round and they do not sum to 0mod10
    assert (distance1+distance2)%10==0
    return distance

# This function uses d(x,y) to calculate the distance between each digit of two number strings
def calculate_distances(number_string1,number_string2):
    # Add preceding zeros if needed to make the strings the same length
    if len(number_string1) > len(number_string2):
        number_string2.zfill(len(number_string1))
    elif len(number_string1) < len(number_string2):
         number_string1.zfill(len(number_string2))
    #check string lengths are equal
    assert len(number_string1) == len(number_string2)
    distances = []
    #iterate over pairs of characters in string
    for character in range(0,len(number_string1)):
         #use function d(x,y) to find the distance between character pair. Append to distances list
         #I picked a list as I could set a debugger breakpoint and check things looked right in the memory
         #we could just sum into a cumulative variable instead of using a list to save resources if desired
         distances.append(d(int(number_string1[character]),int(number_string2[character])))
    #return distances list
    return distances

#read lines from input file
def read_data(filename):
    with open(filename,'r') as input_file:
        numbers = []
        for line in input_file:
                numbers.append(line.strip())
    input_file.close()
    return numbers

#write answer
def save_data(filename, result):
    f = open(filename, "w")
    f.writelines(str(result))
    f.close()
    return 0


#Starting point for program
#Read in number strings
[number1, number2] = read_data("DISTANCE.INP")
#Calculate distances between each pair of digits, then sum distances.
result=sum(calculate_distances(number1,number2))
#Save data into output file
save_data("DISTANCE.OUT",result)


## Test script - we can test the function d(x,y) by trying every possible value of x,y
## Each time we check d(x,y)%10==0 using line 'assert (distance1+distance2)%10==0'
## the application will throw an error if the function is broken for a supplied x and y
## uncomment the below code to use
#for x in range(0,10):
#    for y in range(0,10):
#        result = d(x,y)

# this is a test