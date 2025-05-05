

### 👥 2. Create a New Branch for Each Feature

Each user creates their own **feature branch**:

```bash
# Syntax
git checkout -b feature/short-descriptive-name

# Examples:
git checkout -b feature/user-authentication
git checkout -b feature/db-setup
git checkout -b feature/user-registration
```

---

### 🛠️ 3. Make Changes and Commit

Work on your files, then commit:

```bash
git add .
git commit -m "Implement registration route"
```

---

### 🔄 4. Push Branch to Remote Repo (e.g., GitHub)

Assuming the remote is already added (check with `git remote -v`):

```bash
git push origin feature/user-authentication
```

---

### 🔃 5. Merge to Main (Once Complete)

After code review, testing, and approval:

```bash
# Checkout to main
git checkout main

# Pull latest changes
git pull origin main

# Merge the feature branch
git merge feature/user-authentication

# Push the updated main
git push origin main
```

---

### 💡 Pro Tips

* Use a naming convention like `feature/`, `bugfix/`, `hotfix/`, or `chore/` for clarity.
* Create a `.gitignore` and make sure `venv/` is ignored.
* Optionally use pull requests (PRs) on GitHub to review code before merging.

---

Do you want a `.gitignore` template and remote setup commands too?
