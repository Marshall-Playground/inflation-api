# Development Preferences

This file contains my development preferences and conventions. Please refer to these when making technical decisions and implementing features.

## 🛠️ Build & Development Tools

### Makefiles
- **Always include a Makefile** for common development tasks
- **Print commands before execution** using `@echo "Running: <command>"` 
- Include standard targets: `help`, `install`, `lint`, `format`, `test`, `typecheck`, `build`, `dev`, `server`, `clean`
- `build` target should run the full CI pipeline (lint + format + typecheck + test)
- Provide clear help documentation as the default target

### Dependency Management
- **Python**: Use `uv` for package management and virtual environments
- Prefer modern, fast tooling over legacy alternatives
- Lock dependencies for reproducible builds

## 🧪 Testing & Quality

### Testing Strategy
- **Comprehensive unit tests** are essential - add them even if the original project lacks them
- Achieve high test coverage (aim for 80%+)
- Include both unit tests and integration tests
- Test error cases and edge conditions thoroughly

### Code Quality Tools
- **Python**: Use `ruff` for both linting and formatting, `mypy` for type checking
- Configure tools in `pyproject.toml` when possible
- Use strict type checking settings
- Implement pre-commit hooks for automated quality checks

### API Testing
- **Always create HTTP request files** for manual API testing (`.http` files)
- Organize into logical categories: basic operations, examples, error cases
- Include comprehensive documentation on how to use the HTTP files
- Support multiple tools (VS Code REST Client, IntelliJ, curl, HTTPie)

## 🏗️ Architecture & Design

### Code Organization
- **Separation of concerns** is paramount - use clear architectural layers
- **Repository pattern** for data access abstraction
- **Service layer** for business logic
- **Dependency injection** for testability
- Use **abstract base classes** to define contracts

### Naming & Code Style
- **High-quality naming** - favor clarity over brevity
- **Focused, general-purpose functions** that do one thing well
- **Maximum maintainability** through clear structure and documentation
- Avoid unnecessary comments in code - prefer self-documenting code

### Error Handling
- **Comprehensive error handling** with custom exception hierarchies
- **Graceful degradation** - handle missing data and edge cases elegantly
- **Detailed error messages** that help users understand what went wrong
- Use appropriate HTTP status codes for API responses

## 🚀 Framework & Technology Preferences

### Python Web Development
- **FastAPI** for REST APIs - modern, fast, with automatic OpenAPI documentation
- **Pydantic** for data validation and serialization (use v2 syntax)
- **Async/await** patterns for I/O operations
- **Decimal** type for financial calculations requiring precision

### Development Workflow
- **Hot reload** in development environments
- **Automatic documentation** generation (Swagger/OpenAPI)
- **Configuration through environment variables** with sensible defaults
- **Health check endpoints** for monitoring

## 📊 Data & Precision

### Financial/Mathematical Operations
- Use **Decimal** type for financial calculations to avoid floating-point errors
- **Validate input ranges** and provide clear error messages
- **Document mathematical formulas** and business logic in code

### Data Loading & Validation
- **Graceful error handling** for data parsing - skip invalid rows with warnings
- **Comprehensive input validation** with detailed error messages
- **Lazy loading** patterns where appropriate for performance

## 🔧 Configuration & Setup

### Project Structure
- **Modern project structure** following language/framework conventions
- **Comprehensive documentation** including setup, usage, and API examples
- **Environment-specific configuration** files
- **Clear separation** between development and production settings

### Documentation
- **README.md** with clear setup and usage instructions
- **API documentation** with examples and error cases
- **HTTP request collections** for manual testing and exploration
- **Inline documentation** for complex business logic only

## 🎯 Development Philosophy

### Approach to Implementation
- **Start with planning** - break down complex tasks into manageable steps
- **Implement incrementally** - build and test each component thoroughly
- **Follow existing patterns** in the codebase when extending functionality
- **Modernize while migrating** - take opportunities to improve architecture

### Problem Solving
- **Understand the domain** before implementing solutions
- **Fix bugs in original implementations** when discovered during migration
- **Add missing functionality** that was specified but not implemented
- **Validate assumptions** through comprehensive testing

### Tool Selection
- **Prefer modern, actively maintained tools** over legacy alternatives
- **Choose tools with strong ecosystem support** and good documentation
- **Prioritize developer experience** - fast feedback loops, clear error messages
- **Consider long-term maintainability** in technology choices

---

*These preferences should guide technical decisions across all projects, regardless of language or framework. Adapt specific tools and patterns to the technology stack while maintaining these core principles.*