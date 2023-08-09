
"""

Bit Buddy

Ones-complement wrapper for Python standard twos-complement logic,
mostly useful for debugging and displaying an int or BitInt in
binary form, and learning about the binary integer approach to logic.

Runs on Python 3.9 and micropython v1.20.0 on a Pico.

Note: There is another Python project called 'bitbuddy', but it hasn't
  seen any activity in 10 years so I'm grabbing the name.

module:
bitbuddy

version:
about 0.3

sourcecode:
https://github/billbreit/hello-world

copyleft:
2023 by Bill Breitmayer
       
licence:
GNU GPL v3 or above
      
author:
Bill Breitmayer
    
"""

from math import log, floor, ceil

try:
    from functools import partial
except:
    # Ported from the MicroPython library
    def partial(func, *args, **kwargs):
        """Creates a partial of the function"""

        def _partial(*more_args, **more_kwargs):
                local_kwargs = kwargs.copy()
                local_kwargs.update(more_kwargs)
                return func(*(args + more_args), **local_kwargs)

        return _partial


nl = print
DEBUG = False


class BitBuddyError(Exception):
    pass
    


class BitInt(object):
    """BitInt wraps an inner int with bitwise logical functions only,
       no arithmetic functions.  This class is mostly for debugging
       and would not be deployed outside development. """  

    def __init__(self, an_integer, *args, **kwargs ):
    
        super().__init__(*args, **kwargs)

        if an_integer <= ~0:
            raise BitBuddyError('Negative values and `0 ( minus zero ) are not BitInt numbers.')

        self._int = int(an_integer)
        
    def int(self, other):
        """ Type scrubbing, bit kludgy but necessary"""
        if isinstance(other, BitInt):
            return other._int
        else:
            return int(other)


    def __and__(self, other ):
        """Bitwise AND of x & y """
        return self._int & self.int(other)
            
    def __iand__(self, other):
        """x = iand(x, y) is equivalent to x &= y
           Alters the vaule of underlying _int """
        self._int &= self.int(other)
            
    def __or__(self, other):
        """Bitwise OR of x | y."""
        return self._int | self.int(other)
            
    def __ior__(self, other):
        """x = ior(x, y) is equivalent to x |= y.
           Alters the vaule of underlying _int """
        self._int |= self.int(other)
        
    def __xor__(self, other):
        """Bitwise XOR of x ^ y, either x or y but not x & y"""
        return self._int ^ self.int(other)
            
    def __ixor__(self, other):
        """x = ixor(x, y) is equivalent to a ^= b.
           Alters the vaule of underlying _int """
        self_int ^= self.int(other)
        
    def __invert__(self ):
        """Bitwise inverse ~x ( tilde x ) of the number x.
        
           Note non-standard ones-complment implementation:
           
           bin(12) is '0b1100'
           bin(~12) is '-0b1101', negative binary
           invert(12) is '0b0011'
           
           Twos-complement works fine and is more efficient,
           but ones-complement is easier to debug.

        """
        
        if self._int==0: return 1  
        
        return invert(self._int) 
        
    def __lshift__( self, offset):
        """x shifted left by offset, x<< y."""
        return self._int << offset
        
    def __ilshift__(self, offset):
        """x = lshift(x, y) is equivalent to x <<= y.
           Alters the vaule of underlying _int """
        self._int <<= offset
        
    def __rshift__(self, offset):
        """x shifted right by offset, x >> y."""
        return self._int >> offset
        
    def __irshift__( self, offset):
        """x = rshift(x, y) is equivalent to x >>= y.
           Alters the vaule of underlying _int """
        self._int >>= offset
                    

    def __iter__(self):
        """Returns a list of 1/0 values representing the sequence of bits set
           in the underlying integer.
           
           ex. the comprehension [ v for v in iter(11) ] where 11 = '0b1011'
           would return the sequence [1, 1, 0, 1 ], reversed from 'b' format.
           The expression:

                numb = 0
                for i, v in enumerate([1, 1, 0, 1 ]):
                        if v == 1:
                                numb |= pow(2, i )
                print(numb)
                
                will recover the int(11).
        
             
         """ 

        # print('iter- for self ', self)
        # print('iter- bin(self) ', bin(self))
        # print('iter- bit_length ', self.bit_length)
        nl()

        for bindex in range(self.bit_length):
        
            # print('iter- bindex ', bindex)
            test = pow( 2, bindex ) & self
            if test == 0:
                    yield 0
            else:
                        yield 1
                            
    @property
    def bit_length( self ):
        return bit_length(self)
            
    @property
    def num_bits_set(self):

        bl = [ v for v in iter(self) ]
        #print('nbs ', bl)
        #print('nbs ' , bl.count(1))
        return bl.count(1)
    
    @property       
    def bin(self):
        return bin(self._int)
                            
                    
            
bitint = BitInt 


class BitList( list ):
    """Basically, a formatter for a list of 'binary' ints, implementing 
       max_length ( max length some 'ones complement' functions. The int
       in the list have a context/state ( max_length ) in that leading
       zeros are significant even if 'false/0', but are just 'not there'
       for a single 0-value integer.
     """

    @property
    def max_length(self):
        """Bit length of largest int element in the list"""
        
        try:
            return max(max(self).bit_length(), 1)
        except:  # upython  
            max_len = max([ bit_length(i) for i in self ]) 
            return max(max_len, 1)           
    
    def make_bit_mask( self ):
        """ Bit_mask of binary ones with max length in collection
                of 'binary' ints. Inverting leading 0 to 1 is significant."""
        # return int(str( '1'* self.max_length), base=2)
        return int(str( '1'* self.max_length), 2)
    
    def form( self, x:int ):
            
        try:
            return zfill(x, 'b').zfill(self.max_length)
        except: # upython
            return zfill(x, self.max_length)
                    
bitlist = BitList


def zfill(x, maxlen=None):
    """ Make string of 1/0 for int x, filling zeros to left.
            For upython, dumb but nails it and can also work as
            zfill of last resort."""
    
    if maxlen is None: return None
    
    s = []
    for i in range(maxlen):
            if x << i == 0:
                    s.insert(0, '0')
            else:
                    s.insert(0, '1') 
                     
    return ''.join(s)
                                    
                                    


def bit_length( bint ):
    """ bint is binary view of int.
            For bitmask purposes, a zero is FALSE
            and not just no value and has length 1.
    """
    
    if bint is None or not isinstance(bint, int):
            return 0
    if bint == 0:
       return 1 # unlike Py bit_length()
       
    lb = log(bint,2)
    lbi = int(lb)
    if lb == lbi: 
            return lbi+1
    return ceil(lb)


def make_bit_mask( x:int, blength=1 ):
    """Need to partial make_bit_mask with max length of collection
       of 'binary' ints."""
    return int(str( '1'* max(bit_length(x), blength)), 2)

def bform( x:int, maxblen=None ):
    """Formatter for bitint types, with maxblen option."""
    # print('bform ', x, maxblen ) 
    try:
            return format(x, 'b').zfill(maxblen or x.bit_length())
    except: # upython
            return zfill(x, maxblen)


""" Comparison of Bitwise Integers"""


""" Possible for the log func to blow up with large numbers, 2^1000 or so ?"""

def one_of( x:int, y:int ):
    """Only one of x in y. """
    if x == 0: return False
    t = log((x & y), 2)
    return t == floor(t)

def morethanone_of( x:int, y:int ):
    """More than one of x in y. """
    if x == 0: return False
    t = log((x & y), 2)
    return t != floor(t)
    
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
    """Like all_of, but returns value rather than bool"""
    return x & y
    
def invert( x:int ):
    """Logical ones-complement, not '~' which sets neg. bit"""
    # must be partialled with bitlength 
    
    if x == ~0: return 0
    if x == 0: return 1
    
    return x ^ make_bit_mask(x)


if __name__=='__main__':

    nl()
    nl()
    print('==================================')
    print("=== Test Script for 'bitbuddy' ===")
    print('==================================')
    nl()
    
    def bit_info(bint):
            print('bint ', bint)
            print('type(bint) ', type(bint))
            print('bint.bin ', bint.bin)
            print('bint.bit_length ', bint.bit_length)
            print('bint.num_bits_set ', bint.num_bits_set)
            nl()
    
    
    nl()
    print('=== Test BitInt Class ===')
    nl()
    
    print('bi = bitint(25)')
    nl()
    bi = bitint(25)
    
    print('dir(bi) ', dir(bi))
    nl()
    bit_info(bi)
    print('isinstance(bi, int) ', isinstance(bi, int))
    nl()
    
    itest = bitint(33) # not working
    # itest = 33
    
    print('Test non-destructive dunder methods')
    nl()
    print('bi and itest ', bi.bin, itest.bin)
    nl()
    
    print('bi & itest', bi & itest)
    print('bi | itest', bi | itest)
    print('bi ^ itest', bi ^ itest, bin(56))
    print('bi << 1 ', bi << 1, bin(50))
    print('bi >> 1 ', bi >> 1, bin(12))
    nl()
    
    print('Test destructive dunder methods')
    nl()
    print('Invalid syntax. Commented out for now. may get rid of.')
    nl() 
    
    """
    print('bi &= itest', bi &= itest)
    bi = bitint(25)
    print('bi |= itest', bi |= itest)
    bi = bitint(25)
    print('bi ^= itest', bi ^= itest)
    bi = bitint(25)
    print('bi <<= 1', bi <<= 1)
    bi = bitint(25)
    print('bi >>= 1', bi >>= 1)
    nl()
    bi = bitint(25)
    """

    
    bit_info(bitint(0))
    bit_info(bitint(255))
    bit_info(bitint(333315))
    nl()

    print('try bitint(44) + 23')
    nl()
    x = bitint(44)
    try:
        y = x + 23
    except Exception as e:
        print(e)
    nl()
    
    print('try x = bitint(-1)  ')
    nl()
    
    try:
        x = bitint(-1 )
    except BitBuddyError as e:
        print(e)
        nl()
    
    
    print('try x = bitint(-111)  ')

    try:
        x = bitint(-111 )
    except BitBuddyError as e:
        print(e)
        nl()
    else:
        print('No Error')
        nl()
    

    print('Test for bi.__iter__')
    nl()
    print('bin(bi) ', bi.bin)
    print('bi.bit_length ', bi.bit_length)
    print('bi.num_bits_set ', bi.num_bits_set)
    nl()
    for bindex in iter(bi):
            print('__iter__ func returned ', bindex)
    nl()
    
    ilist = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight' ]
    
    print('Mapping BigInt to a list', ilist)
    
    o = int(0b01010101)
    e = int(0b10101010)
    
    odd_index = bitint( o )
    even_index = bitint( e )
    
    print('odd_index ', odd_index, '  ', odd_index.bin)
    print('even_index ', even_index, even_index.bin)
    print('Note the bit lengths of odd and even are ', odd_index.bit_length, even_index.bit_length)  
    print('odd_index.num_bits_set  ',  odd_index.num_bits_set)
    print('even_index.num_bits_set ',  even_index.num_bits_set)
    nl()
    
    xx = odd_index.num_bits_set
    print('xx ', xx)
    print('xx ', type(xx))
    nl()
    

    print('Use iter(odd_index) ', odd_index.bin ,' to fetch odds from list') 
    nl()
    
    olist = []
    for i, v in enumerate(iter(odd_index)):
        print('odds', v)
        if v == 1:
                olist.append(ilist[i])
    nl()
                    
    print('Use iter(even_index) ', even_index.bin, ' to fetch evens from list') 
    nl()
            
    elist = []      
    for i, v in enumerate(iter(even_index)):
        print('even', v)
        if v == 1:
                elist.append(ilist[i])
    nl()
                    
            
    print('odds ', olist)
    print('evens ', elist)
    nl()

    
    
    print('Functions')
    nl()
    a = int(0b11101100000111)
    b = int(0b10000000000000)
    c = int(0b11100000000000)
    d = int(0b00001111000000)
    o = int(0b00000000000001)
    z = int(0b00000000000000)
    
    print('bit_length')
    nl()
    print('bit_length a: ', bit_length(a))
    print('bit_length b: ', bit_length(b))
    print('bit_length c: ', bit_length(c))
    print('bit_length d: ', bit_length(d))
    print('bit_length z: ', bit_length(z))
    print('bit_length 4.3: ', bit_length(4.3))
    print('bit_length None: ', bit_length(None))
    nl()
    
    print('bitlist class ')
    nl()

    blist = bitlist( [z, z, z, z] )
    print('blist ', blist )
    print('blist max_length: ', blist.max_length)
    print('blist make_bit_mask: ', blist.form(blist.make_bit_mask()))
    nl()

    bbform = partial( bform, maxblen=blist.max_length) 
    
    print('new blist ', blist )  

    blist = bitlist( [a, b, c, d] )
    print('new blist ', blist )     
    print('blist max_length: ', blist.max_length)
    print('blist make_bit_mask: ', blist.form(blist.make_bit_mask()))
    nl()

    bbform = partial( bform, maxblen=22)
    
    nl()
    print('bbform - partial bform ', bbform)

    pmake_bit_mask = partial( make_bit_mask, blength=blist.max_length) 
    nl()
    print('bbform(22)')
    nl()
    print('a: ', bbform(a))
    print('b: ', bbform(b))
    print('c: ', bbform(c))
    print('d: ', bbform(d))
    print('z: ', bbform(z))
    nl()

    bbform = partial( bform, maxblen=blist.max_length)
    pmake_bit_mask = partial( make_bit_mask, blength=blist.max_length)  

    nl()
    print('bbform(blist.max_length)')
    nl()
    print('a: ', bbform(a))
    print('b: ', bbform(b))
    print('c: ', bbform(c))
    print('d: ', bbform(d))
    print('z: ', bbform(z))
    nl()
    
    print('one_of x in  y') 
    nl()
    print('one_of(b,a): ', one_of(b,a))
    print('one_of(d,a): ', one_of(d,a))
    print('one_of(z,a): ', one_of(z,a))
    print('one_of(a,a): ', one_of(a,a))
    print('one_of(b,b): ', one_of(b,b))
    nl()
    
    print('morethanone_of x in  y, detect conflict') 
    nl()
    print('morethanone_of(b,a): ', morethanone_of(b,a))
    print('morethanone_of(d,a): ', morethanone_of(d,a))
    print('morethanone_of(z,a): ', morethanone_of(z,a))
    print('morethanone_of(a,a): ', morethanone_of(a,a))
    print('morethanone_of(b,b): ', morethanone_of(b,b))
    nl()
    
    print('all_of x in y, logical AND ')
    nl()
    print('all_of(b,a): ', all_of(b,a))
    print('all_of(c,a): ', all_of(c,a))
    print('all_of(d,a): ', all_of(d,a))
    print('all_of(a,a): ', all_of(a,a))
    print('all_of(z,z): ', all_of(z,z))
    nl()
    
    print('any_of x in y, logical OR ')
    nl()
    print('any_of(c,b): ', any_of(c,b))
    print('any_of(d,b): ', any_of(d,b))
    print('any_of(a,a): ', any_of(a,a))
    print('any_of(z,a): ', any_of(z,a))
    print('any_of(z,z): ', any_of(z,z))
    nl()
    
    print('none_of x in y - logical NAND')
    nl()
    print('none_of(d,c): ', none_of(d,c))      
    print('none_of(d,a): ', none_of(d,a))
    print('none_of(a,a): ', none_of(a,a))
    print('none_of(z,a): ', none_of(z,a))
    print('none_of(z,z): ', none_of(z,z))
    nl()
    
    print('diff between x and y - logical XOR')
    nl()
    print('diff(d,b): ', bbform(diff(d,b)))      
    print('diff(d,a): ', bbform(diff(d,a)))
    print('diff(a,a): ', bbform(diff(a,a)))
    print('diff(z,a): ', bbform(diff(z,a)))
    print('diff(z,z): ', bbform(diff(z,z)))
    nl()
    print('match() returning int of matches, similar to all_of')
    nl()
    print('match(d,b): ', bbform(match(d,b)))      
    print('match(d,a): ', bbform(match(d,a)))
    print('match(a,a): ', bbform(match(a,a)))
    print('match(z,a): ', bbform(match(z,a)))
    nl()

    
    print('To Invert Or Not ')
    nl()
    
    print('Invert combined with logical functions ') 
    print('match( a , invert(a)): ', bbform(match( a , invert(a))))
    print('any_of( a, invert(a)):   ', any_of( a, invert(a)))
    print('none_of( a, invert(a)):   ', none_of( a, invert(a)))
    nl()
    
    print('The Reason We Invert')
    nl()
    print('a:         ', bbform(a))
    print('invert(a): ', bbform(invert(a)))
    print('b:         ', bbform(b))      
    print('invert(b): ', bbform(invert(b)))
    print('z:         ', bbform(z)) 
    print('invert(z): ', bbform(invert(z)), 'pythonically wrong, but right for bitint or in blist')
    print('bool(invert(z)): ', bool(invert(z)))
    nl()
    
    print('Compare ones to twos complement Python')
    nl()
    print('~0: ', ~0)
    print('~0 == 1: ', ~0 == 1)
    print('bin(~0) ', bin(~0))
    print('bool(~0) ', bool(~0))
    print('bool(bin(~0)) ', bool(bin(~0)))
    print('invert(0) ', invert(0))
    print('invert(~0) ', invert(~0))
    print('Beware inverting python logical ~0 !' )
    nl()

    print('bform again, with some manipulations.')
    nl()
    print(bform(int(0b0101011101111001110001110)))
    print(bform(invert(int(0b0101011101111001110001110)), 24))
    # print('bf will print 23 blen, lose leading 0->1')
    print(bform(invert(int(0b0101011101111001110001110))), '   blength becomes 23')
    nl()
    
    print('bitlength(0) ', bit_length(0))
    print('bitlength(1) ', bit_length(1))
    print('max(bit_length(0), 1) ', max(bit_length(0), 1))
    print('make_bit_mask(0) ', bin(make_bit_mask(0)))
    print('0^make_bit_mask(0) ', bin(0^make_bit_mask(0)))
    print('0^make_bit_mask(0, blength=4) ', bin(make_bit_mask(0, blength=4)))
    nl()
                    
    print('The End.')
    nl()
    
    

