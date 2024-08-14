import os

# Load the necessary functions from PyOxidizer
load("@pyoxidizer//:python_distribution.bzl", "python_distribution")

# Define the Python distribution
python_dist = python_distribution(
    name = "my_python_app",  # Name of your Python distribution
    default_config = "default",  # Default configuration
)

# Get the current directory
current_dir = os.getcwd()

# Create the Python executable
exe = python_dist.to_python_executable(
    name = "attempt3-app",  # Name of your executable
    packaging_policy = "pyoxidizer_packaged",  # Packaging policy
)

# Add your files to the executable
exe.add_python_file(path = os.path.join(current_dir, "attempt3.py"), install_location = "attempt3.py")
exe.add_python_file(path = os.path.join(current_dir, "large_exam_venues.xlsx"), install_location = "large_exam_venues.xlsx")
exe.add_python_file(path = os.path.join(current_dir, "large_invigilators.xlsx"), install_location = "large_invigilators.xlsx")

# Create a file manifest and add the Python resource
files = FileManifest()
files.add_python_resource(".", exe)
