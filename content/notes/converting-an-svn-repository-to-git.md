---
Category: Tech
Tags: git, svn
Date: 09 Aug 2009
---

# Converting an SVN repository to git

A few lines to convert a subversion repository in `SVNURL` to a repository
`GITNAME.git` which is accessible at `GITURL/GITNAME.git`.

This assumes to that you crated a `users.txt` file in the current directory.

This does not take care of the whole subversion branches/tags issue (you'd have
to add a few lines)

```bash
pushd .
git-svn clone SVNURL --authors-file=users.txt --no-metadata GITNAME
mkdir GITNAME.git
cd GITNAME.git
git --bare init
cd ..
cd GITNAME
git remote add origin GITURL/GITNAME.git
git push origin master
popd
rm -rf GITNAME
```
