from setuptools import setup, Extension
import sysconfig

python_include_dir = sysconfig.get_path('include')
python_lib_dir = sysconfig.get_config_var('LIBDIR')

if not python_lib_dir:
    python_lib_dir = r'C:\Users\toko\AppData\Local\Programs\Python\Python310\libs'  # Adjust path as needed

module = Extension(
    'apifn',
    sources=['apifn.c'],
    include_dirs=[
        '.', 
        python_include_dir,
        # Add any other necessary include paths
    ],
    library_dirs=[python_lib_dir],
    libraries=['python310'],  # Adjust the version as needed
    define_macros=[('SOME_MACRO', '1'), ('ANOTHER_MACRO', '1')],
    extra_compile_args=['/DWIN32', '/D_WINDOWS', '/W3'],
    language='c'
)

setup(
    name='apifn',
    version='1.0',
    description='Python C extension for Blakserv API',
    ext_modules=[module]
)
