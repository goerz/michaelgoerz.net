---
Category: Programming
Tags: fortran
Date: Oct 20, 2008
---

# Some Fortran String Gotchas

I ran into some problems the other day from a misunderstanding about how
passing strings works in fortran.

Consider the following program:

```fortran
program teststrings

  implicit none
  integer, parameter :: stringlength=100
  character (len=10) :: a
  character (len=10) :: b
  character (len=stringlength) :: c

  a = 'Hello'
  b = 'World'
  c = trim(a)//' '//trim(b)
  call printstring(c)
  call printstring(trim(a)//' '//trim(b))

contains

  subroutine printstring(s)
    character (len=stringlength) :: s ! this is a bug

    write (*,*) ""
    write (*,*) "len(s) = ", len(s)
    if (s == 'Hello World') then
    write (*,*) "s == 'Hello World' is True"
    else
    write (*,*) "s == 'Hello World' is False"
    end if

    write (*,*) 'trim(s) = "'//trim(s)//'"'
  end subroutine printstring

end program teststrings
```

The output of this program is the following:

```
len(s) =          100
s == 'Hello World' is True
trim(s) = "Hello World"

len(s) =          100
s == 'Hello World' is False
trim(s) = "Hello WorldS,AF(sdfl0qhahsd j
i2S.F*df"
```

However, if I change line 18 to

```fortran
character (len=*) :: s
```

I get this output:

```
len(s) =          100
s == 'Hello World' is True
trim(s) = "Hello World"

len(s) =           11
s == 'Hello World' is True
trim(s) = "Hello World"
```

This illustrates the following points:

* Inside subroutines, you must *always* declare string dummy parameters
  as `character (len=*)`. This is called 'assumed length' (cf. Fortran 90
  Handbook, section 12.5.1). The parameter will end up with the the same length
  as the variable or string that is passed to the subroutine. If you don't use
  `len=*`, you will run into problems if the string that you pass to the
  subroutine is shorter than what you declared for dummy parameter. Not
  observing this rule can easily introduce serious bugs into your program.
* String comparisons between strings of different length work like this: The
  shorter string is padded on the right with spaces until it matches the length
  of the longer string. Then, both strings are compared. (cf. Fortran 90
  Handbook, section 7.3.1.2). So, comparing strings of different length works,
  you don't have to use the trim function.
