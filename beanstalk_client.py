import beanstalkc
import json
import os
from time import sleep

beanstalk = beanstalkc.Connection()

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PDF_SRC_DIR = os.path.join(PROJECT_ROOT, 'static', 'pdf-src')
PDF_OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'static', 'pdf')

while True:
    job = beanstalk.reserve()
    sleep(3)
    job_data = json.loads(job.body)
    cmd = 'pdfjoin %(page_files)s --outfile %(output_dir)s/%(queue_id)s.pdf' % {
        'page_files': " ".join(["%s/%s.pdf" % (PDF_SRC_DIR, page) for page in ['cover'] + job_data['pages'] + ['back']]),
        'output_dir': PDF_OUTPUT_DIR,
        'queue_id': job_data['queue_id'],
    }
    os.system(cmd)
    job.delete()
