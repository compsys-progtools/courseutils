---

# **Tutorial: Customizing `getassignment.yml` in Your KWL Repo**

### **1. Open and edit your workflow file**

In your kwl repo, go to:

```
.github/workflows/getassignment.yml
```

This file controls what kinds of assignment issues (prepare/review/practice) will be created automatically when you run the workflow with **GitHub Actions**.

---

### **2. Choose which assignment types you want**

Inside the workflow, find the section:

```yaml
# prepare badge lines
pretitle="prepare-"$(cspt getbadgedate --prepare)
cspt getassignment --type prepare | gh issue create --title $pretitle --label prepare --body-file -
```

Prepare **must stay enabled**.

Then choose whether you also want *review* or *practice*:

```yaml
# review badge lines
#rtitle="review-"$(cspt getbadgedate --review)
#cspt getassignment --type review | gh issue create --title $rtitle --label review --body-file -
```

Uncomment to enable review.

```yaml
# practice badge lines
pratitle="practice-"$(cspt getbadgedate --practice)
cspt getassignment --type practice | gh issue create --title $pratitle --label practice --body-file -
```

Comment or uncomment based on what you want the workflow to create.

---

### **3. Save your changes and push them**

Commit your edited workflow file:

```
git add .github/workflows/getassignment.yml
git commit -m "Customize assignment types in getassignment workflow"
git push
```

GitHub will update the workflow automatically.

---

### **4. Run the workflow manually in GitHub**

Since the workflow runs only with `workflow_dispatch`, you must trigger it manually:

1. Go to your repo on GitHub
2. Click **Actions**
3. Select **Create badge issues (Do not run manually)**
4. Press **Run workflow**

This will execute the steps using the assignment types you selected.

---

### **5. Check your new assignment issues**

After the workflow finishes:

* Go to the **Issues** tab in your repo.
* You will see issues created automatically with titles like:

  * `prepare-2025-11-24`
  * `practice-2025-11-24`
  * (and review if enabled)

Each issue contains the assignment instructions retrieved from:

```
cspt getassignment --type <type>
```

---
