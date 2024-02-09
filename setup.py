from setuptools import setup

setup(
    name='syscourseutils',
    version='1.0.2',
    py_modules=['cspt','cspt.config','cspt.tasktracking',
                'cspt.sitetools','cspt.notes'],
    install_requires=[
        'Click', 'pandas', 'lxml', 'numpy','requests','html5lib'
    ],
    entry_points={
        'console_scripts': [
            'sysgetassignment = cspt.tasktracking:get_assignment',
            'sysfmtassignment = cspt.tasktracking:fetch_to_checklist',
            'sysgetbadgedate = cspt.tasktracking:get_badge_date',
            'kwlcsv = cspt.sitetools:kwl_csv',
            'cleandate = cspt.tasktracking:parse_date',
            'sysprocessexport = cspt.notes:process_export'
        ],
    },
)
