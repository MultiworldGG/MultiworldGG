#!/usr/bin/python3

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# the COPYING file included with this distribution or
# http://sam.zoy.org/wtfpl/COPYING for more details.

from distutils.core import setup

setup(
		name="python-bps-continued",
		version="7",
		description="A toolkit for working with BPS patch files",
		url="https://github.com/tcprescott/python-bps-continued",
		author="Timothy Allen",
		author_email="screwtape@froup.com",
		license="WTFPL",
		packages=["bps", "bps.test"],
		package_data={"bps.test": ["testdata/*"]},
		scripts=[
			"bin/bps-apply",
			"bin/bps-asm",
			"bin/bps-diff",
			"bin/bps-disasm",
			"bin/bps-graph",
			"bin/bps-optimize",
			"bin/bps-validate",
			],
	)
