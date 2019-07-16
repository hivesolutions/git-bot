#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Git Bot
# Copyright (c) 2008-2019 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2019 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import appier

class AdapterController(appier.Controller):

    def ensure_key(self, data = None):
        data = data or appier.request_json()
        key = data.get("key", None)
        key = self.field("key", key)
        key = self.request.get_header("X-Git-Key", key)
        expected = appier.conf("GIT_KEY", None)
        if not expected: return
        if key == expected: return
        raise appier.SecurityError(
            message = "Mismatch Git key"
        )
