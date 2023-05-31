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
#     spack install py-smartredis
#
# You can edit this file again by typing:
#
#     spack edit py-smartredis
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PySmartredis(PythonPackage):
    """A Python Interface for the SmartRedis Library Client"""

    homepage = "https://www.craylabs.org/docs/smartredis.html"
    pypi = "smartredis/smartredis-0.4.0.tar.gz"
    git = "https://github.com/CrayLabs/SmartRedis"

    maintainers("MattToast")

    version("0.4.0", sha256="d12779aa8bb038e837c25eac41b178aab9e16b729d50ee360b5af8f813d9f1dd")

    depends_on("python@3.8:3.10", type=("build", "run"))
    depends_on("py-setuptools@42:", type=("build",))
    depends_on("cmake@3.13:", type=("build",))
    depends_on("hiredis@1.0", type=("build", "link", "run"))
    depends_on("redis-plus-plus@1.3 cxxstd=17", type=("build", "link"))
    depends_on("py-pybind11@2.6", type=("build",))
    
    depends_on("py-numpy@1.18.2:", type=("build", "run"))

    patch("sr_0_4_0_no_deps.patch", when="@0.4.0")

    def setup_build_environment(self, env):
        spec = self.spec
        env.set("REDISPP_LIB_DIR", spec["redis-plus-plus"].prefix.lib64)
        env.set("REDISPP_INC_DIR", spec["redis-plus-plus"].prefix.include)
        env.set("HIREDIS_LIB_DIR", spec["hiredis"].prefix.lib)
        env.set("HIREDIS_INC_DIR", spec["hiredis"].prefix.include)
        env.set("PYBIND11_TOOLS", spec["py-pybind11"].prefix.share.cmake.pybind11)
 
