# encoding=utf8
from doit import get_var
from roald import Roald

import logging
import logging.config
logging.config.fileConfig('logging.cfg', )
logger = logging.getLogger(__name__)

import data_ub_tasks

config = {
    'dumps_dir': get_var('dumps_dir', '/opt/data.ub/www/default/dumps'),
    'dumps_dir_url': get_var('dumps_dir_url', 'http://data.ub.uio.no/dumps'),
    'graph': 'http://data.ub.uio.no/tekord',
    'fuseki': 'http://localhost:3030/ds',
    'basename': 'tekord',
    'git_user': 'ubo-bot',
    'git_email': 'danmichaelo+ubobot@gmail.com',
}


def task_fetch_core():

    logger.info('Checking for updated files')

    yield {
        'doc': 'Fetch remote files that have changed',
        'basename': 'fetch',
        'name': None
    }
    yield data_ub_tasks.git_pull_task_gen(config)
    for file in [
        {
            'remote': 'https://mapper.biblionaut.net/export/real_tekord_mappings.ttl',
             'local': 'src/real_tekord_mappings.ttl'
        }
    ]:
        yield data_ub_tasks.fetch_remote_gen(file['remote'], file['local'], ['fetch_core:git-pull'])


def task_build():

    def build_dist(task):
        logger.info('Building new dist')
        roald = Roald()
        roald.load('src/tekord.xml', format='bibsys', language='nb')
        roald.set_uri_format(
            'http://data.ub.uio.no/%s/c{id}' % config['basename'])
        roald.save('%s.json' % config['basename'])
        logger.info('Wrote %s.json', config['basename'])

        includes = [
            '%s.scheme.ttl' % config['basename'],
            'ubo-onto.ttl'
        ]

        mappings = [
            'src/real_tekord_mappings.ttl'
        ]

        # 1) MARC21
        marc21options = {
            'vocabulary_code': 'tekord',
            'created_by': 'NO-TrNTNU'
        }
        roald.export('dist/%s.marc21.xml' %
                     config['basename'], format='marc21', **marc21options)
        logger.info('Wrote dist/%s.marc21.xml', config['basename'])

        # 2) RDF (core)
        roald.export('dist/%s.ttl' % config['basename'],
                     format='rdfskos',
                     include=includes,
                     add_same_as=['http://ntnu.no/ub/data/tekord#{id}']
                     )
        logger.info('Wrote dist/%s.core.ttl', config['basename'])

        # 3) RDF (core + mappings)
        roald.export('dist/%s.complete.ttl' % config['basename'],
                     format='rdfskos',
                     include=includes,
                     mappings_from=mappings,
                     add_same_as=['http://ntnu.no/ub/data/tekord#{id}']
                     )
        logger.info('Wrote dist/%s.complete.ttl', config['basename'])

    return {
        'doc': 'Build distribution files (RDF/SKOS + MARC21XML) from source files',
        'actions': [build_dist],
        'file_dep': [
            'src/tekord.xml',
            'src/real_tekord_mappings.ttl',
            'ubo-onto.ttl',
            '%s.scheme.ttl' % config['basename']
        ],
        'targets': [
            '%s.json' % config['basename'],
            'dist/%s.marc21.xml' % config['basename'],
            'dist/%s.ttl' % config['basename'],
            'dist/%s.complete.ttl' % config['basename']
        ]
    }


# def task_git_push():
#     return data_ub_tasks.git_push_task_gen(config)


def task_publish_dumps():
    return data_ub_tasks.publish_dumps_task_gen(config['dumps_dir'], [
        '%s.marc21.xml' % config['basename'],
        '%s.ttl' % config['basename'],
        '%s.complete.ttl' % config['basename']
    ])


def task_fuseki():
    return data_ub_tasks.fuseki_task_gen(config, ['dist/%(basename)s.complete.ttl'])

