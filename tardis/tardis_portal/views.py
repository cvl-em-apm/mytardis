#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
views.py

@author Steve Androulakis
@author Gerson Galang

"""

from django.template import Context, loader
from django.http import HttpResponse

from django.conf import settings

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect, HttpResponseForbidden, \
    HttpResponseNotFound, HttpResponseServerError
from django.contrib.auth.decorators import login_required

from tardis.tardis_portal.ProcessExperiment import ProcessExperiment
from tardis.tardis_portal.forms import *
from tardis.tardis_portal.errors import *
from tardis.tardis_portal.logger import logger

from django.core.paginator import Paginator, InvalidPage, EmptyPage

from tardis.tardis_portal.models import *
from tardis.tardis_portal import constants
from django.db.models import Sum

import urllib
import urllib2

from tardis.tardis_portal import ldap_auth

from tardis.tardis_portal.MultiPartForm import MultiPartForm


def getNewSearchDatafileSelectionForm():
    DatafileSelectionForm = createSearchDatafileSelectionForm()
    return DatafileSelectionForm()


def render_response_index(request, *args, **kwargs):

    kwargs['context_instance'] = RequestContext(request)

    kwargs['context_instance']['is_authenticated'] = \
        request.user.is_authenticated()
    kwargs['context_instance']['username'] = request.user.username

    if request.mobile:
        template_path = args[0]
        split = template_path.partition('/')
        args = (split[0] + '/mobile/' + split[2], ) + args[1:]

    return render_to_response(*args, **kwargs)


def return_response_error(request):
    c = Context({'status': 'ERROR: Forbidden', 'error': True})
    return HttpResponseForbidden(render_response_index(request,
                                 'tardis_portal/blank_status.html', c))


def return_response_not_found(request):
    c = Context({'status': 'ERROR: Not Found', 'error': True})

    return HttpResponseNotFound(render_response_index(request,
                                'tardis_portal/blank_status.html', c))


def return_response_error_message(request, redirect_path, message):
    c = Context({'status': message, 'error': True})

    return HttpResponseServerError(render_response_index(request,
                                   redirect_path, c))


def logout(request):
    try:
        del request.session['username']
        del request.session['password']
        if 'datafileResults' in request.session:
            del request.session['datafileResults']
    except KeyError:
        pass

    c = Context({})

    return HttpResponse(render_response_index(request,
                        'tardis_portal/index.html', c))


def get_accessible_experiments(user_id):

    experiments = None

    # from stackoverflow question 852414

    from django.db.models import Q

    user = User.objects.get(id=user_id)

    queries = [Q(id=group.name) for group in user.groups.all()]

    if queries:
        query = queries.pop()

        for item in queries:
            query |= item

        experiments = Experiment.objects.filter(query)

    return experiments


def get_accessible_datafiles_for_user(experiments):

    # from stackoverflow question 852414

    from django.db.models import Q

    if experiments is not None:
        queries = [Q(dataset__experiment__id=e.id) for e in experiments]

        query = queries.pop()

        for item in queries:
            query |= item

        dataset_files = Dataset_File.objects.filter(query)

        return dataset_files
    else:
        return []


def get_owned_experiments(user_id):

    experiments = \
        Experiment.objects.filter(experiment_owner__user__pk=user_id)

    return experiments


def has_experiment_ownership(experiment_id, user_id):

    experiment = Experiment.objects.get(pk=experiment_id)

    eo = Experiment_Owner.objects.filter(experiment=experiment,
            user=user_id)

    if eo:
        return True
    else:
        return False


# custom decorator


def experiment_ownership_required(f):

    def wrap(request, *args, **kwargs):
        # if user isn't logged in it will redirect to login page
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login')
        if not has_experiment_ownership(kwargs['experiment_id'],
                request.user.pk):
            return return_response_error(request)

        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


# custom decorator


def experiment_access_required(f):

    def wrap(request, *args, **kwargs):

        if not has_experiment_access(kwargs['experiment_id'],
                request.user):

            # if user isn't logged in it will redirect to login page
            if not request.user.is_authenticated():
                return HttpResponseRedirect('/login')
            else:
                return return_response_error(request)

        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


# custom decorator


def dataset_access_required(f):

    def wrap(request, *args, **kwargs):
        if not has_dataset_access(kwargs['dataset_id'], request.user):

            # if user isn't logged in it will redirect to login page
            if not request.user.is_authenticated():
                return HttpResponseRedirect('/login')
            else:
                return return_response_error(request)

        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


# custom decorator


def datafile_access_required(f):

    def wrap(request, *args, **kwargs):
        if not has_datafile_access(kwargs['dataset_file_id'],
                                   request.user):

            # if user isn't logged in it will redirect to login page
            if not request.user.is_authenticated():
                return HttpResponseRedirect('/login')
            else:
                return return_response_error(request)

        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def has_experiment_access(experiment_id, user):

    # public route

    try:
        e = Experiment.objects.get(id=experiment_id)

        if e.public:
            return True
    except Experiment.DoesNotExist, ge:
        pass

    if not user.is_authenticated():
        return False

    g = Group.objects.filter(name=experiment_id, user__id=user.pk)

    if g:
        return True
    else:
        return False


def has_dataset_access(dataset_id, user):

    experiment = Experiment.objects.get(dataset__pk=dataset_id)

    if experiment.public:
        return True

    if not user.is_authenticated():
        return False

    g = Group.objects.filter(name=str(experiment.id), user__pk=user.pk)

    if g:
        return True
    else:
        return False


def has_datafile_access(dataset_file_id, user):

    df = Dataset_File.objects.get(id=dataset_file_id)

    if df.dataset.experiment.public:
        return True

    if not user.is_authenticated():
        return False

    g = Group.objects.filter(name=df.dataset.experiment.id,
                             user__pk=user.pk)

    if g:
        return True
    else:
        return False


def in_group(user, group):
    """Returns True/False if the user is in the given group(s).
    Usage::
        {% if user|in_group:"Friends" %}
        or
        {% if user|in_group:"Friends,Enemies" %}
        {% endif %}
    You can specify a single group or comma-delimited list.
    No white space allowed.

    """

    group_list = [group.name]

    user_groups = []

    for group in user.groups.all():
        user_groups.append(str(group.name))

    logger.debug(group_list)
    logger.debug(user_groups)

    if filter(lambda x: x in user_groups, group_list):
        return True
    else:
        return False


def index(request):

    status = ''

    c = Context(
        {'status': status,
        'searchDatafileSelectionForm': getNewSearchDatafileSelectionForm()})
    return HttpResponse(render_response_index(request,
                        'tardis_portal/index.html', c))


def site_settings(request):

    if request.method == 'POST':  # If the form has been submitted...
        if 'username' in request.POST and \
                'password' in request.POST:

            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_staff:

                    x509 = open(settings.GRID_PROXY_FILE, 'r')

                    c = Context({'baseurl': settings.TARDISURLPREFIX,
                        'proxy': x509.read(), 'filestorepath':
                        settings.FILE_STORE_PATH})
                    return HttpResponse(render_response_index(request,
                            'tardis_portal/site_settings.xml', c),
                            mimetype='application/xml')
                else:
                    return return_response_error(request)
            else:
                return return_response_error(request)
        else:
            return return_response_error(request)
    else:
        return return_response_error(request)


def download(request, experiment_id):

    # todo handle missing file, general error

    if 'dfid' in request.GET and len(request.GET['dfid']) > 0:
        datafile = Dataset_File.objects.get(pk=request.GET['dfid'])
    elif 'url' in request.GET and len(request.GET['url']) > 0:
        datafile = \
            Dataset_File.objects.get(url=urllib.unquote(request.GET['url']),
            dataset__experiment__id=experiment_id)
    else:
        return return_response_error(request)

    if has_datafile_access(datafile.id, request.user):
        url = datafile.url

        if url.startswith('http://') or url.startswith('https://') \
            or url.startswith('ftp://'):
            return HttpResponseRedirect(datafile.url)
        else:
            file_path = settings.FILE_STORE_PATH + '/' \
                + str(datafile.dataset.experiment.id) + '/' \
                + datafile.url.partition('//')[2]

            try:
                logger.debug(file_path)
                from django.core.servers.basehttp import FileWrapper
                wrapper = FileWrapper(file(file_path))

                response = HttpResponse(wrapper,
                        mimetype='application/octet-stream')
                response['Content-Disposition'] = \
                    'attachment; filename=' + datafile.filename

                # import os
                # response['Content-Length'] = os.path.getsize(file_path)

                return response
            except IOError, io:

                return return_response_not_found(request)
    else:

        return return_response_error(request)


def downloadTar(request):

    # Create the HttpResponse object with the appropriate headers.
    # TODO: handle no datafile, invalid filename, all http links
    # (tarfile count?)

    if 'datafile' in request.POST:

        if not len(request.POST.getlist('datafile')) == 0:
            from django.utils.safestring import SafeUnicode
            from django.core.servers.basehttp import FileWrapper

            fileString = ''
            fileSize = 0
            for dfid in request.POST.getlist('datafile'):
                datafile = Dataset_File.objects.get(pk=dfid)
                if has_datafile_access(dfid, request.user):
                    if datafile.url.startswith('file://'):
                        absolute_filename = datafile.url.partition('//')[2]
                        fileString = fileString + request.POST['expid'] \
                            + '/' + absolute_filename + ' '
                        fileSize = fileSize + long(datafile.size)

            # tarfile class doesn't work on large files being added and
            # streamed on the fly, so going command-line-o

            tar_command = 'tar -C ' + settings.FILE_STORE_PATH + ' -c ' \
                + fileString

            import shlex
            import subprocess

            response = \
                HttpResponse(FileWrapper(subprocess.Popen(tar_command,
                             stdout=subprocess.PIPE,
                             shell=True).stdout),
                             mimetype='application/x-tar')
            response['Content-Disposition'] = \
                'attachment; filename=experiment' + \
                request.POST['expid'] + '.tar'
            response['Content-Length'] = fileSize + 5120

            return response
    elif 'url' in request.POST:

        if not len(request.POST.getlist('url')) == 0:
            from django.utils.safestring import SafeUnicode
            from django.core.servers.basehttp import FileWrapper

            fileString = ''
            fileSize = 0
            for url in request.POST.getlist('url'):
                datafile = \
                    Dataset_File.objects.get(url=urllib.unquote(url),
                        dataset__experiment__id=request.POST['expid'])
                if has_datafile_access(datafile.id, request.user):
                    if datafile.url.startswith('file://'):
                        absolute_filename = datafile.url.partition('//')[2]
                        fileString = fileString + request.POST['expid'] \
                            + '/' + absolute_filename + ' '
                        fileSize = fileSize + long(datafile.size)

            # tarfile class doesn't work on large files being added and
            # streamed on the fly, so going command-line-o

            tar_command = 'tar -C ' + settings.FILE_STORE_PATH + ' -c ' + \
                fileString

            response = \
                HttpResponse(FileWrapper(subprocess.Popen(tar_command,
                             stdout=subprocess.PIPE,
                             shell=True).stdout),
                             mimetype='application/x-tar')
            response['Content-Disposition'] = \
                'attachment; filename=experiment' + request.POST['expid'] + \
                '.tar'
            response['Content-Length'] = fileSize + 5120

            return response
        else:
            return return_response_not_found(request)
    else:
        return return_response_not_found(request)


def display_dataset_image(
    request,
    dataset_id,
    parameterset_id,
    parameter_name,
    ):

    # todo handle not exist

    dataset = Dataset.objects.get(pk=dataset_id)
    if has_experiment_access(dataset.experiment.id, request.user):

        image = DatasetParameter.objects.get(name__name=parameter_name,
                parameterset=parameterset_id)

        import base64

        data = base64.b64decode(image.string_value)

        response = HttpResponse(data, mimetype='image/jpeg')

        return response
    else:
        return return_response_error(request)


def display_datafile_image(
    request,
    dataset_file_id,
    parameterset_id,
    parameter_name,
    ):

    # todo handle not exist

    datafile = Dataset_File.objects.get(pk=dataset_file_id)
    if has_experiment_access(datafile.dataset.experiment.id, request.user):
        image = \
            DatafileParameter.objects.get(name__name=parameter_name,
                parameterset=parameterset_id)

        import base64

        data = base64.b64decode(image.string_value)

        response = HttpResponse(data, mimetype='image/jpeg')

        return response
    else:
        return return_response_error(request)


@experiment_access_required
def downloadExperiment(request, experiment_id):

    # Create the HttpResponse object with the appropriate headers.
    # TODO: handle no datafile, invalid filename, all http links
    # (tarfile count?)

    from django.core.servers.basehttp import FileWrapper

    experiment = Experiment.objects.get(pk=experiment_id)

    tar_command = 'tar -C ' + settings.FILE_STORE_PATH + ' -c ' + \
        str(experiment.id) + '/'
    logger.debug('TAR COMMAND: ' + tar_command)

    import subprocess

    response = HttpResponse(FileWrapper(subprocess.Popen(tar_command,
                            stdout=subprocess.PIPE,
                            shell=True).stdout),
                            mimetype='application/x-tar')
    response['Content-Disposition'] = 'attachment; filename=experiment' \
        + str(experiment.id) + '-complete.tar'

    # response['Content-Length'] = fileSize + 5120

    return response


def about(request):

    c = Context({'subtitle': 'About', 'about_pressed': True,
                'nav': [{'name': 'About', 'link': '/about/'}]})
    return HttpResponse(render_response_index(request,
                        'tardis_portal/about.html', c))


def partners(request):

    c = Context({})

    return HttpResponse(render_response_index(request,
                        'tardis_portal/partners.html', c))


@experiment_access_required
def view_experiment(request, experiment_id):

    try:
        experiment = Experiment.objects.get(pk=experiment_id)
        author_experiments = Author_Experiment.objects.all()
        author_experiments = \
            author_experiments.filter(experiment=experiment)
        author_experiments = author_experiments.order_by('order')

        datafiles = \
            Dataset_File.objects.filter(dataset__experiment=experiment_id)

        size = 0
        for dataset in experiment.dataset_set.all():
            for df in dataset.dataset_file_set.all():
                size = size + long(df.size)

        owners = None
        try:
            owners = \
                Experiment_Owner.objects.filter(experiment=experiment)
        except Experiment_Owner.DoesNotExist, eo:
            pass

        c = Context({
            # 'totalfilesize': datafiles.aggregate(Sum('size'))['size__sum'],
            'experiment': experiment,
            'authors': author_experiments,
            'datafiles': datafiles,
            'subtitle': experiment.title,
            'owners': owners,
            'size': size,
            'nav': [{'name': 'Data', 'link': '/experiment/view/'},
                    {'name': experiment.title, 'link': '/experiment/view/' +
                     str(experiment.id) + '/'}],
            'searchDatafileSelectionForm':
            getNewSearchDatafileSelectionForm()})
    except Experiment.DoesNotExist, de:
        return return_response_not_found(request)

    return HttpResponse(render_response_index(request,
                        'tardis_portal/view_experiment.html', c))


def experiment_index(request):

    experiments = None

    # if logged in
    if request.user.is_authenticated():
        experiments = get_accessible_experiments(request.user.id)
        if experiments:
            experiments = experiments.order_by('title')

    public_experiments = Experiment.objects.filter(public=True)
    if public_experiments:
        public_experiments = public_experiments.order_by('title')

    c = Context({
        'experiments': experiments,
        'public_experiments': public_experiments,
        'subtitle': 'Experiment Index',
        'bodyclass': 'list',
        'nav': [{'name': 'Data', 'link': '/experiment/view/'}],
        'data_pressed': True,
        })
    return HttpResponse(render_response_index(request,
                        'tardis_portal/experiment_index.html', c))


# web service, depreciated
def register_experiment_ws(request):

    # from java.lang import Exception

    import sys

    process_experiment = ProcessExperiment()
    status = ''
    if request.method == 'POST':  # If the form has been submitted...

        url = request.POST['url']
        username = request.POST['username']
        password = request.POST['password']

        from django.contrib.auth import authenticate
        user = authenticate(username=username, password=password)
        if user is not None:
            if not user.is_active:
                return return_response_error(request)
        else:
            return return_response_error(request)

        try:
            experiments = Experiment.objects.all()
            experiments = experiments.filter(url__iexact=url)
            if not experiments:
                eid = process_experiment.register_experiment(url=url,
                        created_by=user)
            else:
                return return_response_error_message(request,
                        'tardis_portal/blank_status.html',
                        'Error: Experiment already exists')
        except IOError, i:
            return return_response_error_message(request,
                    'tardis_portal/blank_status.html',
                    'Error reading file. Perhaps an incorrect URL?')
        except:
            return return_response_error_message(request,
                    'tardis_portal/blank_status.html',
                    'Unexpected Error - ', sys.exc_info()[0])

        response = HttpResponse(status=200)
        response['Location'] = settings.TARDISURLPREFIX \
            + '/experiment/view/' + str(eid)

        return response
    else:
        return return_response_error(request)


def create_placeholder_experiment(user):
    e = Experiment(
        url='http://www.example.com',
        approved=True,
        title='Placeholder Title',
        institution_name='Placeholder',
        description='Placeholder description',
        created_by=user,
        )

    e.save()

    return e.id


# todo complete....


def ldap_login(request):
    from django.contrib.auth import authenticate, login

    # if user exists then check if ldap: try log in through ldap, else try log
    # in usual way, either way login

    # TODO: put me in SETTINGS
    if 'username' in request.POST and \
            'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']

        next = '/'
        # TODO: this block will need fixing later as the expected functionality
        #       this condition is supposed to provide does not work
        if 'next' in request.POST:
            next = request.POST['next']

        c = Context({'searchDatafileSelectionForm':
            getNewSearchDatafileSelectionForm()})

        error_template_redirect = 'tardis_portal/login.html'

        if settings.LDAP_ENABLE:
            try:
                u = User.objects.get(username=username)

                try:
                    if u.get_profile().authcate_user:
                        if ldap_auth.authenticate_user_ldap(username,
                                password):
                            u.backend = \
                                'django.contrib.auth.backends.ModelBackend'
                            login(request, u)
                            return HttpResponseRedirect(next)
                        else:
                            return return_response_error_message(request,
                                error_template_redirect,
                                "Sorry, username and password don't match")
                    else:
                        if authenticate(username=username,
                                password=password):
                            u.backend = \
                                'django.contrib.auth.backends.ModelBackend'
                            login(request, u)
                            return HttpResponseRedirect(next)
                        else:
                            return return_response_error_message(request,
                                    error_template_redirect,
                                    "Sorry, username and password don't match")
                except UserProfile.DoesNotExist, ue:
                    if authenticate(username=username,
                                    password=password):
                        u.backend = \
                            'django.contrib.auth.backends.ModelBackend'
                        login(request, u)
                        return HttpResponseRedirect(next)
                    else:
                        return return_response_error_message(request,
                                error_template_redirect,
                                "Sorry, username and password don't match")
            except User.DoesNotExist, ue:
                if ldap_auth.authenticate_user_ldap(username, password):
                    email = ldap_auth.get_ldap_email_for_user(username)

                    from random import choice
                    import string

                    # random password todo make function

                    random_password = ''
                    chars = string.letters + string.digits

                    for i in range(8):
                        random_password = random_password \
                            + choice(chars)

                    u = User.objects.create_user(username, email,
                            random_password)
                    up = UserProfile(authcate_user=True, user=u)
                    up.save()

                    u.backend = \
                        'django.contrib.auth.backends.ModelBackend'
                    # TODO: consolidate
                    login(request, u)
                    return HttpResponseRedirect(next)
                else:
                    return return_response_error_message(request,
                            error_template_redirect,
                            "Sorry, username and password don't match")
        u = authenticate(username=username, password=password)
        if u:
            u.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, u)
            return HttpResponseRedirect(next)
        else:
            return return_response_error_message(request,
                    error_template_redirect,
                    "Sorry, username and password don't match")

    c = Context({'searchDatafileSelectionForm':
            getNewSearchDatafileSelectionForm()})
    return HttpResponse(render_response_index(request,
                        'tardis_portal/login.html', c))


def register_experiment_ws_xmldata_internal(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        filename = request.POST['filename']
        eid = request.POST['eid']

        from django.contrib.auth import authenticate
        user = authenticate(username=username, password=password)
        if user is not None:
            if not user.is_active:
                return return_response_error(request)
        else:
            return return_response_error(request)

        process_experiment = ProcessExperiment()
        process_experiment.register_experiment_xmldata_file(filename=filename,
                created_by=user, expid=eid)

        response = HttpResponse('Finished cataloging: ' + str(eid),
                                status=200)
        response['Location'] = settings.TARDISURLPREFIX \
            + '/experiment/view/' + str(eid)

        return response


# web service


def register_experiment_ws_xmldata(request):
    import sys
    import threading

    status = ''
    if request.method == 'POST':  # If the form has been submitted...

        # A form bound to the POST data
        form = RegisterExperimentForm(request.POST, request.FILES)
        if form.is_valid():  # All validation rules pass

            xmldata = request.FILES['xmldata']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            experiment_owner = form.cleaned_data['experiment_owner']
            originid = form.cleaned_data['originid']

            from_url = None
            if 'form_url' in request.POST:
                from_url = request.POST['from_url']

            from django.contrib.auth import authenticate
            user = authenticate(username=username, password=password)
            if user is not None:
                if not user.is_active:
                    return return_response_error(request)
            else:
                return return_response_error(request)

            eid = create_placeholder_experiment(user)

            dir = settings.FILE_STORE_PATH + '/' + str(eid)

            # TODO: this entire function needs a fancy class with functions for
            # each part..

            import os
            if not os.path.exists(dir):
                os.makedirs(dir)
                os.system('chmod g+w ' + dir)

            filename = dir + '/METS.xml'
            file = open(filename, 'wb+')

            for chunk in xmldata.chunks():
                file.write(chunk)

            file.close()

            class RegisterThread(threading.Thread):

                def run(self):
                    data = urllib.urlencode({
                        'username': username,
                        'password': password,
                        'filename': filename,
                        'eid': eid,
                        })
                    urllib.urlopen(settings.TARDISURLPREFIX
                                   + '/experiment/register/internal/',
                                   data)

            RegisterThread().start()

            # create group

            # for each PI
                # check if they exist
                    # if exist
                        # assign to group
                    # else
                        # create user, generate username, randomly generated
                        # pass, send email with pass

            if not len(request.POST.getlist('experiment_owner')) == 0:
                g = Group(name=eid)
                g.save()

                for owner in request.POST.getlist('experiment_owner'):

                    owner = urllib.unquote_plus(owner)

                    logger.debug('registering owner: ' + owner)
                    u = None

                    # try get user from email

                    if settings.LDAP_ENABLE:
                        u = ldap_auth.get_or_create_user_ldap(owner)
                        e = Experiment.objects.get(pk=eid)
                        exp_owner = Experiment_Owner(experiment=e,
                                user=u)
                        exp_owner.save()
                        u.groups.add(g)

            logger.debug('Sending file request')

            if from_url:

                class FileTransferThread(threading.Thread):

                    def run(self):

                        # todo remove hard coded u/p for sync transfer....

                        logger.debug('started transfer thread')

                        file_transfer_url = from_url + '/file_transfer/'
                        data = urllib.urlencode({
                            'originid': str(originid),
                            'eid': str(eid),
                            'site_settings_url': str(settings.TARDISURLPREFIX +
                            '/site-settings.xml/'),
                            'username': str('synchrotron'),
                            'password': str('tardis'),
                            })

                        logger.debug(file_transfer_url)
                        logger.debug(data)

                        urllib.urlopen(file_transfer_url, data)

                FileTransferThread().start()

            logger.debug('returning response from main call')

            response = HttpResponse(str(eid), status=200)
            response['Location'] = settings.TARDISURLPREFIX \
                + '/experiment/view/' + str(eid)

            return response
    else:

        form = RegisterExperimentForm()  # An unbound form

    c = Context({'form': form, 'status': status,
        'subtitle': 'Register Experiment',
        'searchDatafileSelectionForm': getNewSearchDatafileSelectionForm()})
    return HttpResponse(render_response_index(request,
                        'tardis_portal/register_experiment.html', c))


@datafile_access_required
def retrieve_parameters(request, dataset_file_id):

    parametersets = DatafileParameterSet.objects.all()
    parametersets = parametersets.filter(dataset_file__pk=dataset_file_id)

    c = Context({'parametersets': parametersets})

    return HttpResponse(render_response_index(request,
                        'tardis_portal/ajax/parameters.html', c))


@datafile_access_required
def retrieve_xml_data(request, dataset_file_id):
    from pygments import highlight
    from pygments.lexers import XmlLexer
    from pygments.formatters import HtmlFormatter
    from pygments.styles import get_style_by_name

    xml_data = XML_data.objects.get(datafile__pk=dataset_file_id)

    formatted_xml = highlight(xml_data.data, XmlLexer(),
                              HtmlFormatter(style='default',
                              noclasses=True))

    c = Context({'formatted_xml': formatted_xml})
    return HttpResponse(render_response_index(request,
                        'tardis_portal/ajax/xml_data.html', c))


@dataset_access_required
def retrieve_datafile_list(request, dataset_id):
    from django.db.models import Count

    dataset_results = \
        Dataset_File.objects.filter(
        dataset__pk=dataset_id).order_by('filename')

    filename_search = None

    if 'filename' in request.GET and len(request.GET['filename']) \
        > 0:
        filename_search = request.GET['filename']
        dataset_results = \
            dataset_results.filter(url__icontains=filename_search)

    pgresults = 500
    if request.mobile:
        pgresults = 30
    else:
        pgresults = 500

    paginator = Paginator(dataset_results, pgresults)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.

    try:
        dataset = paginator.page(page)
    except (EmptyPage, InvalidPage):
        dataset = paginator.page(paginator.num_pages)

    c = Context({
        'dataset': dataset,
        'paginator': paginator,
        'dataset_id': dataset_id,
        'filename_search': filename_search,
        })
    return HttpResponse(render_response_index(request,
                        'tardis_portal/ajax/datafile_list.html', c))


@login_required()
def control_panel(request):

    experiments = get_owned_experiments(request.user.id)
    if experiments:
        experiments = experiments.order_by('title')

    c = Context({'experiments': experiments,
        'subtitle': 'Experiment Control Panel'})
    return HttpResponse(render_response_index(request,
                        'tardis_portal/control_panel.html', c))


@login_required()
def search_experiment(request):
    get = False
    experiments = get_accessible_experiments(request.user.id)
    if experiments:
        experiments = experiments.order_by('title')

        if 'results' in request.GET:
            get = True
            if 'title' in request.GET and len(request.GET['title']) > 0:
                experiments = \
                    experiments.filter(title__icontains=request.GET['title'])

            if 'description' in request.GET and \
                    len(request.GET['description']) > 0:
                experiments = \
                    experiments.filter(
                    description__icontains=request.GET['description'])

            if 'institution_name' in request.GET \
                    and len(request.GET['institution_name']) > 0:
                experiments = \
                    experiments.filter(
                    institution_name__icontains=request.GET[
                    'institution_name'])

            if 'creator' in request.GET and \
                    len(request.GET['creator']) > 0:
                experiments = \
                    experiments.filter(
                    author_experiment__author__name__icontains=request.GET[
                    'creator'])

    bodyclass = None
    if get:
        bodyclass = 'list'

    c = Context({
        'submitted': get,
        'experiments': experiments,
        'subtitle': 'Search Experiments',
        'nav': [{'name': 'Search Experiment',
            'link': '/search/experiment/'}],
        'bodyclass': bodyclass,
        'search_pressed': True,
        'searchDatafileSelectionForm': getNewSearchDatafileSelectionForm()})
    return HttpResponse(render_response_index(request,
                        'tardis_portal/search_experiment.html', c))


@login_required()
def search_quick(request):
    get = False
    experiments = Experiment.objects.all()
    experiments = Experiment.objects.order_by('title')

    if 'results' in request.GET:
        get = True
        if 'quicksearch' in request.GET \
            and len(request.GET['quicksearch']) > 0:
            experiments = \
                experiments.filter(
                title__icontains=request.GET['quicksearch']) | \
                experiments.filter(
                institution_name__icontains=request.GET['quicksearch']) | \
                experiments.filter(
                author_experiment__author__name__icontains=request.GET[
                'quicksearch']) | \
                experiments.filter(
                pdbid__pdbid__icontains=request.GET['quicksearch'])

            experiments = experiments.distinct()

            logger.debug(experiments)

    c = Context({'submitted': get, 'experiments': experiments,
                'subtitle': 'Search Experiments'})
    return HttpResponse(render_response_index(request,
                        'tardis_portal/search_experiment.html', c))


@login_required()
def __getFilteredDatafiles(request, searchQueryType, searchFilterData):
    """Filter the list of datafiles for the provided searchQueryType using the
    cleaned up searchFilterData.

    Arguments:
    request -- the HTTP request
    searchQueryType -- the type of query, 'mx' or 'sax'
    searchFilterData -- the cleaned up search form data

    Returns:
    A list of datafiles as a result of the query or None if the provided search
      request is invalid

    """

    #from django.db.models import Q

    datafile_results = \
        get_accessible_datafiles_for_user(
        get_accessible_experiments(request.user.id))

    # there's no need to do any filtering if we didn't find any
    # datafiles that the user has access to
    if len(datafile_results) == 0:
        return datafile_results

    datafile_results = \
        datafile_results.filter(
datafileparameterset__datafileparameter__name__schema__namespace__exact=constants.SCHEMA_DICT[
        searchQueryType]['datafile']).distinct()

    # if filename is searchable which i think will always be the case...
    if searchFilterData['filename'] != '':
        datafile_results = \
            datafile_results.filter(
            filename__icontains=searchFilterData['filename'])
    # TODO: might need to cache the result of this later on

    # get all the datafile parameters for the given schema
    # TODO: if p is searchable
    parameters = [p for p in
        ParameterName.objects.filter(
        schema__namespace__exact=constants.SCHEMA_DICT[searchQueryType]
        ['datafile'])]

    datafile_results = __filterParameters(parameters, datafile_results,
            searchFilterData, 'datafileparameterset__datafileparameter')

    # get all the dataset parameters for given schema
    # TODO: if p is searchable
    parameters = [p for p in
        ParameterName.objects.filter(
        schema__namespace__exact=constants.SCHEMA_DICT[searchQueryType]
        ['dataset'])]

    datafile_results = __filterParameters(parameters, datafile_results,
            searchFilterData, 'dataset__datasetparameterset__datasetparameter')

    # let's sort it in the end
    if datafile_results:
        datafile_results = datafile_results.order_by('filename')

    return datafile_results


def __filterParameters(
    parameters,
    datafile_results,
    searchFilterData,
    paramType,
    ):
    """Go through each parameter and apply it as a filter (together with its
    specified comparator) on the provided list of datafiles.

    Arguments:
    parameters -- list of ParameterNames model
    datafile_results -- list of datafile to apply the filter
    searchFilterData -- the cleaned up search form data
    paramType -- either 'datafile' or 'dataset'

    Returns:
    A list of datafiles as a result of the query or None if the provided search
      request is invalid

    """

    for parameter in parameters:
        kwargs = {paramType + '__name__name__icontains': parameter.name}
        try:

            # if parameter is a string...
            if not parameter.is_numeric:
                if searchFilterData[parameter.name] != '':
                    # let's check if this is a field that's specified to be
                    # displayed as a dropdown menu in the form
                    if parameter.choices != '':
                        if searchFilterData[parameter.name] != '-':
                            kwargs[paramType + '__string_value__iexact'] = \
                                searchFilterData[parameter.name]
                    else:
                        if parameter.comparison_type == \
                                ParameterName.EXACT_VALUE_COMPARISON:
                            kwargs[paramType + '__string_value__iexact'] = \
                                searchFilterData[parameter.name]
                        elif parameter.comparison_type == \
                                ParameterName.CONTAINS_COMPARISON:
                            # we'll implement exact comparison as 'icontains'
                            # for now
                            kwargs[paramType + '__string_value__icontains'] = \
                                searchFilterData[parameter.name]
                        else:
                            # if comparison_type on a string is a comparison type
                            # that can only be applied to a numeric value, we'll
                            # default to just using 'icontains' comparison
                            kwargs[paramType + '__string_value__icontains'] = \
                                searchFilterData[parameter.name]
                else:
                    pass
            else:  # parameter.is_numeric:
                if parameter.comparison_type == \
                        ParameterName.RANGE_COMPARISON:
                    fromParam = searchFilterData[parameter.name + 'From']
                    toParam = searchFilterData[parameter.name + 'To']
                    if fromParam is None and toParam is None:
                        pass
                    else:
                        # if parameters are provided and we want to do a range
                        # comparison
                        # note that we're using '1' as the lower range as using
                        # '0' in the filter would return all the data
                        # TODO: investigate on why the oddness above is
                        #       happening
                        # TODO: we should probably move the static value here
                        #       to the constants module
                        kwargs[paramType + '__numerical_value__range'] = \
                            (fromParam is None and
                             constants.FORM_RANGE_LOWEST_NUM or fromParam,
                             toParam is not None and toParam or
                             constants.FORM_RANGE_HIGHEST_NUM)

                elif searchFilterData[parameter.name] is not None:

                    # if parameter is an number and we want to handle other
                    # type of number comparisons
                    if parameter.comparison_type == \
                            ParameterName.EXACT_VALUE_COMPARISON:
                        kwargs[paramType + '__numerical_value__exact'] = \
                            searchFilterData[parameter.name]

                    # TODO: is this really how not equal should be declared?
                    #elif parameter.comparison_type ==
                    #       ParameterName.NOT_EQUAL_COMPARISON:
                    #   datafile_results = \
                    #       datafile_results.filter(
                    #  datafileparameter__name__name__icontains=parameter.name)
                    #       .filter(
                    #  ~Q(datafileparameter__numerical_value=searchFilterData[
                    #       parameter.name]))

                    elif parameter.comparison_type == \
                            ParameterName.GREATER_THAN_COMPARISON:
                        kwargs[paramType + '__numerical_value__gt'] = \
                            searchFilterData[parameter.name]
                    elif parameter.comparison_type == \
                            ParameterName.GREATER_THAN_EQUAL_COMPARISON:
                        kwargs[paramType + '__numerical_value__gte'] = \
                            searchFilterData[parameter.name]
                    elif parameter.comparison_type == \
                            ParameterName.LESS_THAN_COMPARISON:
                        kwargs[paramType + '__numerical_value__lt'] = \
                            searchFilterData[parameter.name]
                    elif parameter.comparison_type == \
                            ParameterName.LESS_THAN_EQUAL_COMPARISON:
                        kwargs[paramType + '__numerical_value__lte'] = \
                            searchFilterData[parameter.name]
                    else:
                        # if comparison_type on a numeric is a comparison type
                        # that can only be applied to a string value, we'll
                        # default to just using 'exact' comparison
                        kwargs[paramType + '__numerical_value__exact'] = \
                            searchFilterData[parameter.name]
                else:
                    # ignore...
                    pass

            # we will only update datafile_results if we have an additional
            # filter (based on the 'passed' condition) in addition to the
            # initial value of kwargs
            if len(kwargs) > 1:
                logger.debug(kwargs)
                datafile_results = datafile_results.filter(**kwargs)
        except KeyError:
            pass

    return datafile_results


def __forwardToSearchDatafileFormPage(request, searchQueryType,
        searchForm=None):
    """Forward to the search data file form page."""

    url = 'tardis_portal/search_datafile_form.html'
    if not searchForm:
        #if searchQueryType == 'sax':
        SearchDatafileForm = createSearchDatafileForm(searchQueryType)
        searchForm = SearchDatafileForm()
        #else:
        #    # TODO: what do we need to do if the user didn't provide a page to
        #            display?
        #    pass

    # TODO: remove this later on when we have a more generic search form
    if searchQueryType == 'mx':
        url = 'tardis_portal/search_datafile_form_mx.html'

    from itertools import groupby

    # sort the fields in the form as it will make grouping the related fields
    # together in the next step easier
    sortedSearchForm = sorted(searchForm, lambda x, y: cmp(x.name, y.name))

    # modifiedSearchForm will be used to customise how the range type of fields
    # will be displayed. range type of fields will be displayed side by side.
    modifiedSearchForm = [list(g) for k, g in groupby(
        sortedSearchForm, lambda x: x.name.rsplit('To')[0].rsplit('From')[0])]

    # the searchForm will be used by custom written templates whereas the
    # modifiedSearchForm will be used by the 'generic template' that the
    # dynamic search datafiles form uses.
    return render_to_response(url, {'username': request.user.username,
                              'searchForm': searchForm,
                              'modifiedSearchForm': modifiedSearchForm,
                              'searchDatafileSelectionForm':
                              getNewSearchDatafileSelectionForm()})


def __getSearchForm(request, searchQueryType):
    """Create the search form based on the HTTP GET request.

    Arguments:
    request -- The HTTP request object
    searchQueryType -- The search query type: 'mx' or 'sax'

    Returns:
    The supported search form

    Throws:
    UnsupportedSearchQueryTypeError is the provided searchQueryType is not
    supported

    """

    try:
        SearchDatafileForm = createSearchDatafileForm(searchQueryType)
        form = SearchDatafileForm(request.GET)
        return form
    except UnsupportedSearchQueryTypeError as e:
        raise e


def __processParameters(request, searchQueryType, form):
    """Validate the provided datafile search request and return search results.

    Arguments:
    request -- The HTTP request object
    searchQueryType -- The search query type
    form -- The search form to use

    Returns:
    A list of datafiles as a result of the query or None if the provided search
      request is invalid

    Throws:
    SearchQueryTypeUnprovidedError if searchQueryType is not in the HTTP GET
        request
    UnsupportedSearchQueryTypeError is the provided searchQueryType is not
        supported

    """

    if form.is_valid():

        datafile_results = __getFilteredDatafiles(request,
            searchQueryType, form.cleaned_data)

        # let's cache the query with all the filters in the session so
        # we won't have to keep running the query all the time it is needed
        # by the paginator
        request.session['datafileResults'] = datafile_results
        return datafile_results
    else:
        return None


@login_required()
def search_datafile(request):

    if 'type' in request.GET:
        searchQueryType = request.GET.get('type')
    else:
        # for now we'll default to MX if nothing is provided
        # TODO: should we forward the page to experiment search page if
        #       nothing is provided in the future?
        searchQueryType = 'mx'

    # TODO: check if going to /search/datafile will flag an error in unit test
    bodyclass = None

    if 'page' not in request.GET and 'type' in request.GET and \
            len(request.GET) > 1:
        # display the 1st page of the results

        form = __getSearchForm(request, searchQueryType)
        datafile_results = __processParameters(request, searchQueryType, form)
        if datafile_results is not None:
            bodyclass = 'list'
        else:
            return __forwardToSearchDatafileFormPage(
                request, searchQueryType, form)

    else:
        if 'page' in request.GET:
            # succeeding pages of pagination
            if 'datafileResults' in request.session:
                datafile_results = request.session['datafileResults']
            else:
                form = __getSearchForm(request, searchQueryType)
                datafile_results = __processParameters(request,
                    searchQueryType, form)
                if datafile_results is not None:
                    bodyclass = 'list'
                else:
                    return __forwardToSearchDatafileFormPage(request,
                        searchQueryType, form)
        else:
            # display the form
            if 'datafileResults' in request.session:
                del request.session['datafileResults']
            return __forwardToSearchDatafileFormPage(request, searchQueryType)

    # process the files to be displayed by the paginator...
    paginator = Paginator(datafile_results,
                          constants.DATAFILE_RESULTS_PER_PAGE)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of :range, deliver last page of results.
    try:
        datafiles = paginator.page(page)
    except (EmptyPage, InvalidPage):
        datafiles = paginator.page(paginator.num_pages)

    import re
    cleanedUpQueryString = re.sub('&page=\d+', '',
        request.META['QUERY_STRING'])

    c = Context({
        'datafiles': datafiles,
        'paginator': paginator,
        'query_string': cleanedUpQueryString,
        'subtitle': 'Search Datafiles',
        'nav': [{'name': 'Search Datafile', 'link': '/search/datafile/'}],
        'bodyclass': bodyclass,
        'search_pressed': True,
        'searchDatafileSelectionForm': getNewSearchDatafileSelectionForm()})
    url = 'tardis_portal/search_datafile_results.html'
    return HttpResponse(render_response_index(request, url, c))


@login_required()
def retrieve_user_list(request):

    users = User.objects.all().order_by('username')

    c = Context({'users': users})
    return HttpResponse(render_response_index(request,
                        'tardis_portal/ajax/user_list.html', c))


@experiment_ownership_required
def retrieve_access_list(request, experiment_id):

    users = \
        User.objects.filter(groups__name=experiment_id).order_by('username')

    c = Context({'users': users, 'experiment_id': experiment_id})
    return HttpResponse(render_response_index(request,
                        'tardis_portal/ajax/access_list.html', c))


@experiment_ownership_required
def add_access_experiment(request, experiment_id, username):
    try:
        u = User.objects.get(username=username)

        g = Group.objects.get(name=experiment_id)

        if not in_group(u, g):
            u.groups.add(g)

            c = Context({'user': u, 'experiment_id': experiment_id})
            return HttpResponse(render_response_index(request,
                                'tardis_portal/ajax/add_user_result.html', c))
        else:
            return return_response_error(request)
    except User.DoesNotExist, ue:

        return return_response_not_found(request)
    except Group.DoesNotExist, ge:
        return return_response_not_found(request)

    return return_response_error(request)


@experiment_ownership_required
def remove_access_experiment(request, experiment_id, username):

    try:
        u = User.objects.get(username=username)

        g = Group.objects.get(name=experiment_id)

        e = Experiment.objects.get(pk=experiment_id)

        if in_group(u, g):
            u.groups.remove(g)

            try:
                eo = Experiment_Owner.objects.filter(experiment=e,
                        user=u)
                eo.delete()
            except Experiment_Owner.DoesNotExist, eo:
                pass

            c = Context({})
            return HttpResponse(render_response_index(request,
                'tardis_portal/ajax/remove_user_result.html', c))
        else:
            return return_response_error(request)
    except User.DoesNotExist, ue:

        return return_response_not_found(request)
    except Group.DoesNotExist, ge:
        return return_response_not_found(request)
    except Experiment.DoesNotExist, ge:
        return return_response_not_found(request)

    return return_response_error(request)


@experiment_ownership_required
def publish_experiment(request, experiment_id):

    experiment = Experiment.objects.get(id=experiment_id)

    if not experiment.public:
        filename = settings.FILE_STORE_PATH + '/' + experiment_id + \
            '/METS.XML'

        mpform = MultiPartForm()
        mpform.add_field('username', settings.TARDIS_USERNAME)
        mpform.add_field('password', settings.TARDIS_PASSWORD)
        mpform.add_field('url', settings.TARDISURLPREFIX + '/')
        mpform.add_field('mytardis_id', experiment_id)

        f = open(filename, 'r')

        # Add a fake file

        mpform.add_file('xmldata', 'METS.xml', fileHandle=f)

        logger.debug('about to send register request to site')

        # Build the request

        requestmp = urllib2.Request(settings.TARDIS_REGISTER_URL)
        requestmp.add_header('User-agent',
                             'PyMOTW (http://www.doughellmann.com/PyMOTW/)')
        body = str(mpform)
        requestmp.add_header('Content-type', mpform.get_content_type())
        requestmp.add_header('Content-length', len(body))
        requestmp.add_data(body)

        print
        logger.debug('OUTGOING DATA:')
        logger.debug(requestmp.get_data())

        print
        logger.debug('SERVER RESPONSE:')
        logger.debug(urllib2.urlopen(requestmp).read())

        experiment.public = True
        experiment.save()

        c = Context({})
        return HttpResponse(render_response_index(request,
                            'tardis_portal/index.html', c))
    else:
        return return_response_error(request)


def stats(request):

    # stats

    public_datafiles = Dataset_File.objects.filter()
    public_experiments = Experiment.objects.filter()

    size = 0
    for df in public_datafiles:
        size = size + long(df.size)

    public_datafile_size = size

    c = Context({'public_datafiles': len(public_datafiles),
                'public_experiments': len(public_experiments),
                'public_datafile_size': public_datafile_size})
    return HttpResponse(render_response_index(request,
                        'tardis_portal/stats.html', c))


def import_params(request):
    if request.method == 'POST':  # If the form has been submitted...

        # A form bound to the POST data
        form = ImportParamsForm(request.POST, request.FILES)
        if form.is_valid():  # All validation rules pass

            params = request.FILES['params']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            from django.contrib.auth import authenticate
            user = authenticate(username=username, password=password)
            if user is not None:
                if not user.is_active or not user.is_staff:
                    return return_response_error(request)
            else:
                return return_response_error(request)

            i = 0
            for line in params:
                if i == 0:
                    prefix = line
                    logger.debug(prefix)
                elif i == 1:
                    schema = line
                    logger.debug(schema)

                    try:
                        Schema.objects.get(namespace=schema)
                        return HttpResponse('Schema already exists.')
                    except Schema.DoesNotExist, s:
                        schema_db = Schema(namespace=schema)
                        schema_db.save()
                else:
                    part = line.split('^')
                    if len(part) == 4:

                        is_numeric = False
                        if part[3].strip(' \n\r') == 'True':
                            is_numeric = True

                        pn = ParameterName(schema=schema_db,
                                name=part[0], full_name=part[1],
                                units=part[2], is_numeric=is_numeric)
                        pn.save()

                i = i + 1

            return HttpResponse('OK')
    else:
        form = ImportParamsForm()

    c = Context({'form': form, 'subtitle': 'Import Parameters'})
    return HttpResponse(render_response_index(request,
                        'tardis_portal/import_params.html', c))