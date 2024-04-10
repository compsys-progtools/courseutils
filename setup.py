from setuptools import setup

setup(
    name='syscourseutils',
    version='1.0.4',
    py_modules=['cspt','cspt.activities','cspt.badges','cspt.cli',
                'cspt.config','cspt.lesson','cspt.notes','cspt.prep',
                'cspt.sitetools','cspt.tasktracking','cspt.grade_calculation',
                'cspt.grade_constants'
                ],
    install_requires=[
        'Click', 'pandas', 'lxml','pyyaml', 'numpy','requests','html5lib'
    ],
    entry_points={
        'console_scripts': [
            'cspt = cspt.cli:cspt_cli',
        ],
    },
)
