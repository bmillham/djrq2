#!/usr/bin/env python
# encoding: utf-8

import os

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


setup(
		name = "DJRQ2",
		version = "0.1",
		
		description = "DJRQ2 - Request site for DJs.",
		long_description = "",
		url = "https://github.com/bmillham/djrq2",
		author = "Brian Millham",
		author_email = "bmillham@gmail.com",
		license = "mit",
		keywords = [],
		
		packages = find_packages(exclude=['test', 'example', 'conf', 'benchmark', 'tool', 'doc']),
		include_package_data = True,
		package_data = {'': [
				'README.rst',
				'LICENSE.txt'
			]},
		
		namespace_packages = [
				'web',
				'web.app',
				'web.ext',
			],
		
		setup_requires = [
				'pytest-runner',
			],
		
		tests_require = [
				'pytest-runner',
				'coverage',
				'pytest',
				'pytest-cov',
				'pytest-spec',
				'pytest-flakes',
			],
		
		install_requires = [
				'WebCore>=2.0.3,<3',  # The underlying web framework.
				'web.db>=2.0.1,<3',  # Database connectivity layer for WebCore.
				'marrow.mongo',
				#'web.session>=2.0',
				'web.dispatch.object',  # Object (class-based filesystem-like) dispatch for endpoint discovery.
				'web.dispatch.resource',  # Resource (based on REQUEST_METHOD) dispatch for endpoint discovery.
				'cinje',  # Template engine, an importable Python domain-specific code transformer / language.
				'mysqlclient',
				'sqlalchemy', # SQLAlchemy for mysql access
				'babel', # For internationalization
				'markupsafe',
			],
		
		extras_require = dict(
				development = [
						'pytest-runner',
						'coverage',
						'pytest',
						'pytest-cov',
						'pytest-spec',
						'pytest-flakes',
						'backlash',
					],
			),
		
		entry_points = {
				}
	)
