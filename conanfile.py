from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import copy, collect_libs, rmdir
from conan.tools.scm import Git
import os

class CompressonatorConan(ConanFile):
    name = "compressonator"
    version = "master"  # May be overridden by set_version
    license = "MIT"
    url = "https://github.com/hfn92/compressonator"
    description = "Compressonator SDK for texture compression and analysis"
    topics = ("compression", "gpu", "textures", "sdk")
    settings = "os", "compiler", "build_type", "arch"
    package_type = "library"
    exports_sources = "CMakeLists.txt"
    no_copy_source = True

    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    def set_version(self):
        git = Git(self)
        commit = git.run("rev-parse --short HEAD").strip()
        self.version = commit if commit else "master"

    def layout(self):
        cmake_layout(self, src_folder="compressonator")

    def source(self):
        self.run("git clone --depth 1 --branch master https://github.com/hfn92/compressonator.git", cwd=self.source_folder)

    def generate(self):
        tc = CMakeToolchain(self)
        if self.settings.compiler in ["gcc", "clang"]:
            tc.variables["CMAKE_CXX_FLAGS"] = "-w"
        elif self.settings.compiler == "msvc":
            tc.variables["CMAKE_CXX_FLAGS"] = "/W0"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_script_folder=os.path.join(self.source_folder, "compressonator/build/sdk"))
        cmake.build(target="CMP_Compressonator")

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = collect_libs(self)
