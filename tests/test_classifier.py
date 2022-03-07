# -*- coding: utf-8 -*-

from datetime import date
import pathlib
import arrow
import os
import shutil
import pytest
import classifier.classifier as clf
import tempfile
from loguru import logger

FILES = [".test", "中文.test"]


def get_temp_dir():
    return tempfile.mkdtemp()


def get_tmp_file(suffix=".test", dir=None):
    _, path = tempfile.mkstemp(suffix=suffix, dir=dir)
    return path


@pytest.fixture
def classifier():
    tmpdir = get_temp_dir()
    tmpfiles = [get_tmp_file(f, dir=tmpdir) for f in FILES]

    os.chdir(tmpdir)

    classifier = clf.Classifier(test=True)
    classifier.__location = tmpdir
    classifier.__files = tmpfiles

    yield classifier

    try:
        shutil.rmtree(tmpdir)
    except PermissionError:
        logger.error(f"Permission error when removing {tmpdir}")


@pytest.mark.parametrize("target", ("moveto",))
def test_moveto(classifier, target):
    target_dir = pathlib.Path(classifier.__location, target)
    for file in classifier.__files:
        classifier.moveto(file, classifier.__location, target_dir)

        assert target_dir.joinpath(file).is_file()


@pytest.mark.parametrize("target", ("bydate",))
def test_moveto(classifier, target):
    date_fmt = "YYYY-MM-DD"
    target_path = pathlib.Path(classifier.__location, target)
    final_path = []
    for file in classifier.__files:
        final_path.append(
            target_path.joinpath(
                arrow.get(os.path.getctime(file)).format(date_fmt),
                pathlib.Path(file).name,
            )
        )

    classifier.classify_by_date(date_fmt, target_path, classifier.__location)

    for file in final_path:
        assert pathlib.Path(file).exists()
