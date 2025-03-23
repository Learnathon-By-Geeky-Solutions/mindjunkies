---
name: Reduce Code Complexity
about: Report and track code complexity improvements
title: "[Refactor] Reduce Complexity"
labels: ''
assignees: ''

---

title: "[Refactor] Reduce Complexity in `<file>`"
labels: [refactor, technical-debt, complexity]
assignees: 
  - ShafayetSadi
body:
  - type: markdown
    attributes:
      value: |
        **This issue is for reducing complexity in a file where SonarCloud or other analysis tools detected high cyclomatic complexity.**

  - type: input
    id: file_path
    attributes:
      label: File Path
      description: "Specify the file that needs complexity reduction."
      placeholder: "e.g., `accounts/models.py`"

  - type: textarea
    id: complexity_reason
    attributes:
      label: Current Complexity Issue
      description: "Explain why this file has high complexity (e.g., too many conditionals, deeply nested loops, etc.)"
      placeholder: "Example: The `create_user` function has multiple conditionals, increasing cyclomatic complexity."
    validations:
      required: true

  - type: textarea
    id: suggested_fixes
    attributes:
      label: Suggested Fixes
      description: "Provide possible ways to refactor and simplify the code."
      placeholder: "Example: Extract the logic into separate functions, reduce redundant conditions, use Django’s built-in methods."

  - type: textarea
    id: expected_outcome
    attributes:
      label: Expected Outcome
      description: "Describe the expected benefit of this refactoring."
      placeholder: "Example: Reduced SonarCloud complexity score, improved readability, easier maintenance."

  - type: dropdown
    id: priority
    attributes:
      label: Priority Level
      description: "How urgent is this refactoring?"
      options:
        - High (Blocking Issue)
        - Medium (Needs Fix Soon)
        - Low (Can be Improved Later)
      default: 1
