from fabric.api import *

env.production = False
env.project = "anxiousprop"

def staging():
    """Deploy on staging host"""
    raise NotImplemented
    env.hosts = ['pb@web01.pb.io']
    env.path = '/home/pb/projects/%(project)s' % env
    
def production():
    """Deploy master branch on live server"""
    env.production = True
    raise NotImplemented

def update_code():
    """Git push (local) and pull(remote)"""
    local("git push origin master" % env)
    with cd(env.path):
        run("git pull origin master" % env)

def deploy():
    """Update code and restart server"""
    if env.production:
        input = prompt('Are you sure you want to deploy to the production server?', default="n", validate=r'^[yYnN]$')
        if input not in ['y','Y']:
            exit()
    update_code()
    run("touch %(path)s/%(project)s.wsgi" % env)
