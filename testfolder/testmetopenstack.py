from openstack import connection
import openstack
def test():
    conn = connection.Connection(auth_url="",
                                 #project_name="admin",username='admin',
                                 #password='',
                                 #user_domain_id='default',
                                 #project_domain_id='default'
                                 )

    print(conn)
    project="admin"
    dictvooropenstack={}
    listvorprojects=[]
    for project in conn.identity.projects():
        #print(project)
        listvorprojects.append(project.name)
    for flavor in conn.compute.flavors():
        #print(flavor.name)
        f='f'
def openstackinstances(user,password,authurl,project):
    dictvooropenstack = {}
    listvorprojects=['admin']

    for project in listvorprojects:
        conn = connection.Connection(auth_url="",
                                     #project_name=project, username='admin',
                                     #password="",
                                     #user_domain_id='default',
                                     #project_domain_id='default'
                                     )
        print(project)
        for server in conn.compute.servers():
            #print(server.name)
            instancename=server.name
            #print(server.security_groups)
            print(server)
            if (server.location.region_name) == '':
                regioname='NONE'
                print('empty region')
            else:
                regioname=server.location.region_name
            #print(server.original_name)
            #for x in (server.addresses):
            #    print(x)
            #print(server.addresses)
            if project in dictvooropenstack:
                f='f'
            else:
                dictvooropenstack[project]={}
            if regioname in dictvooropenstack[project]:
                f='f'
            else:
                dictvooropenstack[project][regioname]={}
            dictvooropenstack[project][regioname][instancename]={}
            dictvooropenstack[project][regioname][instancename]['status']=server.status
            for x in (server.addresses):
                dictvooropenstack[project][regioname][instancename][x]=server.addresses[x][0]['addr']

        #for image in conn.compute.images():
        #    print(image.name)
    return dictvooropenstack

#print(dictvooropenstack)