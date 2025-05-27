# Documentation

This directory contains the documentation for the Monty Extension Specification, built using [MkDocs](https://www.mkdocs.org/) with the [Material](https://squidfunk.github.io/mkdocs-material/) theme.

## Project Structure

```console
.
├── model/                  # Core model documentation
├── examples/              # Example implementations
│   ├── reference-events/
│   ├── gdacs-events/
│   └── ...
├── styles/               # Custom CSS styling
├── scripts/             # Setup and utility scripts
├── mkdocs.yml           # MkDocs configuration
└── pyproject.toml       # Python project dependencies
```

## Setting up locally

1. Create a Python virtual environment and install dependencies:

```bash
./scripts/setup.sh
```

2. Start the documentation server:

```bash
source .venv/bin/activate
mkdocs serve
```

The documentation will be available at [http://127.0.0.1:8000/]

## Building the documentation

To build the static site:

```bash
source .venv/bin/activate
mkdocs build
```

The built documentation will be in the `site` directory.

## Adding Documentation

The documentation is organized into several sections:

- **Model**: Core data model documentation (`model/`)
- **Examples**: Sample implementations and use cases (`examples/`)
- **Sources**: Information about different data sources (`model/sources/`)

To add new documentation:

1. Create your markdown file in the appropriate directory
2. Add the file to the navigation structure in `mkdocs.yml`
3. Use MkDocs features for enhanced content:
   - Code blocks with syntax highlighting
   - Mermaid diagrams for visualizations
   - Admonitions for important notes
   - Tables for structured data

## Previewing Changes

When you run `mkdocs serve`, the documentation will automatically reload when you make changes to any of the source files. This makes it easy to preview your changes in real-time.

## Style Guide

- Use markdown for all documentation files
- Include a table of contents for longer pages
- Use code blocks with appropriate language tags
- Add alt text to images
- Use relative links for internal references
- Follow the existing structure for consistency
