#
# This file is part of HEPData.
# Copyright (C) 2015 CERN.
#
# HEPData is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# HEPData is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HEPData; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
from hepdata.ext.elasticsearch.aggregations import parse_author_aggregations, \
    parse_date_aggregations, parse_collaboration_aggregations, \
    parse_other_facets, parse_aggregations

def test_parse_author_aggregations():
    buckets = [
        {'key': 'author1', 'doc_count': 1},
        {'key': 'author2', 'doc_count': 2}
    ]

    expected = {
        'vals': [
            {
                'url_params': {'author': 'author1'},
                'key': 'author1',
                'doc_count': 1
            },
            {
                'url_params': {'author': 'author2'},
                'key': 'author2',
                'doc_count': 2
            }
        ],
        'max_values': 10,
        'printable_name': 'Authors',
        'type': 'author'
    }
    assert(parse_author_aggregations(buckets) == expected)

def test_parse_collaboration_aggregations():
    buckets = [
        {'key': 'collab1', 'doc_count': 3},
        {'key': 'collab2', 'doc_count': 1}
    ]
    expected = {
        'vals': [
            {
                'url_params': {'collaboration': 'collab1'},
                'key': 'COLLAB1',
                'doc_count': 3
            },
            {
                'url_params': {'collaboration': 'collab2'},
                'key': 'COLLAB2',
                'doc_count': 1
            }
        ],
        'max_values': 5,
        'printable_name': 'Collaboration',
        'type': 'collaboration'
    }
    assert(parse_collaboration_aggregations(buckets) == expected)

def test_parse_date_aggregations():
    buckets = [
        {
            'key_as_string': '2013-01-01T00:00:00.000Z',
            'key': 1356998400000,
            'doc_count': 1
        },
        {
            'key_as_string': '2014-02-01T00:00:00.000Z',
            'key': 1391212800000,
            'doc_count': 1
        },
        {
            'key_as_string': '2014-01-01T00:00:00.000Z',
            'key': 1388534400000,
            'doc_count': 2
        }
    ]

    expected = {
        'vals': [
            {
                'url_params': {'date': 2014},
                'key': 2014,
                'key_as_string': '2014-01-01T00:00:00.000Z',
                'doc_count': 2
            },
            {
                'url_params': {'date': 2014},
                'key': 2014,
                'key_as_string': '2014-02-01T00:00:00.000Z',
                'doc_count': 1
            },
            {
                'url_params': {'date': 2013},
                'key': 2013,
                'key_as_string': '2013-01-01T00:00:00.000Z',
                'doc_count': 1
            }
        ],
        'max_values': 5,
        'printable_name': 'Date',
        'type': 'date'
    }

    assert(parse_date_aggregations(buckets) == expected)

def test_parse_other_facets():
    buckets = [
        {'key': 'Key1', 'doc_count': 1},
        {'key': 'Key2', 'doc_count': 3},
        {'key': 'Key3', 'doc_count': 2}
    ]
    expected = {
        'vals': [
            {
                'url_params': {'test_facet': 'Key1'},
                'key': 'Key1',
                'doc_count': 1
            },
            {
                'url_params': {'test_facet': 'Key2'},
                'key': 'Key2',
                'doc_count': 3
            },
            {
                'url_params': {'test_facet': 'Key3'},
                'key': 'Key3',
                'doc_count': 2
            }
        ],
        'max_values': 5,
        'printable_name': 'Test_facet',
        'type': 'test_facet'
    }
    assert(parse_other_facets(buckets, 'test_facet') == expected)


def test_parse_aggregations():
    aggregations = {
        'nested_authors': {
            'author_full_names': {
                'buckets': [
                    {'key': 'author1', 'doc_count': 1}
                ]
            }
        },
        'collaboration': {
            'buckets': [
                {'key': 'collab1', 'doc_count': 3}
            ],
        },
        'dates': {
            'buckets': [
                {
                    'key_as_string': '2013-01-01T00:00:00.000Z',
                    'key': 1356998400000,
                    'doc_count': 1
                }
            ]
        },
        'another_facet': {
            'buckets': [
                {'key': 'Key1', 'doc_count': 1}
            ]
        },
    }

    expected = [
        {
            'vals': [
                {
                    'url_params': {'date': 2013},
                    'key': 2013,
                    'key_as_string': '2013-01-01T00:00:00.000Z',
                    'doc_count': 1
                }
            ],
            'max_values': 5,
            'printable_name': 'Date',
            'type': 'date'
        },
        {
            'vals': [
                {
                    'url_params': {'author': 'author1'},
                    'key': 'author1',
                    'doc_count': 1
                }
            ],
            'max_values': 10,
            'printable_name': 'Authors',
            'type': 'author'
        },
        {
            'vals': [
                {
                    'url_params': {'another_facet': 'Key1'},
                    'key': 'Key1',
                    'doc_count': 1
                }
            ],
            'max_values': 5,
            'printable_name': 'Another_facet',
            'type': 'another_facet'
        },
        {
            'vals': [
                {
                    'url_params': {'collaboration': 'collab1'},
                    'key': 'COLLAB1',
                    'doc_count': 3
                }
            ],
            'max_values': 5,
            'printable_name': 'Collaboration',
            'type': 'collaboration'
        }
    ]
    assert(parse_aggregations(aggregations) == expected)
