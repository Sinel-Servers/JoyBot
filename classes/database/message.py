# JoyBot - Discord Bot
# Copyright (C) 2020 - 2021 Dylan Prins
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.
# If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>.

# You may contact me at admin@sinelservers.xyz

import json
from time import time

from classes.exceptions import NoDataError
from classes.database import Database
from classes.database.guild import Storage
from functions import quotify


class Message(Database):
    """ High-level management of message database """

    def __init__(self, user_id: int, msg_id: int):
        super().__init__("joybot_main")
        if user_id is not None:
            self.user_id = user_id
            self.msg_id = msg_id
            self.msgdata = self._loadmsgs()

    def _loadmsgs(self):
        """ Update/load all the message data """
        if not self._table_exists("message"):
            self._make_table("message", [("time", "INTEGER PRIMARY KEY"), ("user_id", "INTEGER"), ("base64", "TEXT")])

        lookup = self._lookup_record("message", f"user_id = {self.user_id}")

        if not lookup:
            self._add_record("message", [("time", str(int(time()))), ("user_id", self.user_id), ("base64", "'e30='")])
            lookup = "e30="
        else:
            lookup = lookup[0][-1]

        return json.loads(Storage(lookup).un_base64())

    def _commit(self):
        """ Commit all the message data to the databse """
        self._update_record("message", [("time", str(int(time()))), ("base64", quotify(Storage(json.dumps(self.msgdata)).do_base64()))], f"user_id = {self.user_id}")

    def add(self, message_data):
        """ Add message data to a user

        :param message_data: The message data
        """
        self.msgdata[str(self.msg_id)] = message_data
        self._commit()

    def get(self):
        """ Get message data from a user

        :return: The message data
        """
        try:
            return self.msgdata[str(self.msg_id)]
        except KeyError:
            raise NoDataError

    def remove(self):
        """ Remove message data from a user

        :return: The message data
        """
        try:
            msgdata = self.msgdata[str(self.msg_id)]
            self.msgdata.pop(str(self.msg_id))
        except ValueError:
            raise NoDataError

        self._commit()
        return msgdata

    def list(self):
        """ Get list of message data for a user

        :return: List of all the pictures
        """
        return self.msgdata
