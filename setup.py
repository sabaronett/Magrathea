"""
Setup script for building Magrathea with C++ extension
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext


class CMakeExtension(Extension):
    def __init__(self, name):
        super().__init__(name, sources=[])


class MagratheaBuild(build_ext):
    """Custom build command that compiles the C++ executable"""
    
    def run(self):
        # Build the C++ executable
        self.build_magrathea()
        
        # Copy to package directory
        self.copy_executable()
        
        super().run()
    
    def build_magrathea(self):
        """Build the C++ Magrathea executable"""
        build_dir = Path(self.build_temp).absolute()
        build_dir.mkdir(parents=True, exist_ok=True)
        
        source_dir = Path(__file__).parent.absolute()
        
        print("Building Magrathea C++ executable...")
        
        # Run make in the source directory
        try:
            subprocess.check_call(['make', 'clean'], cwd=source_dir)
            subprocess.check_call(['make', '-B'], cwd=source_dir)
            print("Successfully built Magrathea C++ executable")
        except subprocess.CalledProcessError as e:
            print(f"Error building C++ executable: {e}")
            print("Make sure GSL library is installed:")
            print("  Ubuntu/Debian: sudo apt install libgsl-dev")
            print("  macOS: brew install gsl")
            raise
    
    def copy_executable(self):
        """Copy the built executable to the package directory"""
        source_dir = Path(__file__).parent.absolute()
        exe_name = 'planet.exe' if sys.platform == 'win32' else 'planet'
        source_exe = source_dir / exe_name
        
        if not source_exe.exists():
            raise FileNotFoundError(f"Executable not found: {source_exe}")
        
        # Determine target directory
        package_dir = Path(self.build_lib) / 'magrathea'
        package_dir.mkdir(parents=True, exist_ok=True)
        
        target_exe = package_dir / exe_name
        
        print(f"Copying {source_exe} to {target_exe}")
        shutil.copy2(source_exe, target_exe)
        
        # Make executable
        if sys.platform != 'win32':
            os.chmod(target_exe, 0o755)


# Read long description from README
long_description = ""
readme_path = Path(__file__).parent / "README.md"
if readme_path.exists():
    with open(readme_path, 'r', encoding='utf-8') as f:
        long_description = f.read()


setup(
    long_description=long_description,
    long_description_content_type="text/markdown",
    ext_modules=[CMakeExtension('magrathea._magrathea')],
    cmdclass={'build_ext': MagratheaBuild},
)
