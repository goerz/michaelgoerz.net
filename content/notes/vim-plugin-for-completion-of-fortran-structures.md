---
Category: Programming
Tags: vim, fortran
Date: 18 Dec 2008
---

# Vim Plugin for Completion of Fortran Structures

I wrote a little plugin for vim that allows you to complete Fortran 90
structures by pressing F7.

<http://www.vim.org/scripts/script.php?script_id=2487>

The plugin in written in python, so you need to have your vim compiled with
python support in order to use it.

The intention is to complete "program", "type", "interface", "module",
"subroutine", "function", "do", and "select" constructs. You write the first
line of such a construct (e.g. "subroutine foo(a, b)", then press F7, and the
script will add the closing line "end subroutine foo" and put the cursor
between the two lines, indented by one level.

[1]: http://www.vim.org/scripts/script.php?script_id=2487
