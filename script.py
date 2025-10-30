import os


def create_project_structure():
    # Define the project structure
    directories = [
        "backend/api",
        "backend/models",
        "backend/repositories",
        "backend/services",
        "backend/schemas",
        "backend/mappers",
        "backend/tasks",
        "backend/core",
        "backend/tests",
        "frontend/public",
        "frontend/src/components",
        "frontend/src/pages",
        "frontend/src/services",
        "frontend/src/store",
        "frontend/src/assets",
        "frontend/src/utils",
        "docs",
    ]

    # Create each directory
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")


if __name__ == "__main__":
    create_project_structure()
