"""
Test that volume mounts work when running
"""
import os
import subprocess
import tempfile
import time

def test_volume_abspath():
    """
    Validate that you can bind mount a volume onto an absolute dir & write to it
    """
    ts = str(time.time())
    with tempfile.TemporaryDirectory() as tmpdir:
        subprocess.check_call([
            'repo2docker',
            '-v', '{}:/home/jovyan'.format(tmpdir),
            tmpdir,
            '--',
            '/bin/bash',
            '-c', 'echo -n {} > ts'.format(ts)
        ])

        with open(os.path.join(tmpdir, 'ts')) as f:
            assert f.read() == ts


def test_volume_relpath():
    """
    Validate that you can bind mount a volume onto an relative path & write to it
    """
    curdir = os.getcwd()
    try:
        ts = str(time.time())
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            subprocess.check_call([
                'repo2docker',
                '-v', '.:.',
                tmpdir,
                '--',
                '/bin/bash',
                '-c', 'echo -n {} > ts'.format(ts)
            ])

            with open(os.path.join(tmpdir, 'ts')) as f:
                assert f.read() == ts
    finally:
        os.chdir(curdir)
