#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Git Bot
# Copyright (c) 2008-2020 Hive Solutions Lda.
#
# This file is part of Hive Git Bot.
#
# Hive Git Bot is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Git Bot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Git Bot. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import os
import shutil

import appier

from . import base

class Replica(base.GitBotBase):

    origin_url = appier.field(
        immutable = True,
        meta = "url",
        description = "Origin URL"
    )

    target_url = appier.field(
        immutable = True,
        meta = "url",
        description = "Target URL"
    )

    branches = appier.field(
        type = list
    )

    @classmethod
    def validate(cls):
        return super(Replica, cls).validate() + [
            appier.not_null("origin_url"),
            appier.not_empty("origin_url"),
            appier.is_url("origin_url"),

            appier.not_null("target_url"),
            appier.not_empty("target_url"),
            appier.is_url("target_url"),

            appier.not_null("branches"),
            appier.not_empty("branches")
        ]

    @classmethod
    def list_names(cls):
        return ["id", "origin_url", "target_url", "branches"]

    def post_delete(self):
        base.GitBotBase.post_delete(self)
        if os.path.exists(self.repo_path):
            shutil.rmtree(self.repo_path, ignore_errors = True)

    @appier.operation(name = "Sync")
    def sync(self):
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

        if self.is_repo_new:
            appier.Git.clone(self.origin_url, path = self.base_path)
            appier.Git.add_upstream(self.target_url, path = self.repo_path)

        appier.Git.fetch(flags = ["--all"], path = self.repo_path)
        appier.Git.pull(flags = ["--all"], path = self.repo_path)

        for branch in self.branches:
            if not branch in appier.Git.get_branches(names = True, path = self.repo_path):
                appier.Git.checkout(
                    branch = "origin/" + branch,
                    flags = ["-b", branch],
                    path = self.repo_path
                )
            appier.Git.checkout(branch = branch, path = self.repo_path)
            appier.Git.pull(flags = ["--all"], path = self.repo_path)

        appier.Git.push(flags = ["upstream", "--all"], path = self.repo_path)
        appier.Git.push(flags = ["upstream", "--tags"], path = self.repo_path)

    @appier.operation(name = "Rebuild")
    def rebuild(self):
        if os.path.exists(self.repo_path):
            shutil.rmtree(self.repo_path, ignore_errors = True)
        self.sync()

    @appier.operation(
        name = "Set Origin URL",
        parameters = (("Origin URL", "origin_url", str),)
    )
    def set_origin_url(self, origin_url):
        self.origin_url = origin_url
        self.save(immutables_a = False)
        self.rebuild()

    @appier.operation(
        name = "Set Target URL",
        parameters = (("Target URL", "target_url", str),)
    )
    def set_target_url(self, target_url):
        self.target_url = target_url
        self.save(immutables_a = False)
        self.rebuild()

    @property
    def base_path(self):
        base_path = appier.conf("REPOS_PATH", "repos")
        base_path = os.path.abspath(base_path)
        base_path = os.path.normpath(base_path)
        return base_path

    @property
    def repo_path(self):
        repo_path = os.path.join(self.base_path, self.repo_name)
        repo_path = os.path.abspath(repo_path)
        repo_path = os.path.normpath(repo_path)
        return repo_path

    @property
    def repo_name(self):
        origin_url_p = appier.legacy.urlparse(self.origin_url)
        basename = os.path.basename(origin_url_p.path)
        if basename.endswith(".git"): return basename[:-4]
        return basename

    @property
    def is_repo_new(self):
        if not os.path.exists(self.repo_path): return True
        if not (name for name in os.listdir(self.repo_path) if not name in (".git",)): return True
        return False
