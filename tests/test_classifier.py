# -*- coding: utf-8 -*-

import arrow
import os
import shutil
import unittest

from classifier import classifier as clf
from six.moves import getcwd


class ClassifierTest(unittest.TestCase):

    __location = os.path.realpath(
        os.path.join(getcwd(), os.path.dirname(__file__), '.unittest'))

    __tmp_files = [u'test_file', u'test_file_中文']
    __tmp_dirs = [u'test_dir', u'test_dir_中文']

    def setUp(self):
        if not os.path.exists(self.__location):
            os.mkdir(self.__location)
        os.chdir(self.__location)
        for file_ in self.__tmp_files:
            open(file_, 'w').close()
        for dir_ in self.__tmp_dirs:
            if not os.path.exists(dir_):
                os.mkdir(dir_)
        super(ClassifierTest, self).setUp()

    def tearDown(self):
        shutil.rmtree(self.__location)
        super(ClassifierTest, self).tearDown()

    def test_moveto(self):
        target_dir = os.path.abspath(os.path.join(self.__location, 'moveto'))
        for file_ in self.__tmp_files:
            clf.moveto(file_, self.__location, target_dir)

        for file_ in self.__tmp_files:
            final_file_path = os.path.join(target_dir, file_)
            self.assertTrue(os.path.exists(final_file_path))

    def test_classify_bydate(self):
        date_format = 'DD-MM-YYYY'
        target_files = []
        for file_ in self.__tmp_files:
            target_dir = arrow.get(os.path.getctime(file_)).format(date_format)
            final_file_path = os.path.join(target_dir, file_)
            target_files.append(final_file_path)
        clf.classify_by_date(date_format, self.__location)
        for file_ in target_files:
            self.assertTrue(os.path.exists(final_file_path))
        for dir_ in self.__tmp_dirs:
            self.assertTrue(os.path.exists(dir_))


if __name__ == '__main__':
    unittest.main()
