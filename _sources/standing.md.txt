# Checking Course Standing

## Badges 

### Check a single badge

```{click} badges:verify_badge
---
prog: verifybadge
nested: full
---
```

### Get a report

First, get your PR info: 
```
gh pr list --state all --json title,latestReviews >> badges.json
```

If you have more than 30 total PRs use the `-limit` option with a number >= your total number of PRs.

Then use the package to verify and make a list of all: 

```{click} badges:process_badges
---
prog: verifyjson
nested: full
---
```


## KWL repo contents 

```{warning}
this may not be applicable in sp23
```

```{click} kwltracking:get_file_list
---
prog: kwlfilecheck
nested: full
---
```

```{click} kwltracking:count_files
---
prog: kwlfilecount
nested: full
---
```