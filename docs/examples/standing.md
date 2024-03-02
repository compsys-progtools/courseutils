# Standing


(progressreport)=
## Get a Progress Report

First, get your PR info: 
```
gh pr list --state all --json title,latestReviews >> badges.json
```

Notes: 
- `--state all` is important to get both open and closed PRs
- `--json` is requires and `title, latestReviews` are the two requied attributes to that parameter, you can add additional ones though and for some features, additional ones are requires. 
- if you have more than 30 total PRs(PRs only, not issues) use the `--limit`/`-L` option with a number >= your total number of PRs.

Then use `cspt progressreport` to check which have been approved by a valid approver and have a badge keyword in them.

```
cspt progressreport badges.json
```

 Options allow you to control the format of the report. 

```{eval-rst}
.. click:: cspt.cli:progressreport
   :prog: cspt progressreport
   :nested: full
   :commands:

```

## Check PR Titles

### Check a single PR

```
cspt titlecheck -t 'title I am thinking about'
```


```{eval-rst}
.. click:: cspt.cli:titlecheck
   :prog: cspt titlecheck
   :nested: full
   :commands:

```


### Make a list of PRs to fix
This can check which titles will work with the grading calculation functions. 

```{eval-rst}
.. click:: cspt.cli:prfixlist
   :prog: cspt prfixlist
   :nested: full
   :commands:

```

### What counts?
Under the hood, the majority of the checking is done by this function: 

```{eval-rst}
.. automodule:: cspt.badges
   :members: is_title_gradeable
   :no-index:
```

## Check if Early bonus is met


```
gh pr list -s all --json title,latestReviews,createdAt  | cspt earlybonus -
```


```{eval-rst}
.. click:: cspt.cli:earlybonus
   :prog: cspt earlybonus
   :nested: full
   :commands:

```

