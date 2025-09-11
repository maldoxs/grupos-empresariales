#
# Copyright (C) 2013 - 2022, Oracle and/or its affiliates. All rights reserved.
# ORACLE PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
#
import shutil
import subprocess
import sys
import warnings
from distutils.version import LooseVersion

from pathlib import Path
from setuptools import setup
from setuptools.command.install import install

SETUP_PATH = Path(__file__).resolve().parent
LIB_PATH = SETUP_PATH / "lib"
JARS_PATH = SETUP_PATH / "python" / "pypgx" / "jars"
WHLS_PATH = SETUP_PATH / "python"


def call_pip_install(package, local_inst, no_use_pep517=False, no_index=True, raise_exception=False):
    # --verbose: If users request verbose output on PyPGX installation,
    # they should get verbose output also for the dependency installations.
    # Otherwise, the subprocess output will not be shown to the user regardless of this.
    # --upgrade: To make sure we upgrade the package if a lower version exists
    # --no-index: To not use the installations from pypi.org
    # --find-links: To provide the package location
    local_inst = "--user" if local_inst else ""
    no_use_pep517 = "--no-use-pep517" if no_use_pep517 else ""
    no_index = "--no-index" if no_index else ""
    cmd_line = "{} -m pip install --verbose --upgrade {} {} {} {} --find-links {}".format(
        sys.executable, package, local_inst, no_use_pep517, no_index, WHLS_PATH
    )

    try:
        subprocess.check_call(cmd_line.split())
    except Exception:
        warnings.warn(
            "Error installing {}: Please ensure {} is correctly installed before installing PyPGX.".format(
                package, package
            )
        )
        if raise_exception:
            raise

try:
    for jar_file in LIB_PATH.iterdir():
        shutil.copy(jar_file, JARS_PATH)

    class InstallLocalPackage(install):
        """A class that installs the necessary libraries."""

        def run(self):
            """Install the necessary libraries."""
            install.run(self)

            if not sys.executable:
                warnings.warn("Empty sys.executable, can't install dependencies of PyPGX")
                return

            local_inst = "--user" in sys.argv

            # Install Cython which is required for pyjnius installation
            call_pip_install("Cython", local_inst)

            # Install pyjnius
            # Unlike Cython or pandas, we do not want to make the installation successful without pyjnius
            #
            # In addition to the flags above, we need --no-use-pep517 flag for pip>=19.0. For older
            # versions of pip, we do not need the flag (pep517 is not used by default).
            #
            # --no-index breaks for versions lower than 19.1.1.
            import pip; pip_version = pip.__version__  # this will be replaced with importlib.metadata.version from Python 3.8
            no_use_pep517 = LooseVersion(pip_version) >= LooseVersion("19.0")
            no_index = LooseVersion(pip_version) >= LooseVersion("19.1.1")
            call_pip_install("pyjnius", local_inst, no_use_pep517=no_use_pep517, no_index=no_index, raise_exception=True)

            # Install OPG4Py
            call_pip_install("opg4py", local_inst)

            # Install pandas
            call_pip_install("pandas", local_inst)

            # note: if python 3.6 or python 3.7 is used, the open CVE is present: CVE-2021-34141,
            # fixes are available in python 3.8
            if sys.version_info < (3, 8):
                warnings.warn(
                    "Python 3.6 and 3.7 support will be deprecated in future releases due to the presence of CVE (CVE-2021-34141)."
                )

    setup(name="pypgx",
        # allow installation for python 3.6 and 3.7
        # do not ship pandas support for python 3.6 and 3.7
        python_requires=">=3.6",
        version="22.3.1",
        description="PyPGX",
        url="PGX",
        platforms=["Linux x86_64"],
        license="OTN",
        long_description="PyPGX",
        packages=[
            "pypgx",
            "pypgx.api",
            "pypgx.api.auth",
            "pypgx.api.filters",
            "pypgx.api.frames",
            "pypgx.api.mllib",
            "pypgx.api.redaction",
            "pypgx.pg",
            "pypgx.pg.rdbms",
            "pypgx._utils",
            "pypgx.jars"
        ],
        package_dir={"pypgx": "python/pypgx"},
        package_data={"pypgx.jars": ["*.jar"], "pypgx.resources": ["*"]},
        cmdclass={"install": InstallLocalPackage}
        )

finally:
    for jar_file in LIB_PATH.iterdir():
        file_to_remove = JARS_PATH / jar_file.name
        file_to_remove.unlink()