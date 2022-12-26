---
Category: Programming
Tags: fortran
Date: 19 May 2011 
---

# Advanced Array-Passing in Fortran

There are instances where one wishes to change the rank (the number of
dimensions) of an array as it is passed to a subroutine. Maybe you want to call
a library routine that expects to get a vector, but you have the data to be
passed stored in a matrix. There should be no problem in principle, as the data
for an array -- no matter its rank -- is stored sequentially in memory (array
element order of subscripts along the first dimension varying more quickly).
Thus, it should be possible to simply re-interpret the data to a different
shape. In practice, one can change the rank of the array by declaring the dummy
array with an explicit shape specification. As soon as the dummy array has an
explicit shape, one can pass anything that contains enough elements to fill the
dummy array, no matter what the rank or shape. The feature is known as array
element sequence association and is illustrated in the following example:

```fortran
program test
  implicit none
  integer :: test_array1(10)
  integer :: test_array2(10,2)
  test_array1 = (/1, 2, 3, 4, 5, 6, 7, 8, 9, 10/)
  test_array2(:,1) = (/1,   2,  3,  4,  5,  6,  7,  8,  9, 10/)
  test_array2(:,2) = (/11, 12, 13, 14, 15, 16, 17, 18, 19, 20/)
  write(*,*) "print_a(test_array1, 10)"
  call print_a(test_array1, 10)
  write(*,*) "print_a(test_array2, 10)"
  call print_a(test_array2, 10)
  write(*,*) "print_a(test_array2, 20)"
  call print_a(test_array2, 20)
  write(*,*) "print_a(test_array2(:,2), 10)"
  call print_a(test_array2(:,2), 10)
  write(*,*) "print_m(test_array1, 2,5)"
  call print_m(test_array1, 2, 5)

contains

  subroutine print_a(a, n)
    integer, intent(in) :: n
    integer, intent(in) :: a(n)
    integer :: i
    do i = 1, n
      write(*,*) a(i)
    end do
  end subroutine

  subroutine print_m(a, n, m)
    integer, intent(in) :: n
    integer, intent(in) :: m
    integer, intent(in) :: a(n,m)
    integer :: i, j
    do i = 1, n
      do j = 1, m
        write(*,*) a(i,j)
      end do
    end do
  end subroutine

end program test
```

There are two alternatives to do basically the same thing, one standard, one
not. The first one is known as assumed-size, and looks like this:

```fortran
subroutine print_a(a, n)
  integer, intent(in) :: a(*)
  integer, intent(in) :: n
  integer :: i
  do i = 1, n
    write(*,*) a(i)
  end do
end subroutine
```

Here, `a` has rank one, and a size large enough to fit whatever is passed to
the routine. However, the routine does not actually know the size of `a`
(`size(a)` is illegal in this context). There certainly is nothing that ensures
that the size of `a` is n, and the compiler has no way of perfoming any checks
on the use of `a`. In that sense, assumed-size is not very useful compared to
explicit-shape, except maybe in some rare instances where the array size can
somehow be deduced from the data stored in the array, so that the array size
`n` does not have to be passed along.

The second alternative is a non-standard trick that behaves identically to
assumed-size, but was used before the assumed-size feature was introduced to
Fortran. It looks like this:

```fortran
subroutine print_a(a, n)
  integer, intent(in) :: a(1)
  integer, intent(in) :: n
  integer :: i
  do i = 1, n
    write(*,*) a(i)
  end do
end subroutine
```

In principle, this is also an example of array element sequence association. In
the subroutine, `a` is called with subscripts outside of the bounds of its
declared size 1, which is more or less guaranteed to work since the array is
passed by reference. Again, the compiler has not idea about the actual size of
`a`. Most compilers will recognize this trick and not complain about going out
of bounds, even with bound-checking enabled, understanding `a(1)` to be
identical to `a(*)`, with the only difference being that `size(a)` is legal,
but of course returns 1, i.e. not the size of the actual passed array.
Declaring `a` as `a(2)` will not work, however.

Any of these definitions should only be used if the rank of the array needs to
be changed. For just passing arrays of identical rank, but unknown shape, one
should always use the assumed-shape syntax (e.g. `a(:,:)`)

A few pointers about where to find the discussed concepts in the Fortran 90
Handbook: array element order is discussed in section 6.4.7, the definition of
array element sequence association appears in section 12.5.2.1, and
explicit-shape, assumed-shape, deferred-shape, and assumed-size specification
are explained in section 5.3.1.

Thanks to the people on `comp.lang.fortran` for illuminating some of these
concepts to me.
