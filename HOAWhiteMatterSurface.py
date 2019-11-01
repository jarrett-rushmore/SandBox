#!/usr/bin/env python

from __future__ import print_function
from util import logfmt, TemporaryDirectory, N_CPU, __version__
from plumbum import local, cli, FG
from plumbum.cmd import ImageMath, bash
import sys
import os

import logging
logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG, format=logfmt(__file__))


class App(cli.Application):
    """Generates White Matter Surface using FreeSurfer Utilities"""

    VERSION = __version__

    fsSubjectDir = cli.SwitchAttr(
        ['-s', '--subjectDir'],
        cli.ExistingFile
        help='FreeSurfer Subject'
        mandatory=True
    )

