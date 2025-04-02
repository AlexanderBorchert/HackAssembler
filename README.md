# Hack Assembler

A Python implementation of the Hack Assembler for converting **Hack Assembly code** into binary **machine code**.  
The assembler is designed as part of the [**Nand2Tetris course**](https://www.nand2tetris.org/). It translates `.asm`
files into `.hack` files that can run on the [**Hack CPU**](https://nand2tetris.github.io/web-ide/chip/).

---

## **Usage**

To use the assembler, provide a Hack assembly file (`.asm`) as input. The assembler will generate the corresponding
binary machine code (`.hack`) file in the same directory.

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

2. Install the program:
   ```bash
   pip install hackassembler
   ```

3. Run the assembler:
   ```bash
   hackassemble example.asm
   ```

4. The corresponding `example.hack` file will be created:
   ```hack
   0000000000000001
   1110110000010000
   0000000000000010
   1110000010010000
   0000000000000000
   1110001100001000
   ```

---

## **Project Structure**

```plaintext
HackAssembler/
├── hackassembler/
│   ├── assembler.py   # Assembler logic (high-level translation control)
│   ├── parser.py      # Parses `.asm` files into commands
│   ├── commands.py    # Dataclasses and Enums for assembly commands
│   ├── code.py        # Binary translation of commands
├── tests/
│   ├── test_assembler.py  # Tests for the assembler
│   ├── test_parser.py     # Tests for the parser
│   ├── test_code.py       # Tests for binary translation
│   ├── conftest.py        # Fixtures for testing
├── .pre-commit-config.yaml  # Pre-commit hooks for linting & formatting
├── pyproject.toml          # Project configuration (dependencies, metadata)
└── README.md               # Project readme (this file)
```

---

## **Requirements**

- **Python**: `>=3.9`
- Optional dependencies:
    - `mypy`: Static type checking
    - `pytest`: Testing framework
    - `ruff`: Linting & formatting
    - `setuptools`: Project packaging

---

## **Development**

Follow these steps to set up the project locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/AlexanderBorchert/HackAssembler.git
   cd hackassembler
   ```

2. **Install Dependencies**:
   Using pip:
   ```bash
   pip install -r requirements.txt
   ```

   Or, install the package using `pyproject.toml`:
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

### **Linting**

Code quality is enforced using `ruff` and type-checked with `mypy`. Run:

```bash
ruff check .
mypy .
```

To auto-fix formatting issues:

```bash
ruff --fix .
```
