
print('yow')

import dataclasses as d
from collections.abc import Iterable


for k, v in d.__dict__.items():
    if isinstance(v, Iterable) and not isinstance(v, str):
        print( 'Key: ', k)
        for vv in v:
           print( vv )
        print()
    else:
        print( 'Key: ', k, ' Value: ', v )
        print()


        
from math import log, floor, ceil
from functools import partial

nl = print



class bitlist( list ):
    """List of 'binary' ints.  They have collective context/state in that
       leading zeros are significant ( 'false' ) for bitints
       but are just zeros ints."""

    @property
    def max_length(self):
        """Bit length of largest int element in the list"""
        return max(max(self).bit_length(), 1)
    
    @property
    def make_bit_mask( self ):
        """ Bit_mask of binary ones with max length in collection
            of 'binary' ints. Inverting leading 0 to 1 is significant."""
        return int(str( '1'* self.max_length), base=2)
    
    def form( self, x:int ):
        return format(x, 'b').zfill(self.max_length)


def bit_length( bint ):
    """ bint is binary view of int.
        For bitmask purposes, a zero is FALSE
        and not just no value and has length 1.
    """
    
    if bint is None or not isinstance(bint, int): return 0
    if bint == 0: return 1 # unlike Py bit_length()
    lb = log(bint,2)
    lbi = int(lb)
    if lb == lbi: 
        return lbi+1
    return ceil(lb)


""" Comparison of bit integers"""


""" Possible for the log func to blow up with large numbers, 2^1000 or so ?"""

def one_of( x:int, y:int ):
    """Only one of x in y. """
    if x == 0: return False
    return log((x & y), 2) == floor(log((x & y), 2))

def morethanone_of( x:int, y:int ):
    """More than one of x in y. """
    if x == 0: return False
    return log((x & y), 2) != floor(log((x & y), 2))
    
def all_of( x:int, y:int ):
    """All of x in y"""
    if x == 0: return False 
    return x & y == x

def any_of( x:int, y:int ):
    """Any of integer x in y. """
    return x & y > 0

def none_of( x:int, y:int ):
    """None of x in y."""
    return x & y == 0

"""Basic operations on bit integers"""

def diff( x:int, y:int ):
    """( 1, 0 ) or ( 0, 1 ), but not both nor neither ( XOR )"""
    return x ^ y

def match( x:int, y:int ):
    """When same, (1 ,1 )"""
    return x & y
    
def invert( x:int ):
    """Logical complement, not '~' which is arithmetic"""
    return x ^ make_bit_mask(x)

def make_bit_mask( x:int, blength=1 ):
    """Need to partial make_bit_mask with max length of collection
       of 'binary' ints."""
    return int(str( '1'* max(x.bit_length(), blength)), base=2)

def bform( x:int, maxblen=None ):
    """Partial for maxblen""" 
    return format(x, 'b').zfill(maxblen or x.bit_length())

# print('log ', log(1,2 ))

a = int(0b11101100000111)
b = int(0b10000000000000)
c = int(0b11100000000000)
d = int(0b00001111000000)
z = int(0b00000000000000)

# need aggregate for context

nl()
print('bit_length a: ', bit_length(a))
print('bit_length b: ', bit_length(b))
print('bit_length c: ', bit_length(c))
print('bit_length d: ', bit_length(d))
print('bit_length z: ', bit_length(z))
print('bit_length 4.3: ', bit_length(4.3))
print('bit_length None: ', bit_length(None))
nl()

blist = bitlist( [z, z, z, z] )
print('blist max_length: ', blist.max_length)
print('blist make_bit_mask: ', blist.form(blist.make_bit_mask))

bbform = partial( bform, maxblen=blist.max_length)  

blist = bitlist( [a, b, c, d] )
print('blist max_length: ', blist.max_length)
print('blist make_bit_mask: ', blist.form(blist.make_bit_mask))

bbform = partial( bform, maxblen=blist.max_length)
make_bit_mask = partial( make_bit_mask, blength=blist.max_length)  # override, implies state

nl()
print('a: ', bbform(a))
print('b: ', bbform(b))
print('c: ', bbform(c))
print('d: ', bbform(d))
print('z: ', bbform(z))
nl()

print('one_of(b,a): ', one_of(b,a))
print('one_of(d,a): ', one_of(d,a))
print('one_of(z,a): ', one_of(z,a))
print('one_of(a,a): ', one_of(a,a))
print('one_of(b,b): ', one_of(b,b))
nl()
print('morethanone_of(b,a): ', morethanone_of(b,a))
print('morethanone_of(d,a): ', morethanone_of(d,a))
print('morethanone_of(z,a): ', morethanone_of(z,a))
print('morethanone_of(a,a): ', morethanone_of(a,a))
print('morethanone_of(b,b): ', morethanone_of(b,b))
nl()
print('all_of(b,a): ', all_of(b,a))
print('all_of(c,a): ', all_of(c,a))
print('all_of(d,a): ', all_of(d,a))
print('all_of(a,a): ', all_of(a,a))
print('all_of(z,z): ', all_of(z,z))
nl()
print('any_of(c,b): ', any_of(c,b))
print('any_of(d,b): ', any_of(d,b))
print('any_of(a,a): ', any_of(a,a))
print('any_of(z,a): ', any_of(z,a))
print('any_of(z,z): ', any_of(z,z))
nl()
print('none_of(d,c): ', none_of(d,c))      
print('none_of(d,a): ', none_of(d,a))
print('none_of(a,a): ', none_of(a,a))
print('none_of(z,a): ', none_of(z,a))
print('none_of(z,z): ', none_of(z,z))
nl()
print('diff(d,b): ', bbform(diff(d,b)))      
print('diff(d,a): ', bbform(diff(d,a)))
print('diff(a,a): ', bbform(diff(a,a)))
print('diff(z,a): ', bbform(diff(z,a)))
print('diff(z,z): ', bbform(diff(z,z)))
nl()
print('match(d,b): ', bbform(match(d,b)))      
print('match(d,a): ', bbform(match(d,a)))
print('match(a,a): ', bbform(match(a,a)))
print('match(z,a): ', bbform(match(z,a)))
nl()
print('a:         ', bbform(a))
print('invert(a): ', bbform(invert(a)))
print('b:         ', bbform(b))      
print('invert(b): ', bbform(invert(b)))
print('z:         ', bbform(z)) 
print('invert(z): ', bbform(invert(z)))
nl()
print('match( a , invert(a)): ', match( a , invert(a)))
print('any_of( a, invert(a)):   ', any_of( a, invert(a)))
print('none_of( a, invert(a)):   ', none_of( a, invert(a)))
nl()

# print(int(1*a.bit_length()))
# print('invert string: ', int(str( '1'* a.bit_length()))) 
#print('int str literal: ', str('1'* a.bit_length())) 
#print(int(str( '1'* a.bit_length())))

#print('inverse(int(0b111111111111111)): ', bbform(inverse(int(0b111111111111111))))

print(bform(int(0b0101011101111001110001110)))
print(bform(invert(int(0b0101011101111001110001110)), 24))
# print('bf will print 23 blen, lose leading 0->1')
print(bform(invert(int(0b0101011101111001110001110))), '   blength becomes 23')

