# encoding:utf-8

"""Custom exceptions used or raised by tvmaze_api
"""

__author__ = 'Prinz23'
__version__ = '1.0'

__all__ = ['IMDbException', 'IMDbError', 'IMDbUserabort', 'IMDbShownotfound',
           'IMDbSeasonnotfound', 'IMDbEpisodenotfound', 'IMDbAttributenotfound', 'IMDbTokenexpired']

from lib.tvinfo_base.exceptions import *


class IMDbException(BaseTVinfoException):
    """Any exception generated by tvdb_api
    """
    pass


class IMDbError(BaseTVinfoError, IMDbException):
    """An error with thetvdb.com (Cannot connect, for example)
    """
    pass


class IMDbUserabort(BaseTVinfoUserabort, IMDbError):
    """User aborted the interactive selection (via
    the q command, ^c etc)
    """
    pass


class IMDbShownotfound(BaseTVinfoShownotfound, IMDbError):
    """Show cannot be found on thetvdb.com (non-existant show)
    """
    pass


class IMDbSeasonnotfound(BaseTVinfoSeasonnotfound, IMDbError):
    """Season cannot be found on thetvdb.com
    """
    pass


class IMDbEpisodenotfound(BaseTVinfoEpisodenotfound, IMDbError):
    """Episode cannot be found on thetvdb.com
    """
    pass


class IMDbAttributenotfound(BaseTVinfoAttributenotfound, IMDbError):
    """Raised if an episode does not have the requested
    attribute (such as a episode name)
    """
    pass


class IMDbTokenexpired(BaseTVinfoAuthenticationerror, IMDbError):
    """token expired or missing thetvdb.com
    """
    pass
