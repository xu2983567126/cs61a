test = {
  'name': 'concatenate',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          scm> (concatenate (list (list 1 2) (list 5 1)))
          90d7208c38d3c085802e93f77912e08e
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          scm> (concatenate (list (list 1 2) (list)))
          1db8597eac84e7adb36454b21eb78535
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          scm> (define (tail-list n so-far)
          ....   (if (= n 0)
          ....       so-far
          ....       (tail-list (- n 1) (cons 1 so-far)))) ; What does scheme return after a `define` statement?
          79b88a8e0ebf92e1da668c28c007153b
          # locked
          scm> (define big-list (tail-list 100000 '()))
          5fbf7cc182a8a5559d4417532f41ba58
          # locked
          scm> (define result (concatenate (list big-list (list 1 2 3 4)))) ; Test for tail recursion
          aeefa8f57eccb020bad009f1c8ed2376
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
