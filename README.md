# Hack Assembler

A Python implementation of the Hack Assembler for converting **Hack Assembly code** into binary **machine code**.
The assembler is designed as part of the **Nand2Tetris course/project**, and it translates `.asm` files into `.hack`
files that can run on the Hack CPU.

## **Features**

- Parses `.asm` files with support for:
- Generates `.hack` machine code files.
- Modular, extensible code structure:
    - Separate `parser`, `assembler`, and `code` modules.
- Comprehensive test suite with `pytest`.

---

## **Project Structure**

```plaintext
HackAssembler/
├── src/
│   ├── assembler.py   # Assembler logic (high-level translation control)
│   ├── parser.py      # Parses `.asm` files into commands
│   ├── commands.py    # Dataclasses and Enums for assembly commands
│   ├── code.py        # Binary translation of commands
├── tests/
│   ├── test_assembler.py  # Tests for the assembler
│   ├── test_parser.py     # Tests for the parser
│   ├── test_code.py       # Tests for binary translation
│   ├── conftest.py        # Fixtures for testing
├── .pre-commit-config.yaml  # Pre-commit hooks for linting and formatting
├── pyproject.toml          # Project configuration (dependencies, metadata)
└── README.md               # Project readme (this file)
```

---

## **Requirements**

- **Python**: `>=3.9`
- Optional dependencies:
    - `mypy`
    - `pytest`
    - `ruff`
    - `setuptools`

All dependencies are managed through `pyproject.toml`.

---

## **Setup**

Follow these steps to set up the project locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/hack-assembler.git
   cd hack-assembler
   ```

2. **Install Dependencies**:
   Using pip:
   ```bash
   pip install -r requirements.txt
   ```

   Or using `pip` with `pyproject.toml`:
   ```bash
   pip install .
   ```

3. **Install Pre-commit Hooks** (optional but recommended):
   ```bash
   pre-commit install
   ```

4. **Run Tests**:
   To ensure everything is working:
   ```bash
   pytest
   ```

---

## **Usage**

To use the assembler, you can pass a Hack assembly file (`.asm`) as input. The assembler will generate the corresponding
machine code (`.hack`) file in the same directory.

### **Example**

1. Create a Hack assembly file, e.g., `example.asm`:
   ```asm
   // This file adds the numbers 1 + 2
   @1
   D=A
   @2
   D=D+A
   @0
   M=D
   ```

2. Run the assembler:
   ```bash
   python src/main.py example.asm
   ```

3. The corresponding `example.hack` file will be created:
   ```hack
   0000000000000001
   1110110000010000
   0000000000000010
   1110000010010000
   0000000000000000
   1110001100001000
   ```

---

## **Development**

### **Running Tests**

The project uses `pytest` for unit testing. Run all tests with:

```bash
pytest
```

### **Linting**

Code quality is enforced using `ruff` and type-checked with `mypy`. Run:

```bash
ruff check src/
mypy src/
```

To auto-fix formatting issues:

```bash
ruff --fix .
```

---
