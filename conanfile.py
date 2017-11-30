#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class LibnameConan(ConanFile):
    name = "cpr"
    version = "1.3.0"
    url = "https://github.com/whoshuu/cpr"
    description = "C++ Requests: Curl for People, a spiritual port of Python Requests"
    license = "https://raw.githubusercontent.com/whoshuu/cpr/master/LICENSE"
    exports_sources = ["CMakeLists.txt", "LICENSE"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    requires = "libcurl/7.52.1@bincrafters/stable"
    generators = "cmake"

    def source(self):
        source_url = "https://github.com/whoshuu/cpr"
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, "sources")

    def build(self):
        cmake = CMake(self)

        tools.replace_in_file(
            'sources/cpr/CMakeLists.txt',
            '${CURL_LIBRARIES})',
            '${CONAN_LIBS})')

        cmake.definitions["USE_SYSTEM_CURL"] = True
        cmake.definitions["BUILD_CPR_TESTS"] = False
        cmake.definitions["CMAKE_BUILD_SHARED_LIBS"] = self.options.shared

        cmake.configure()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", src="sources")
        self.copy(pattern="*", dst="include", src="sources/include")
        self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
