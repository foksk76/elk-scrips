# Elasticsearch Administration Scripts

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.19.1-orange.svg)
![License](https://img.shields.io/badge/License-Apache_2.0-green.svg)

A collection of Python scripts for managing Elasticsearch clusters, with a focus on index operations and maintenance tasks.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Scripts](#scripts)
- [Usage Examples](#usage-examples)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Index Management**:
  - Unfreeze frozen indices
  - Reindex index range

## Requirements

- Python 3.6+
- Elasticsearch 8.19.1
- Required Python packages:
  
  ```text
  elasticsearch==8.15.1
  ```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/foksk76/elk-scripts.git
cd elk-scripts
```

### 2. Set Up Virtual Environment (Recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/MacOS
# .venv\Scripts\activate  # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Scripts

### `unfreeze_indices.py`

Unfreezes all frozen indices in the cluster.

**Usage**:

```bash
python unfreeze_indices.py [--host <HOST>] [--username <USERNAME>] [--password <PASSWORD>] [--verify-certs <VERIFY-CERTS>]
```

### `reindex_elasticsearch.py`

Reindex a range of indexes in Elasticsearch.

**Usage**:

```bash
python reindex_elasticsearch.py [--host <HOST>] [--username <USERNAME>] [--password <PASSWORD>] --start-index <START_INDEX> --end-index <END_INDEX> [--alias ALIAS] [--verify-certs VERIFY-CERTS]
```

## Usage Examples

### Basic Unfreeze Operation

```bash
python unfreeze_indices.py --host https://es-cluster:9200
```

### Basic Reindex Operation

```bash
python reindex_elasticsearch.py --host http://localhost:9200 --username elastic --password yourpassword --start-index fg-009783 --end-index fg-009789
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

### Coding Standards

- Follow PEP 8 guidelines
- Include docstrings for all functions
- Add unit tests for new features
- Update documentation when making changes

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
