#!/usr/bin/python3
#import datetime # only needed for the test script
# ON_TAP.docx question 1 Spreadsheet date from 1/1/1990

# Working
# 365 days per year. 366 in leap year. 1992 is first leap year after 1990.
# A leap year is a year divisible by 4, though years divisible by 100 but not divisible 
# by 400 are not leap years

# Leap years follow patterns that we can predict.
# the pattern repeats itself every 400 years due to the 'divisible by 400' rule
# We can therefore determine that any two dates that are 400 years apart are 146097
# days apart
#
# We can use datetime module to verify this
#
#      >>> import datetime
#      >>> a = datetime.date(2400,1,1) - datetime.date(2000,1,1)
#      >>> a.days
#      146097
#
# This holds for all pairs of dates that are 400 years apart - you can try it.
#
# If we call the pattern A, then time is structured like this
#
#         ... A || A || A || A || A || A || A || A || A || A || A .....
#
# Calculating the number of days between 2 days which are not 400 years apart is harder
# If we say that the 400 year pattern starts and stops after the leap year that happens
# every 400 years we can say that 1st March after the 400 year leap year is the start of 
# our pattern. this makes it easier to think about. The first date like this after 
# 1st Jan 1990 is 1st March 2000.
#
# For each repetition of out 400 year pattern (A):
# We have 4 occurrences of a 100 year pattern (B), followed by an extra leap year day (L).
#
# e.g.    A = B || B || B || B || L
#
# Every B is 36524 days long, and it follows that len(A) = 4*len(B) + len(L)
#
#                                                        = 4*36524  + 1
#
#                                                        = 146097
#
# A leap year is every 4 years, except from years divisible by 100 but not 400. Therefore
# let C be 4 years followed by a leap year. Then each B will be 24 of pattern C,
# followed by 4 years but no leap year
# 
# e.g.   B = C||C||C||C||C||C||C||C||C||C||C||C||C||C||C||C||C||C||C||C||C||C||C||C||D
#
#        C = D || L                        D = Y || Y || Y || Y 
#
#        C = Y || Y || Y || Y || L
#
#        len(B) = 36524        len(C) = 1461        len(D) = 1460
#
#  Each of the objects A, B, C, D and L above have a fixed length in days that we know 
#  or can calculate easily. The difficulty is going across a boundary which has an L.
#
# As we are starting at 1st Jan 1990, out next 400 year pattern starts at 1st March 2000 and
# this has a leap year before it
#                                  29th February 1600 | B | B | B | B | Y | 1st March 2000
#       We are here -------------------------------------------------^ 
#                                     
# If our date is before 1st March 2000, then we don't need to worry about the 100 year and
# 400 year patterns, and every year divisible by 4 is a leap year. We can solve the
# problem locally.
#
# If our date is after 1st March 2000, we can solve the problem by working out how many
# days it takes to get to 1st March 2000 and then use the known pattern to work out the
# date we will reach based on the remaining days.
#
# We check to see how many blocks of 400 years we can fit into our remaining days after
# 1st March 2000. This lets us work out which block of 400 years (A) we are in from the
# entirety of known time.
# 
#  - We add 400 * number_of_400_year_blocks to the year (currently 2000)
#  - Our new reference date is now 1st of March of the calculated year.
#  - We subtract the days that represent all of the 400 year blocks from the
#    remaining days, and move to the next step.
#  - Our target date is locally within the same 400 year block as our reference
#    date, so we no longer need to care what happens every 400 years.
#
# Our next biggest block with a known pattern is 100 years (B from above).
# We repeat the process. We have a maximum of 3 blocks to avoid the next A
#
#  - We add 100 * number_of_100_year_blocks to the year in our reference date.
#  - Our new reference date is now 1st of March of the calculated year.
#  - We subtract the days that represent all of the 100 year blocks from the
#    remaining days, and move to the next step.
#  - Our target date is locally within the same 100 year block as our reference
#    date, so we no longer need to care what happens every 100 years.
#  - Note that we need to limit ourselves to 3 100 year blocks to avoid hitting
#    the 400 year block above
#
# Our next biggest block with a known pattern is 4 years with a leap year
# (C from above). We repeat the process. We have a maximum of 24 blocks to
# avoid the next B. (as 100 / 4 = 25 and 25 - 1 = 24)
#
#  - We add 4 * number_of_4_year_plus_1_day_blocks to the year in our reference
#    date.
#  - Our new reference date is now 1st of March of the calculated year.
#  - We subtract the days that represent all of the 4 year blocks from the
#    remaining days, and move to the next step.
#  - Our target date is locally within the same 4 year block as our reference
#    date, so we no longer need to care what happens every 4 years.
#  - Note that we need to limit ourselves to 24 4 year+1 blocks to avoid hitting
#    the 100 year block above
#
# Our next biggest block with a known pattern is 1 year. Our years are exactly
# 365 days long, as if there is a leap year, it will be at the end of the 4
# year block. All whole years will be 365 days long as our reference date is
# 1st March
#
#  - We add number_of_365_day_blocks to the year in our reference
#    date.
#  - Our new reference date is now 1st of March of the calculated year.
#  - We subtract the days that represent all of the 365 day blocks from the
#    remaining days, and move to the next step.
#  - Our target date is locally within the same 1 year block as our reference
#    date. We no longer have to care about leap years for calculating the year.
#
# As our reference date is 1st of March (unless we only need to solve locally)
# the time to the next standard calendar year is only 306 days. If the
# remaining days variable is >= 306, the date must be in January or February
# of the following calendar year. We can adjust the reference date to 1st
# January of the following year and subtract 306 from the remaining days
# variable
# 
# We now know the exact target year.
# - It is easy to check if we are in a leap year
# - It is then easy to find the month and day from the reference date and 
#   remaining days.
# - Note that the reference date may be 1st of March or it may be 1st of January
#   depending on what path we took through the program before
#
#  The rest of the program is pretty normal stuff
# - The program below could be simplified a bit, though I tried to make it
#   readable / clear to follow
#
# The technique used is a bit similar to the greedy algorithm or a greedy packing
# algorithm. We stay below the target date and then try to take the biggest step 
# that we can towards it using the possible options that we have.
# https://vi.wikipedia.org/wiki/Gi%E1%BA%A3i_thu%E1%BA%ADt_tham_lam
# https://www.cs.ox.ac.uk/files/13474/greedy.pdf
# 
# We make steps of 400 years first, then solve locally for steps of 100 years, then
# solve locally for steps of 4 years and then steps of 1 year and then solve for
# the remaining days. Each time we convert the problem into a smaller problem
# with fewer things to think about, and each smaller problem is easier to 
# solve.

def block_remove(remaining_days,block_size,limit):
    block_count = remaining_days//block_size
    if (block_count>limit) and (limit !=0):
        block_count = limit
    remaining_days -= (block_count*block_size)
    assert remaining_days >= 0
    return [remaining_days, block_count]

def find_date_manual(remainder_days):
    assert remainder_days >= 0 #Check value non negative
    assert isinstance(remainder_days, int) #check value integer

    [year, month, day] = [1990,1,1] # set start date
    modifier_set = False

    # if spreadsheet_date_number < 1095, We haven't had a full leap year yet - 1095 days would be 1st Jan 1993.
    # we are inside a block of 4 years with a leap year day at the end. years ar 365 days long
    if(remainder_days >= 1095): # We need to account for leap years in previous years before this year
        # Count up to 1st March 1992 as our 'base'. one day after the 1st leap year.
        year += 2
        month = 3
        # subtract 2 non-leap years and the 60 days between 1 Jan 1990 and 1 March 1992
        remainder_days = remainder_days - (2*365) - 60
        # The next block of 400 years starts on 1st March 2000. There are exactly
        # There are exactly 1461 days between 1st March 1992 and 1st March 1996
        # There are exactly 2922 days between 1st March 1992 and 1st March 2000
        # If remaining_days < 1461, we don't need to worry about leap years anymore when counting days
        if (1461 <= remainder_days < 2922):
            # date is between 1st March 1996 and 1st March 2000
            # We move our reference date to 1st March 1996 and don't need to worry about leap years
            # anymore when counting years
            year += 4
            remainder_days -= 1461
        elif (remainder_days >= 2922):
            # Date is past 1st March 2000
            # This is the beginning of the next 400 year block
            # Move our reference date to 1st March 2000
            year += 8
            remainder_days -= 2922
            # A 400 year block is exactly 146097 days. - Like 2000-03-01 to 2400-03-01
            # We don't have to consider anything more than 400 years.
            # We can now take a 'Greedy' approach (see 'Greedy Algorithm')
            # We start with our largest block of 400 years
            # - a 400 year block always has a fixed length of 146097 days
            # Then consider 100 year blocks
            # - a 100 year block that is inside a 400 year block and doesn't pass outside of it 
            #   has a fixed length of 36524 days
            # Then consider 4 year blocks
            # - a 100 year block that is inside a 100 year block and doesn't pass outside of it 
            #   has a fixed length of 1461 days - (365*3) + 366
            if (remainder_days >= 146097):
                # We have at least 1 400 year block remaining - lets get rid of them all
                [remainder_days, block_count] = block_remove(remainder_days,146097,0)
                year += 400*block_count
            if (remainder_days >= 36524):
                # We have at least 1 100 year block remaining - lets get rid of them all
                [remainder_days, block_count] = block_remove(remainder_days,36524,3)
                year += 100*block_count
            if (remainder_days >= 1461):
                # We have at least 1 4 year block remaining - lets get rid of them all
                [remainder_days, block_count] = block_remove(remainder_days,1461,24)
                year += 4*block_count
        if (remainder_days >= 306):
            # Shift reference date to 1st January in the next year if we can
            # This prevents a year being missed if there is less than a full year
            # to our date (it is in Jan or Feb the following year)
            remainder_days -= 306
            month = 1
            year += 1

    #We now account for any remaining full years
    if (remainder_days >= 365):
        #inside a 4 year block, each full year is 365 days long
        [remainder_days, block_count] = block_remove(remainder_days,365,4)
        year += block_count

    #We know the year and now need to account for the day and month

    # define a dictionary object mapping each month to the number of days in the month
    # adjust february for current year if current year is a leap year
    #Leap years are divisable by 4
    if (year%4 == 0):
        if ((year%100) == 0) and ((year%400) != 0):
            #Years divisible by 100 but not 400 are not a leap year
            month_table = {1:31, 2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
            #if we are in a not_leap_year and it is before feb 29th then we subtract a day from those remaining
            # we added an extra day in when we didn't need to yet
        else:
            #other years divisible by 4 are a leap year
            month_table = {1:31, 2:29,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}

    else:
        # year is not divisible by 4 so cannot be a leap year
        month_table = {1:31, 2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
    
    #remember that the month value may either be set to 1 for January or 3 for March
    current_month = month

    for month_check in range(current_month,13):
      if  remainder_days < month_table[month_check]:  #We have fewer days remaining than a full month (equal would mean it is next month, as it is an offset from 1)
         # we know the month, so can set that
         month=month_check
         # we add the remaining days to 1, the start day
         day+=remainder_days
         break
      else:
         remainder_days = remainder_days - month_table[month_check]

    # Change to datetime.datetime(year,month,day) to use test suite
    return (year, month, day)

spreadsheet_number = int(input("Enter spreadsheet number: "))
date=find_date_manual(spreadsheet_number)
print(f'Date (DD/MM/YYYY): {date[2]}/{date[1]}/{date[0]}')

#test suite
#
#print(find_date_manual(149808))
#print(datetime.datetime(1990,1,1)+datetime.timedelta(days=149808))

# Test script
#throw an error if out calculation is different from the system calculation
#for x in range(1,10000000):
#   assert find_date_manual(x) == (datetime.datetime(1990,1,1)+datetime.timedelta(days=x))
