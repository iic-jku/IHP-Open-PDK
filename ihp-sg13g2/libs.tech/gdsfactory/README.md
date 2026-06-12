# GDSFactory: Programmatic Layout

[GDSFactory](https://gdsfactory.github.io/IHP/) provides a Python-based alternative to manual layout editors like KLayout. Instead of drawing geometries by hand, you write Python code to generate your layouts, which brings several advantages:

- **AI-assisted design**: generate layout code using AI tools, accelerating the design process.
- **Automated design**: parameterize and script your cells, enabling batch generation and design-space exploration.
- **Complex systems**: build hierarchical layouts programmatically, making it easier to create large-scale designs such as photonic or RF systems.
- **Reproducibility**: layouts defined as code are version-controlled, testable, and shareable.

Get started with the IHP GDSFactory plugin at https://gdsfactory.github.io/IHP/.

## Installation

We recommend `uv`

```bash
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Installation for users

Use python 3.11, 3.12 or 3.13. We recommend [VSCode](https://code.visualstudio.com/) as an IDE.

```
uv pip install ihp-gdfactory --upgrade
```

Then you need to restart Klayout to make sure the new technology installed appears.

### Installation for contributors


Then you can install with:

```bash
git clone https://github.com/gdsfactory/ihp.git
cd ubc
uv venv --python 3.12
uv sync --extra docs --extra dev
```

## Documentation

- [gdsfactory docs](https://gdsfactory.github.io/gdsfactory/)
- [IHP docs](https://gdsfactory.github.io/ihp/) and [code](https://github.com/gdsfactory/ihp)
