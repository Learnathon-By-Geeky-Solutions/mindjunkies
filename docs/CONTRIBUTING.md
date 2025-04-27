# 🤝 Contributing to BiddyaPeeth

First off, thank you for considering contributing to **BiddyaPeeth**!  
Your help is critical to make this Learning Management System even better.

We welcome contributions from everyone — whether you're fixing a typo, improving documentation, fixing a bug, or adding a new feature 🚀.

---

## 🧑‍💻 How to Contribute

Follow these steps to get started:

### 1. Fork the Repository

Click the "Fork" button at the top right of the [main repository](https://github.com/Learnathon-By-Geeky-Solutions/mindjunkies) page.

This creates a copy under your GitHub account.

---

### 2. Clone Your Fork

```bash
git clone https://github.com/your-username/mindjunkies.git
cd mindjunkies
```


### 3. Create a Feature Branch
Always create a new branch for your work:

```bash
git checkout -b feature/your-feature-name
```
Use a descriptive branch name like feature/add-user-profile, fix/login-bug, etc.

### 4. Install Dependencies
Make sure your environment is ready:
```bash
pip install uv
uv sync
```
Run database migrations:

```bash
python manage.py migrate
```

(Optional) Start Tailwind watcher:
```bash
python manage.py tailwind watch
```


### 5. Make Changes

- Follow **PEP8** coding standards.
- Use **Black** formatter (`black .`) before pushing.
- Validate HTML and CSS if you modify templates.
- Keep commit messages clear and meaningful.

Example commit:

```bash
git commit -m "Fix: Corrected login validation error"
```

### 6. Push Your Changes
```
git push origin feature/your-feature-name
```
### 7. Create a Pull Request (PR)
- Go to your fork on GitHub.
- Click "New Pull Request".
- Select your feature branch as the compare branch.
- Fill in the PR template carefully (description, screenshots if needed).
- Request a review from the maintainers.


### 📜 Pull Request Guidelines
- Target the develop branch, NOT the main branch.

- Ensure your branch is up-to-date with develop (git pull origin develop).

- Keep Pull Requests focused: one PR = one feature/fix.

- Write clear and concise PR titles and descriptions.

- Add tests if you add new features.

- Update documentation if needed.


### 🧹 Code Style Guidelines
- Python: Follow PEP8 and use Black (black .).
- Frontend: Follow Tailwind CSS best practices.
- Run pre-commit hooks locally before submitting PRs. 
- Keep code clean, avoid deep nesting, write readable functions.
