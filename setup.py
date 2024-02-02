from setuptools import setup

setup(
    name='syscourseutils',
    version='1.0.1',
    py_modules=['cspt','cspt.config','cspt.tasktracking','cspt.sitetools',],
    install_requires=[
        'Click', 'pandas', 'lxml', 'numpy','requests','html5lib'
    ],
    entry_points={
        'console_scripts': [
            'sysgetassignment = cspt.tasktracking:get_assignment',
            'sysfmtassignment = tasktracking:fetch_to_checklist',
            'sysgetbadgedate = tasktracking:get_badge_date',
            'kwlcsv = sitetools:kwl_csv',
            'cleandate = tasktracking:parse_date'
        ],
    },
)
