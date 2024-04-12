# IFFT v1.0
Repository for tracking the development of "IFFT" tool for my "term paper".

**Brief Summary**: Reminds developers that a set of files should be edited together.
![ifft](https://github.com/thiagosantos0/TCC-UFMG/assets/55515126/efe3052e-ad43-4b7a-a8e7-fe708a9595b9)

# Usage
*Right now the usage modes are here just as an illustration. An investigative work of the viability of these modes is still required.*

# PyPi Package
```shell
ifft run
ifft change_pattern
ifft exit
```

# Hooks
```yaml
- repo: [https://github.com/thiagosantos0/IFFT](https://github.com/thiagosantos0/IFFT)
  # Version
  rev: v1.0.0
  hooks:
    # Run ifft
    - id: ifft
```

# Github Action
```yaml
name: IFFT 
on: [ push ]
jobs:
  ruff:  
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
```
