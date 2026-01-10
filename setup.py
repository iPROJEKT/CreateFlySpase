from setuptools import setup

setup(
    name='CreateFlySpase',
    version='1.0',
    options={
        'build_apps': {
            'gui_apps': {
                'CreateFlySpase': 'run.py',
            },
            'icons': {
                'win_amd64': 'media/ico/ico.ico'
            },
            'include_patterns': [
            'media/**',
            'moled/**',
            '**/*.png',
            '**/*.jpg',
            '**/*.jpeg',
            '**/*.ico',
            '**/*.ttf',
            '**/*.bam',
            '**/*.egg',
            '**/*.glb',
            '**/*.gltf',
            'tcl8.6/**',
            'tk8.6/**',
        ],
            'plugins': [
                'pandagl',
                'p3openal_audio',
            ],
            'platforms': ['win_amd64'],
            'log_filename': 'output.log',
        }
    }
)