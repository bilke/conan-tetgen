#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class LibnameConan(ConanFile):
    name = "tetgen"
    version = "1.5.0"
    url = "https://github.com/bilke/conan-tetgen"
    description = "Keep it short"

    # Indicates License type of the packaged library
    license = "AGPLv3"

    # Packages the license for the conanfile.py
    exports = ["LICENSE"]

    # Remove following lines if the target lib does not use cmake.
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"

    # Custom attributes for Bincrafters recipe conventions
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def source(self):
        source_url = "https://github.com/ufz/tetgen"
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)


    def build(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self.build_subfolder)
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="license", src=self.source_subfolder)
        self.copy(pattern="*.h", dst="include")
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        if self.settings.os == "Windows":
            self.copy(pattern="*.exe", dst="bin", keep_path=False)
        else:
            binfolder = os.path.join(self.build_subfolder, self.source_subfolder)
            self.copy(pattern=binfolder + "/tetgen", dst="bin", keep_path=False)


    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
