# Get assignment instructions

There are a set of commands that can be used to create the badge issues.


## Get Assignment

Example use case: making a badge issue

```
cspt getassignment | gh issue create -t 'next prepare work' -F -
```

The `-F` option of [`gh issue create`](https://cli.github.com/manual/gh_issue_create) 
allows specifying a file for the body of the issue, and `-` reads from stdin, or in this case the pipe. 

(makeupbadgeissue)=
### Create a badge issue for a specific date
Create a badge issue from instructions

```
cspt getassignment --type practice --date 2025-02-18 | gh issue create -t 'practice 2025-02-18' -F -
```


### Use instructions in PR issue
Put badge instructions into the PR comment, while creating a PR from the current branch

```
cspt getassignment --type practice --date 2025-02-18 | gh pr create -t 'practice 2025-02-18' -F -
```

### Details

```{eval-rst}
.. click:: cspt.cli:getassignment
   :prog: cspt getassignment
   :nested: full
   :commands:

```




## Get the most recent badge date

To get the date of the most recently posted badge of a given type, for 
example when creating issues for the title use `cspt getbadgedate`

```
pretitle="prepare-"$(cspt getbadgedate --prepare)
cspt getassignment --type prepare | gh issue create --title $pretitle --label prepare --body-file -
```

```{eval-rst}
.. click:: cspt.cli:getbadgedate
   :prog: cspt getbadgedate
   :nested: full
   :commands:

```