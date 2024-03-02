# Todo

There are a set of commands that can be used to create the badge issues.


## Get Assignments 

Example use case:
```
sysgetassignment | gh issue create -t 'next prepare work' -F -
```

The `-F` option of [`gh issue create`](https://cli.github.com/manual/gh_issue_create) 
allows specifying a file for the body of the issue, and `-` reads from stdin, or in this case the pipe. 

```{eval-rst}
.. click:: cspt.cli:getassignment
   :prog: cspt getassignment
   :nested: full
   :commands:

```


## Get the most recent badge date

To get the date of the most recently posted badge of a given type, for 
example when creating issues for the title use `cspt getbadgedate`

```{eval-rst}
.. click:: cspt.cli:getbadgedate
   :prog: cspt getbadgedate
   :nested: full
   :commands:

```