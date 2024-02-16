from setuptools import setup

setup(
    name='syscourseutils',
    version='1.0.2',
    py_modules=['cspt','cspt.activities','cspt.badges','cspt.cli',
                'cspt.config','cspt.lesson','cspt.notes','cspt.prep',
                'cspt.sitetools','cspt.tasktracking'
                ],
    install_requires=[
        'Click', 'pandas', 'lxml', 'numpy','requests','html5lib'
    ],
    entry_points={
        'console_scripts': [
            'sysgetassignment = cspt.cli:get_assignment',
            'sysgetbadgedate = cspt.cli:get_badge_date',
            'sysgetapprovedbadges = cspt.cli:progress_report',
            'syscheckprs = cspt.cli:check_pr_titles',
            'sysmkghmd = cspt.cli:md_likify_gh_output',
            'kwlcsv = cspt.cli:kwl_csv',
            'cleandate = cspt.cli:parse_date',
            'sysprocessexport = cspt.cli:prepare_notes',
            'syscreatetoyfiles = cspt.cli:create_toy_files',
            'sysprepprismia = cspt.cli:export_prismia',
            'sysprephandout = cspt.cli:export_handout',
            'sysexportac = cspt.cli:export_ac'
        ],
    },
)
