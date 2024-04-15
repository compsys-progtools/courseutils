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
   :noindex:
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

## Calculate Grade 

the following is how you can compute most of your grade.  

This does not take into consideration any of the event bonuses, but you can add them to the badges.yml file if you think you'll have them or want to see the impact they would have. 


```
gh pr list -s all  -L 200 --json title,latestReviews,createdAt > badges.json
cspt badgecounts badges.json  > badges.yml
cspt earlybonus -y badges.json >> badges.yml
cspt grade badges.yml 
```

```{warning}
Your grade is not an *average* it is cumulative, so the grade this shows is not the grade you will get if you keep working as you have been, but the grade you will get if you do no more work. 
```

For more: 

```{eval-rst}
.. click:: cspt.cli:badgecounts
   :prog: cspt badgecounts
   :nested: full
   :commands:

```

```{eval-rst}
.. click:: cspt.cli:grade
   :prog: cspt grade
   :nested: full
   :commands:

```

```{tip}
copy and edit that `badges.yml` file to represent other scenarios and increase badge counts to see what 
your grade would be with more badges.
```