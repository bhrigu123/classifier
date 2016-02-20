# -*- coding: utf-8 -*-

import unittest

import six.moves.configparser as configparser

from classifier import config


class ConfigTest(unittest.TestCase):

    def test_config(self):
        raw = {'a': '123'}
        dicts = {'a': {'aa': 'bb', 'b': 'bb'}}
        lists = {'a': ['x', 'y', 'z']}
        conf = configparser.SafeConfigParser()
        config._set(conf, 'raw', raw)
        config._set(conf, 'dicts', dicts)
        config._set(conf, 'lists', lists)
        assert config._get(conf, 'raw') == raw
        assert config._get(conf, 'dicts', dict) == dicts
        assert config._get(conf, 'lists', list) == lists


if __name__ == '__main__':
    unittest.main()
