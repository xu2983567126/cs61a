test = {
  'name': 'using-link',
  'points': 0,
  'suites': [
    {
      'cases': [
        {
          'answer': '9c71e25107bcc9b61bd94e1e745321f8',
          'choices': [
            "Link('+', Link('-', Link(2, Link(4, Link(6, Link(8))))))",
            "Link('+', Link(Link(-, Link(2, Link(4))), Link(6, Link(8))))",
            'Link(+, Link(Link(-, Link(2, Link(4))), Link(6, Link(8))))',
            "Link('+', Link(Link('-', Link(2, Link(4))), Link(6, Link(8))))",
            'None of these'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': 'Find the Python expression that returns a `Link` representing the given expression: (+ (- 2 4) 6 8)'
        },
        {
          'answer': '37670e4b00633084aa22d884c6c9326d',
          'choices': [
            '-',
            '+',
            '(',
            '2',
            '6',
            'None of these'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': "What is the operator of the previous part's call expression?"
        },
        {
          'answer': 'f691e16231ded18eebfd3f4f5ef545cd',
          'choices': [
            'p',
            'p.first',
            'p.rest',
            'p.rest.first',
            'p.first.rest'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': r"""
          If the `Link` you constructed in the previous part was bound to the name `p`,
          how would you retrieve the operator?
          """
        },
        {
          'answer': 'df97a47b2518e72a265467bdb7e64aff',
          'choices': [
            'p',
            'p.first',
            'p.rest',
            'p.rest.first',
            'p.first.rest'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': r"""
          If the `Link` you constructed was bound to the name `p`, 
          how would you retrieve a list containing all of the operands?
          """
        },
        {
          'answer': '47cc7a335c0fc0140c6aabcbbdbce2f6',
          'choices': [
            'p',
            'p.first',
            'p.rest',
            'p.rest.first',
            'p.first.rest'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': 'How would you retrieve only the first operand?'
        },
        {
          'answer': '804c40b21e1fcae9ab6eb0c65188169d',
          'choices': [
            "'-'",
            "'+'",
            '2',
            '4',
            '-2',
            "Link('-', Link(2, Link(4)))",
            'Link(2, Link(4))'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': 'What is the first operand of the call expression (+ (- 2 4) 6 8) prior to evaluation?'
        }
      ],
      'scored': False,
      'type': 'concept'
    }
  ]
}
