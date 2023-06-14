# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-smartsim
#
# You can edit this file again by typing:
#
#     spack edit py-smartsim
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

import os

from spack.package import *


class PySmartsim(PythonPackage):
    """A workflow library to easily integrate machine learning libraries with
    high performance computing simulations and applications
    """

    homepage = "https://www.craylabs.org/docs/overview.html"
    git = "https://github.com/CrayLabs/SmartSim"
    pypi = "smartsim/smartsim-0.4.2.tar.gz"

    maintainers("MattToast")

    version("0.4.2", sha256="ab632ff7d036e73822ddc5081fe85ea69c48d8be53ad0e6e487e9193eb3410f6")

    variant("torch", default=True, description="Build with the pytorch backend")
    variant("cuda", default=False, description="Use CUDA")
    variant("rocm", default=False, description="Use ROCm")

    depends_on("python@3.8:3.10", type=("build", "run"))
    depends_on("py-wheel", type=("build",))
    depends_on("py-setuptools", type=("build",))

    depends_on("py-psutil@5.7.2:", type=("build", "run"))
    depends_on("py-coloredlogs@10:", type=("build", "run"))
    depends_on("py-tabulate@0.8.9:", type=("build", "run"))
    depends_on("py-redis@4.5:", type=("build", "run"))
    depends_on("py-tqdm@4.56:", type=("build", "run"))
    depends_on("py-filelock@3.4:", type=("build", "run"))
    depends_on("py-protobuf@3.20:3", type=("build", "run"))

    # Companion libs
    depends_on("py-smartredis@0.4.0", type=("build", "run"), when="@0.4.2")

    # Backends
    depends_on("redis@7.0.5:", type=("build", "run"))

    depends_on("redis-ai@1.2.7:", type=("build", "run"))
    depends_on("redis-ai+cuda", type=("build", "run"), when="+cuda")
    depends_on("redis-ai+rocm", type=("build", "run"), when="+rocm")

    # ML Deps
    with when("+torch"):
        depends_on("redis-ai+torch", type=("build", "run"))
        depends_on("py-torch@1.11:", type=("build", "run"))
        depends_on("py-torch+cuda+cudnn", type=("build", "run"), when="+cuda")
        depends_on("py-torch+rocm", type=("build", "run"), when="+rocm")

    # Remove dangerous build functionality from spack install
    patch("dont-build-db.patch")
    patch("remove-cli-build-fns.patch")

    # Remove out-dated deps
    patch("remove-redis-py-cluster.patch", when="@0.4.2")

    @run_after("install")
    def symlink_bin_deps(self):
        ss_core_path = (self.prefix
                            .lib
                            .join("python3.10")
                            .join("site-packages")
                            .smartsim
                            ._core)
        os.symlink(self.spec["redis"].prefix.bin.join("redis-server"),
                   ss_core_path.bin.join("redis-server"))
        os.symlink(self.spec["redis"].prefix.bin.join("redis-cli"),
                   ss_core_path.bin.join("redis-cli"))
        os.symlink(self.spec["redis-ai"].prefix, ss_core_path.lib)
