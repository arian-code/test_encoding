def grayScore2tour (tour_score_gray, no_of_cities, city_bits, verbose = False):
    ''' Converts stings of gray score to vaild tour
            Input:  
                    no_of_cities        = 6 
                    city_bits           = 3
                    tour_score_gray     = [0,1,0,1,1,0,1,1,1,0,0,0,0,1,0,0,1,1]
            Internal:
                    
                    tour_score_dec      = [3, 4, 5, 0, 3, 2]
                    tour_score_repair   = [3, 4, 5, 0, 6, 2]
                    tour_score_sort     = [0, 2, 3, 4, 5, 6]
            Output:
                    tour                = [3, 5, 0, 1, 2, 4]
                    errors              = 1
        #######
            Input:  
                    no_of_cities        = 6 
                    city_bits           = 3
                    tour_score_gray     = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            Internal:
                    tour_score_dec      = [5, 5, 5, 5, 5, 5]
                    tour_score_repair   = [5, 6, 7, 8, 9, 10]
                    tour_score_sort     = [5, 6, 7, 8, 9, 10]
            Output:
                    tour                = [0, 1, 2, 3, 4, 5]
                    errors              = 5
        #######
            Input:  
                    no_of_cities        = 6 
                    city_bits           = 3
                    tour_score_gray = [0,1,0,1,1,0,1,1,1,1,1,0,0,1,0,0,1,1] 
            Internal:
                    tour_score_dec      = [3, 4, 5, 4, 3, 2]
                    tour_score_repair   = [3, 4, 5, 6, 7, 2]
                    tour_score_sort     = [2, 3, 4, 5, 6, 7]
            Output:
                    tour                = [5, 0, 1, 2, 3, 4]
                    errors              = 2
    ''' 
    if verbose:
        print ("Random tour_score_gray   : " + str (tour_score_gray))
    tour_score_dec = score_gray2dec (tour_score_gray, no_of_cities, city_bits)
    if verbose:
        print ("Random tour_score_dec    : " + str (tour_score_dec))
    tour_score_repair, errors = repairTourScore (tour_score_dec)
    if verbose:
        print ("Random tour_score_repair : " + str (tour_score_repair))
    if verbose:
        tour_score_sort = tour_score_repair.copy()                      #not required
        tour_score_sort.sort()                                          #not required
        print ("Random tour_score_sort   : " + str (tour_score_sort) + " <- not req in python")     #not required
    tour = tourScore2Tour (tour_score_repair)
    return (tour, errors)



def tourScore2Tour (tour_score_repair):
    li=[]
    for i in range(len(tour_score_repair)):
          li.append([tour_score_repair[i],i])
    li.sort()
    tour = []
    for x in li:
          tour.append(x[1])
    return (tour)



def repairTourScore (tour_score_dec):
    ''' Repair tour score 
            Ex  IN:     tour_score_dec      = [2, 0, 0, 0, 1, 0, 0, 1, 3, 1] 
                OUT:    tour_score_repair   = [2, 0, 4, 5, 1, 6, 7, 8, 3, 9]
    '''
    errors=0    
    tour_score_repair = []
    for score in tour_score_dec:
        if score not in tour_score_repair:
            tour_score_repair.append(score)
        else:
            while ((score in tour_score_dec) or (score in tour_score_repair)):
                score = score + 1
            tour_score_repair.append(score)    
            errors = errors + 1
    return (tour_score_repair, errors)


def score_gray2dec(tour_gray, no_of_cities, city_bits):
    """Convert tour score from Gray to tour in decimal and return it."""
    tour_score_dec = []
    for i in range (no_of_cities):
        #print (i)
        #print (tour_gray[i*city_bits:(i+1)*city_bits])
        score_gray_list = (tour_gray[i*city_bits:(i+1)*city_bits])
        score_gray = intList2str (score_gray_list)
        score_bin = gray2binary(score_gray)
        #print (score_bin)
        score_dec = binary2decimal(score_bin)
        #print (score_dec)
        tour_score_dec.append(score_dec)
    return (tour_score_dec)




def binary2gray(n):
    """Convert Binary to Gray codeword and return it."""
    n = int(n, 2) # convert to int
    n ^= (n >> 1)
    return bin(n)[2:]
def gray2binary(n):
    """Convert Gray codeword to binary and return it."""
    n = int(n, 2) # convert to int
    mask = n
    while mask != 0:
        mask >>= 1
        n ^= mask
    return bin(n)[2:]
def binary2decimal(n):
    return int(n,2) 

def intList2str (int_list):
    """Convert list of int to a string of int and return it."""
    int_str = ""	
    for x in int_list: 
        int_str = int_str + str(x) 
    return (int_str)

