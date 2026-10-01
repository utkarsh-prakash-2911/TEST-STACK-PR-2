# TEST-STACK-PR-2

The purpose of this repository is to demonstrate the functions of **Stacked PRs** —
building a series of small, dependent pull requests that stack on top of one another
rather than one large change.

## Language

This project is written in **Python**.

## Project layout

```
.
├── src/stackpr/        # Python package used in the demos
├── tests/              # Unit tests
├── .github/
│   ├── workflows/      # CI workflows
│   └── CODEOWNERS      # Required reviewers for PRs to main
└── README.md
```

## Running the tests

```bash
python -m pytest
```

## Contributing

All pull requests target `main` and require approval from the designated
code owner before they can be merged. See [.github/CODEOWNERS](.github/CODEOWNERS).
