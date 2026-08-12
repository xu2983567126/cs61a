test = {
  'name': 'accumulate',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          scm> (accumulate * 1 5 identity)
          8a65148020e6949b5f51ce1565d3a472
          # locked
          scm> (accumulate * 2 4 identity)
          f842757563357c52762061ee1f54f51c
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        }
      ],
      'scored': True,
      'setup': r"""
      scm> (load-all ".")
      scm> (define (identity x) x)
      """,
      'teardown': '',
      'type': 'scheme'
    },
    {
      'cases': [
        {
          'code': r"""
          scm> (define (square x) (* x x))
          cc5843273602621c15b3b18274a0dbb3
          # locked
          scm> (accumulate + 0 5 square)
          3ddbc76ef86b6916e795c81705899c13
          # locked
          scm> (accumulate + 5 5 square)
          0af3e7a1212cd17f3179f57324330bca
          # locked
          scm> (accumulate + 2 3 square)
          cd59f3362ef5418f3c213379f16cf8dc
          # locked
          """,
          'hidden': False,
          'locked': True,
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
