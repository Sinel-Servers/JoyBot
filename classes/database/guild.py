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

# You may contact me at joybot@sinelservers.xyz

import json
from ast import literal_eval
from config import config
import pymongo
import functions
from classes.storage import Storage
from classes.exceptions import AlreadyCountedError, AlreadyBannedError, NoDataError


class Bump:
    """ High-level management of bump database """
    def __init__(self, guild_id: int, user_id: int = None):
        self.guild_id = guild_id
        self.user_id = user_id
        self.bumpDict, self.first_bump_id, self.streak_data = self._loadbumps()

    def _commit(self):
        """ Commits a change to the database """
        self._update_record("bump", [
                                        ("base64", functions.quotify(Storage(json.dumps(self.bumpDict)).do_base64())),
                                        ("first_bump_id", self.first_bump_id),
                                        ("streak_base64", functions.quotify(Storage(json.dumps(self.streak_data)).do_base64()))
                                     ],
                            f"guild_id = {self.guild_id}"
                            )

    def get_top(self, num: int = 1, raw: bool = False):
        """ Gets the top {num} entries.

        :param num: The top number to get
        :param raw: Whether to return just the top ID or the data too.
        :return: A list of tuples, if raw is off. Else a string of the top id
        """
        top = functions.sort_dict(self.bumpDict, num)
        if not top:
            return None
        if raw is True:
            return top[0]
        return top

    def get_pos(self):
        """ Gets the position of the person on the leaderboard

        :return: Integer of the person's position
        """
        toplist = [item for item in self.get_top(num=100000000) if item is not None]

        try:
            toplist = [int(listitem[0]) for listitem in toplist]
        except TypeError:
            return None

        try:
            return toplist.index(self.user_id)+1
        except ValueError:
            return None

    def get_total(self):
        """ Gets the bump total

        :return: Integer of the person's bump total
        """
        try:
            total = self.bumpDict[str(self.user_id)]
        except KeyError:
            total = 0

        return total

    def get_streak(self):
        """ Gets the current person's streak data

        :return: The current person's streak data
        """
        if str(self.user_id) in self.streak_data:
            return self.streak_data[str(self.user_id)]

        self.streak_data[str(self.user_id)] = (0, 0)
        return self.streak_data[str(self.user_id)]

    def get_streaker(self):
        """ Gets the current person with a streak

        :return: The current streaker's id, and their streak data
        """
        cur_streaker = self.streak_data["cur_streak"]
        cur_streaker_data = self.streak_data[cur_streaker]

        return cur_streaker, cur_streaker_data

    def add_total(self, amount: int = 1):
        """ Adds {amount} to the total

        :param amount: The amount to add to the total
        """
        if self.first_bump_id is None:
            self.first_bump_id = self.user_id

        # Bump totals

        if str(self.user_id) in self.bumpDict:
            self.bumpDict[str(self.user_id)] += amount
        else:
            self.bumpDict[str(self.user_id)] = 0
            self.bumpDict[str(self.user_id)] += amount

        # Streak
        if "cur_streak" not in self.streak_data:
            self.streak_data["cur_streak"] = ""

        if self.streak_data["cur_streak"] == str(self.user_id):
            self.streak_data[str(self.user_id)][0] += amount
            if self.streak_data[str(self.user_id)][0] > self.streak_data[str(self.user_id)][1]:
                self.streak_data[str(self.user_id)][1] = self.streak_data[str(self.user_id)][0]

        else:
            prev_streaker = self.streak_data["cur_streak"]
            try:
                prev_streaker_data = self.streak_data[prev_streaker]
                self.streak_data[prev_streaker] = (0, prev_streaker_data[1])
            except KeyError:
                pass

            self.streak_data["cur_streak"] = str(self.user_id)

            if str(self.user_id) not in self.streak_data:
                self.streak_data[str(self.user_id)] = (amount, amount)

            else:
                self.streak_data[str(self.user_id)] = (amount, self.streak_data[str(self.user_id)][1])

        self._commit()

    def remove_total(self, amount: int):
        """ Removes {amount} from the total

        :param amount: The amount to remove from the total
        """
        if str(self.user_id) in self.bumpDict:
            self.bumpDict[str(self.user_id)] -= amount

            if self.bumpDict[str(self.user_id)] <= 0:
                self.bumpDict.pop(str(self.user_id))

        self._commit()

    def reset_total(self):
        """ Resets the bump total of the user """
        if str(self.user_id) in self.bumpDict:
            self.bumpDict.pop(str(self.user_id))

        self._commit()

    def reset_guild_total(self):
        """ Resets the bump total of the entire guild """
        self.bumpDict = {}
        self._delete_record("bump", f"guild_id = {self.guild_id}")

    def get_first_bump(self):
        return self.first_bump_id


class Settings(Database):
    """ High-level management of settings databse """
    def __init__(self, guild_id: int):
        super().__init__("joybot_main")
        self.guild_id = guild_id
        self.settings = self._loadsettings()

    def _loadsettings(self):
        """ Update/load all the settings """
        if not self._table_exists("settings"):
            self._make_table("settings", [("guild_id", "INTEGER PRIMARY KEY"), ("base64", "TEXT")])

        lookup = self._lookup_record("settings", f"guild_id = {self.guild_id}")

        if not lookup:
            self._add_record("settings", [("guild_id", self.guild_id), ("base64", functions.quotify(Storage(json.dumps(config["DEFAULT_SETTINGS"])).do_base64()))])
            lookup = Storage(json.dumps(config["DEFAULT_SETTINGS"])).do_base64()
        else:
            lookup = lookup[0][1]

        return json.loads(Storage(lookup).un_base64())

    def _commit(self):
        """ Commits a change to the database """
        self._update_record("settings", [("base64", functions.quotify(Storage(json.dumps(self.settings)).do_base64()))], f"guild_id = {self.guild_id}")

    def get_setting(self, setting: str):
        """ Gets a certain setting

        :param setting: The setting to get the value of
        :return: The setting's value
        """
        return self.settings[setting]

    def get_all_settings(self):
        """ Gets all settings

        :return: The setting's value
        """
        return self.settings

    def set_setting(self, setting: str, value: str):
        """ Sets a settings' value

        :param setting: The setting to set the value of
        :param value: The value to set to the setting
        """
        self.settings[setting] = value
        self._commit()

    def reset_settings(self, regen=True):
        """ Reset the settings for a guild

        :param regen: Whether to regenerate the default settings
        """
        self._delete_record("settings", f"guild_id = {self.guild_id}")
        if regen:
            self._loadsettings()


class Counting:
    """ High-level management of counting databse """
    def __init__(self, guild_id: int):
        super().__init__("joybot_main")
        self.guild_id = guild_id

        if not self._table_exists("counting"):
            self._make_table("counting", [("guild_id", "INTEGER PRIMARY KEY"), ("channel", "INTEGER"), ("last_counted", "INTEGER"), ("count", "INTEGER")])

    def channel_get_id(self):
        """ Get the current counting channel id (if applicable)

        :return: None if no channel, otherwise current channel id
        """

        cur_data = self._lookup_record("counting", f"guild_id = {self.guild_id}")
        if len(cur_data) == 0:
            return
        return cur_data[0][1]

    def channel_set(self, channel_id: int):
        """ Set the counting channel

        :param channel_id: ID of the counting channel
        :return: Previous counting channel or false
        """
        cur_data = self._lookup_record("counting", f"guild_id = {self.guild_id}")
        if len(cur_data) == 0:
            self._add_record("counting", [("guild_id", self.guild_id),
                                          ("channel", channel_id), ("count", "0"),
                                          ("last_counted", "504030703264989194")])
        else:
            self._update_record("counting", [("channel", channel_id), ("count", "0"),
                                ("last_counted", "504030703264989194")], f"guild_id = {self.guild_id}")

    def add(self, user_id: int, amount: int = 1):
        """ Add to the current count

        :param user_id: ID of the user who counted
        :param amount: The amount to add
        :return: If the operation succeded or not, and if so the current count
        """

        cur_data = self._lookup_record("counting", f"guild_id = {self.guild_id}")
        if len(cur_data) == 0:
            raise NoDataError
        if cur_data[0][2] == user_id:
            raise AlreadyCountedError

        try:
            self._update_record("counting", [("count", cur_data[0][3]+amount), ("last_counted", user_id)], f"guild_id = {self.guild_id}")
        except OperationalError as e:
            return False, e

        return True, cur_data[0][3]+amount

    def get(self):
        """ Get the current count

        :return: Current count
        """

        cur_data = self._lookup_record("counting", f"guild_id = {self.guild_id}")
        if len(cur_data) == 0:
            raise NoDataError

        return cur_data[0][3]

    def set(self, amount: int):
        """ Set the current count

        :param amount: The amount to set it to
        :return: If it succeded or not, and the previous count if so
        """
        cur_data = self._lookup_record("counting", f"guild_id = {self.guild_id}")
        if len(cur_data) == 0:
            return False, NoDataError

        try:
            self._update_record("counting", [("count", amount)], f"guild_id = {self.guild_id}")
        except OperationalError as e:
            return False, e

        return True, cur_data[3]

    def remove(self, amount: int):
        cur_data = self._lookup_record("counting", f"guild_id = {self.guild_id}")
        if len(cur_data) == 0:
            return False, NoDataError

        try:
            self._update_record("counting", [("count", cur_data[0][3]-amount)], f"guild_id = {self.guild_id}")
        except OperationalError as e:
            return False, e

        return True, cur_data[0][3]

    def reset(self):
        """ Reset everything

        :return: If the operation succeded or not, and if so all the data for the counting in that guild
        """
        cur_data = self._lookup_record("counting", f"guild_id = {self.guild_id}")
        if len(cur_data) == 0:
            return False, NoDataError

        try:
            self._delete_record("counting", f"guild_id = {self.guild_id}")
        except OperationalError as e:
            return False, e

        return True, cur_data[0]


class Ban:
    """ High-level management of joybot bans databse """
    def __init__(self, guild_id: int):
        super().__init__("joybot_main")
        self.guild_id = guild_id

        if not self._table_exists("guild_bans"):
            self._make_table("guild_bans", [("guild_id", "INTEGER PRIMARY KEY")])

    def is_banned(self):
        """ Checks if a guild is banned or not """
        rec = self._lookup_record("guild_bans", f"guild_id = {self.guild_id}")
        if rec:
            return rec[0] != 0
        return False

    def ban(self):
        """ Bans a guild """
        try:
            self._add_record("guild_bans", [("guild_id", self.guild_id)])
        except IntegrityError:
            raise AlreadyBannedError

    def unban(self):
        """ Unbans a guild """
        self._delete_record("guild_bans", f"guild_id = {self.guild_id}")


class Bypass:
    """ High-level management of joybot permissions bypass databse """
    def __init__(self, guild_id: int):
        super().__init__("joybot_main")
        self.guild_id = guild_id
        self.is_bypassed = self.check_bypass()

        if not self._table_exists("perm_bypass"):
            self._make_table("perm_bypass", [("guild_id", "INTEGER PRIMARY KEY")])

    def check_bypass(self):
        """ Checks if a guild's permission message is bypassed or not """
        rec = self._lookup_record("perm_bypass", f"guild_id = {self.guild_id}")
        if rec:
            return rec[0] != 0
        return False

    def change(self):
        """ Sets bypass state """
        try:
            self._add_record("perm_bypass", [("guild_id", self.guild_id)])
            self.is_bypassed = True
            return True

        except IntegrityError:
            self._delete_record("perm_bypass", f"guild_id = {self.guild_id}")
            self.is_bypassed = False
            return False
