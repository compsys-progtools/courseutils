from setuptools import setup

setup(
    name='syscourseutils',
    version='0.4.0',
    py_modules=['kwltracking','tasktracking','sitetools','badges'],
    install_requires=[
        'Click', 'pandas', 'lxml', 'numpy','requests','html5lib'
    ],
    entry_points={
        'console_scripts': [
            'sysgetassignment = tasktracking:get_assignment',
            'sysfmtassignment = tasktracking:fetch_to_checklist',
            'sysgetbadgedate = tasktracking:get_badge_date',
            'kwlcsv = sitetools:kwl_csv',
            'cleandate = tasktracking:parse_date'
        ],
    },
)
