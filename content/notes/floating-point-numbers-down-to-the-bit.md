---
Category: Science
Tags: numerics, python
Date: 28 May 2011
---

# Floating Point Numbers, Down to the Bit


### Floating Point Memory Format ###

The general idea behind floating point numbers is the same as behind scientific
notation: write a mantissa, combined with an exponent to move the decimal
point. E.g. $1.093 \times 10^5 = 10^5 \sum_{k=0}^3 a_k 10^{-k}$ with $a_k =
1,0,9,3$. The exact same thing can be done in binary:

$$
v = 2^e \sum_{k=0}^{n-1} a_k 2^{-k}
$$

In memory, floats can be stored by reserving a section of the total available
bits to store the exponent, while the mantissa is stored in the remaining bits.
For a double precision float, the total size is 64 bit. One bit is used to
encode the sign of the number, 11 bits for the exponent, and the remaining 52
bits for the mantissa. In order to only have to store positive integers as
exponents, as fixed bias exponent of 1023 is subtracted from the stored
exponent. Also, the digit $a_0$ is assumed to be 1, and is not stored
explicitly in the mantissa; the effective number of mantissa digits is
therefore 53. For details, see the Wikipedia article for the [Double precision
floating-point format][1]. The [Single precision floating-point format][2] is
very similar, but only uses 32 total bits.

[1]: http://en.wikipedia.org/wiki/Double_precision_floating-point_format
[2]: http://en.wikipedia.org/wiki/Single_precision_floating-point_format


### Parsing Double Precision Floats in Python ###

It is relatively easy to parse a binary representation of a double precision
float. I've written a python script to do so (both for double and single
precision), available on [Github][3].

Given a representation (as a hex string) or a float value (as a string like
"1.2" or "-2.3456e-192") the scripts decompose the binary representation into
sign, exponent, and mantissa, and print out this information along with the exact
decimal the binary representation corresponds to according to the floating
point model.

A similar online tool for double precision floats is available at
[binaryconvert.com][4] (also [single precision][5] and [others][6]).


The key routine:

```python
BIAS = 1023                # constant to be subtracted from the stored exponent
SIGN_BIT = 63              # bit index at which the sign is stored
EXP_BIT = 52               # bit index at which the exponent starts
EXP_MASK = 0x000fffffffffffff  # bit-mask to remove exponent, leaving mantissa
NAN_EXP = 0x7ff            # special exponent which encodes NaN/Infinity

def parse_hex(hexstring, float_format='%.15e', no_decimal=False):
    """ Take a 8-byte hex string (16 digits) representing a double precision,
        parse it, and print detailed information about the represented float
        value.
    """
    bits = int('0x%s' % hexstring, 16)
    sign = '+1'
    if test_bit(bits, SIGN_BIT) > 0:
        sign = '-1'
    bits = clear_bit(bits, SIGN_BIT)
    stored_exp = bits >> EXP_BIT
    mantissa = bits & EXP_MASK # mask the exponent bits

    print ""
    print "Bytes         = 0x%s" % hexstring
    print "Float         = "+ float_format \
                           % struct.unpack('!d', hexstring.decode('hex'))[0]
    print "Sign          = %s" % sign
    if stored_exp == 0:
        print "Exponent      = 0x%x (Special: Zero/Subnormal)" % stored_exp
        print "Mantissa      = 0x%x" % mantissa
        if not no_decimal:
            if mantissa == 0:
                print "Exact Decimal = %s0" % sign[0]
            else:
                print "Exact Decimal = %s (subnormal)" \
                    % float2decimal(hex2float(hexstring))
    elif stored_exp == NAN_EXP:
        print "Exponent      = 0x%x (Special: NaN/Infinity)" % stored_exp
        print "Mantissa      = 0x%x" % mantissa
        if not no_decimal:
            if mantissa == 0:
                print "Exact Decimal = %sInfinity" % sign[0]
            else:
                print "Exact Decimal = NaN"
    else:
        print "Exponent      = 0x%x = %i (bias %i)" % (stored_exp,
                                                       stored_exp, BIAS)
        print "Mantissa      = 0x%x" % mantissa
        if not no_decimal:
            mantissa = set_bit(mantissa, EXP_BIT) # set the implicit bit
            print "Exact Decimal = %s 2^(%i) * [0x%x * 2^(-52)]" \
                                % (sign[0], stored_exp-BIAS, mantissa)
            print "              = %s" % float2decimal(hex2float(hexstring))
```

The procedure is quite straightforward:

* Extract the sign from the left-most bit, and set it to 0
* Extract the stored exponent by shifting out the mantissa; to get the actual
  exponent the bias exponent (1023) has to be subtracted
* Extract the mantissa by setting all bits of the exponential to 0 with a
  suitable bitmask

Any float can be represented as an exact decimal, without loss of information.
The calculating of the exact decimal is not completely trivial to implement.
The basic idea is to double the mantissa until it is a (possibly very large)
integer. A routine `float2decimal` that does this is available in
the [FAQ for the Decimal module][7].


[3]: https://github.com/goerz/float_parsers
[4]: http://www.binaryconvert.com/convert_double.html
[5]: http://www.binaryconvert.com/convert_float.html
[6]: http://www.binaryconvert.com/index.html
[7]: http://docs.python.org/release/2.5.2/lib/decimal-faq.html

### Connection to the Fortran Numerical Model ###

In Fortran, the numerical model is described as follows (see the [Fortran
Handbook][8] section 13.2.3):

$$
x = s b^e \sum_{k=1}^p f_k b^{-k}
$$

Note that in good Fortran fashion, the index $k$ counts from 1 as opposed to 0.
This means that the exponential $e$ is shifted by one compared to the more
traditional formula used in the "Floating Point Memory Format" section above.

The specific parameters for single and double precision for a given
compiler/system can be found using the very useful [kindfinder utility][8]. On
my system, I get the following:

    FLOATINGPOINT MODEL (Real/Complex):
     Name:                     Single              Double              Extnd1
     KIND:                          4                   8                  16
     DIGITS:                       24                  53                 113
     RADIX:                         2                   2                   2
     MINEXPONENT:                -125               -1021              -16381
     MAXEXPONENT:                 128                1024               16384
     PRECISION:                     6                  15                  33
     RANGE:                        37                 307                4931
     EPSILON:               1.192E-07           2.220E-16           1.926E-34
     HUGE:                  3.403E+38           1.798+308          1.190+4932
     TINY:                  1.175E-38           2.225-308          3.362-4932


Looking at double precision floats, the `DIGITS` corresponds to the total
number of mantissa digits, $p$ in the model. Note that `DIGITS` is 53, whereas
only 52 bits are used to store the mantissa in memory format: the 53rd bit for
$2^0$ is implicit, as discussed earlier.

`TINY` and `HUGE` are the smallest and largest representable numbers,
respectively. The `parse_dp_float.py` script gives the following information:

For `TINY`:

    Bytes         = 0x0010000000000000
    Float         = 2.225073858507201e-308
    Sign          = +1
    Exponent      = 0x1 = 1 (bias 1023)
    Mantissa      = 0x0
    Exact Decimal = + 2^(-1022) * [0x10000000000000 * 2^(-52)]
                  = 2.225073858507201383090232717332404064219215980462331830553327
    416887204434813918195854283159012511020564067339731035811005152434161553460108
    856012385377718821130777993532002330479610147442583636071921565046942503734208
    375250806650616658158948720491179968591639648500635908770118304874799780887753
    749949451580451605050915399856582470818645113537935804992115981085766051992433
    352114352390148795699609591288891602992641511063466313393663477586513029371762
    047325631781485664350872122828637642044846811407613911477062801689853244110024
    161447421618567166150540154285084716752901903161322778896729707373123334086988
    983175067838846926092773977972858659654941091369095406136467568702398678315290
    680984617210924625396728515625E-308

For `HUGE`:

    Bytes         = 0x7fefffffffffffff
    Float         = 1.797693134862316e+308
    Sign          = +1
    Exponent      = 0x7fe = 2046 (bias 1023)
    Mantissa      = 0xfffffffffffff
    Exact Decimal = + 2^(1023) * [0x1fffffffffffff * 2^(-52)]
                  = 17976931348623157081452742373170435679807056752584499659891747
    680315726078002853876058955863276687817154045895351438246423432132688946418276
    846754670353751698604991057655128207624549009038932894407586850845513394230458
    323690322294816580855933212334827479782620414472316873817718091929988125040402
    6184124858368

Note the `MINEXPONENT = EXPONENT(TINY)` and `MAXEXPONENT = EXPONENT(HUGE)`,
where `EXPONENT` is the Fortran function that returns the exponent in the
Fortran numerical model. These values are shifted by one compared to the stored
exponent in the binary representation, due to the sum in the numerical model
starting at one, as discussed above.

The `PRECISION` is the number of significant digits (the digits after the
decimal point) that are guaranteed to be represented accurately; That is,
when you assign a number to a double precision float, the number actually
stored will always match the assigned number within at least 15 significant
digits.

The `RANGE` is defined as `INT(MIN( LOG10(HUGE), -LOG10(TINY) ))`, in this case
`RANGE = INT(-LOG10(2.225e-308)) = INT(- (308 + 0.347)) = INT(307.653) = 307`.

Finally, `EPSILON` is the difference between one and the next closest
representable number, given as $2^{-52}$. This is the smallest difference for
any two neighboring numbers greater than one. `0.5*EPSILON` provides an upper
bound for the relative error due to rounding.


Some final observations:

*   Two distinct double precision numbers can look the same when printed to 15
    significant digits. The best example for this is `one + EPSILON(one)`.
    However, they will always differ in the 16th significant digit in that case.

*   When printing a float to an arbitrary precision (greater the machine
    precision), there are never any random digits printed. The exact
    decimal encoded by the float determines the result. However, the digits
    beyond the machine precision resulting from a *computation* involving two
    floats may depend and the compiler and the environment so that in general,
    results obtained on different systems cannot be expected to match beyond the
    machine precision.

*   To test whether two floats `r1` and `r2` are the same within some relative
    error `delta_r`, the following expression can be used:

    ```fortran
    approx_eq = (ABS(r1 - r2) <= 0.5d0*ABS(r1+r2) * delta_r)
    ```

    It makes no sense to use a `delta_r < 1.0d-16`; the test would be equivalent
    to a direct comparison on the bit-level.

*   To write out the hex representation of a double precision float `r` in
    Fortran, use `write(*,'(Z16)') transfer(r, 1_8)`.

*   Read [What Every Computer Scientist Should Know about Floating Numbers][10]

[8]: http://portal.acm.org/citation.cfm?id=151166
[9]: http://www.unics.uni-hannover.de/zzzzwg1/kindfind.f90
[10]: http://download.oracle.com/docs/cd/E19957-01/806-3568/ncg_goldberg.html
