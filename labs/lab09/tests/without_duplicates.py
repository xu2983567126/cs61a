test = {
  'name': 'without-duplicates',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          scm> (without-duplicates (list 5 4 2))
          0efc7b6fae05a96fff6baef6d610b805
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          scm> (without-duplicates (list 5 4 5 4 2 2))
          0efc7b6fae05a96fff6baef6d610b805
          # locked
          scm> (without-duplicates (list 5 5 5 5 5))
          d5175fef8eb52fa20d3455e038f1f9aa
          # locked
          scm> (without-duplicates ())
          9fe2321549ca80f78f8bead3784a61a6
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          scm> (without-duplicates '(5 4 3 2 1))
          (5 4 3 2 1)
          scm> (without-duplicates '(5 4 3 2 1 1))
          (5 4 3 2 1)
          scm> (without-duplicates '(5 5 4 3 2 1))
          (5 4 3 2 1)
          scm> (without-duplicates '(12))
          (12)
          scm> (without-duplicates '(1 1 1 1 1 1))
          (1)
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        }
      ],
      'scored': True,
      'setup': r"""
      scm> (load-all ".")
      """,
      'teardown': '',
      'type': 'scheme'
    }
  ]
}
