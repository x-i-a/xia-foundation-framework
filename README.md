# GCP Foundation
## Objects Relationship Maps
1. All application is installed on a foundation
2. Each application could have instance of modules
3. Before module is usable in each application, they must be enabled in foundation
```mermaid
graph TD
    F(Foundation) -->|Installs| A1(Application 1)
    F -->|Installs| A2(Application 2)
    F -->|Enables| M1(Module 1)
    F -->|Enables| M2(Module 2)
    F -->|Enables| M3(Module 3)

    A1 -->|Has Instance of| M1
    A1 -->|Has Instance of| M2
    A2 -->|Has Instance of| M2
    A2 -->|Has Instance of| M3
```

## GCP Foundation Introduction

## Usage
### Preparation

### Starting from scratch
make bigbang

### Foundation Operations
make create

### Module Operations
make init-module module_class=`module_class` package=`package`

### Application Operations
make create-app app_name=`application_name`
