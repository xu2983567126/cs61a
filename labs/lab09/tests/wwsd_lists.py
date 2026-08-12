test = {
  'name': 'What Would Scheme Print?',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          scm> (cons 1 (cons 2 nil))
          5ceacf97ccefe7d64916c8d72dfb2b48
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          scm> (car (cons 1 (cons 2 nil)))
          7cd20da6435c318b417f99ab831ac85e
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          scm> (cdr (cons 1 (cons 2 nil)))
          36f31b0ebd049141c21558b1c3b4894d
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          scm> (list 1 2 3)
          31df56b0e4230528bca8a8edc01115c8
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          scm> '(1 2 3)
          31df56b0e4230528bca8a8edc01115c8
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          scm> (cons 1 '(list 2 3))  ; Recall quoting
          9b9cf94f8db477d48f973c67acf1842a
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          scm> (cons 1 `(list 2 3))  ; Quasiquotes also work as quotes!
          9b9cf94f8db477d48f973c67acf1842a
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          scm> '(cons 4 (cons (cons 6 8) ()))
          beed0382fff95ecdd5f05fad62b13daf
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          scm> (cons 1 (list (cons 3 nil) 4 5))
          6246b211fac4ca26704aa19ed398e556
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        }
      ],
      'scored': True,
      'setup': r"""
      
      """,
      'teardown': '',
      'type': 'scheme'
    }
  ]
}
