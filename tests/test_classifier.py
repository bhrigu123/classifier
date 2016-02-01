# -*- coding: utf-8 -*-

import os
import unittest

from classifier import classifier as clf


class ClassifierTest(unittest.TestCase):

    __location = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    __tmp_file_name = '.classifier_test'

    def test_moveto(self):
        os.chdir(self.__location)
        tmp_file = open(self.__tmp_file_name, 'w')

        parent_dir = os.path.abspath(os.path.join(self.__location, os.pardir))
        clf.moveto(self.__tmp_file_name, self.__location, parent_dir)

        final_file_path = os.path.join(parent_dir, self.__tmp_file_name)
        self.assertTrue(os.path.exists(final_file_path))
        os.remove(final_file_path)

if __name__ == '__main__':
    unittest.main()
