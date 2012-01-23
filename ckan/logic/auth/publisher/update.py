from ckan.logic import check_access_old, NotFound
from ckan.logic.auth import get_package_object, get_group_object, get_authorization_group_object, \
    get_user_object, get_resource_object
from ckan.logic.auth.publisher import _groups_intersect
from ckan.logic.auth.create import check_group_auth, package_relationship_create
from ckan.authz import Authorizer
from ckan.lib.base import _

def make_latest_pending_package_active(context, data_dict):
    return package_update(context, data_dict)

def package_update(context, data_dict):
    model = context['model']
    user = context.get('user')
    package = get_package_object(context, data_dict)

    userobj = model.User.get( user )
    
    # Only allow package update if the user and package groups intersect
    if not _groups_intersect( userobj.get_groups(), package.get_groups() ):
        return {'success': False, 'msg': _('User %s not authorized to edit packages in these groups') % str(user)}
        
    check1 = check_access_old(package, model.Action.EDIT, context)
    if not check1:
        return {'success': False, 'msg': _('User %s not authorized to edit package %s') % (str(user), package.id)}
    else:
        check2 = check_group_auth(context,data_dict)
        if not check2:
            return {'success': False, 'msg': _('User %s not authorized to edit these groups') % str(user)}

    return {'success': True}

def resource_update(context, data_dict):
    model = context['model']
    user = context.get('user')
    resource = get_resource_object(context, data_dict)

    # Only allow resource update if the user and resource packages groups intersect
    userobj = model.User.get( user )
    if not _groups_intersect( userobj.get_groups(), resource.package.get_groups() ):
        return {'success': False, 'msg': _('User %s not authorized to edit resources in this package') % str(user)}

    # check authentication against package
    query = model.Session.query(model.Package)\
        .join(model.ResourceGroup)\
        .join(model.Resource)\
        .filter(model.ResourceGroup.id == resource.resource_group_id)
    pkg = query.first()
    if not pkg:
        raise NotFound(_('No package found for this resource, cannot check auth.'))
    
    pkg_dict = {'id': pkg.id}
    authorized = package_update(context, pkg_dict).get('success')
    
    if not authorized:
        return {'success': False, 'msg': _('User %s not authorized to read edit %s') % (str(user), resource.id)}
    else:
        return {'success': True}

def package_relationship_update(context, data_dict):
    return package_relationship_create(context, data_dict)

def package_change_state(context, data_dict):
    model = context['model']
    user = context['user']
    package = get_package_object(context, data_dict)

    userobj = model.User.get( user )
    if not _groups_intersect( userobj.get_groups(), package.get_groups() ):
        return {'success': False, 'msg': _('User %s not authorized to change this package state') % str(user)}

    authorized = check_access_old(package, model.Action.CHANGE_STATE, context)
    if not authorized:
        return {'success': False, 'msg': _('User %s not authorized to change state of package %s') % (str(user),package.id)}
    else:
        return {'success': True}

def package_edit_permissions(context, data_dict):
    model = context['model']
    user = context['user']
    package = get_package_object(context, data_dict)

    # Only allow package update if the user and package groups intersect
    userobj = model.User.get( user )
    if not _groups_intersect( userobj.get_groups(), package.get_groups() ):
        return {'success': False, 'msg': _('User %s not authorized to edit permissions of this package') % str(user)}

    authorized = check_access_old(package, model.Action.EDIT_PERMISSIONS, context)
    if not authorized:
        return {'success': False, 'msg': _('User %s not authorized to edit permissions of package %s') % (str(user),package.id)}
    else:
        return {'success': True}

def group_update(context, data_dict):
    model = context['model']
    user = context['user']
    group = get_group_object(context, data_dict)

    # Only allow package update if the user and package groups intersect
    userobj = model.User.get( user )
    if not _groups_intersect( userobj.get_groups(), group.get_groups() ):
        return {'success': False, 'msg': _('User %s not authorized to edit this group') % str(user)}

    authorized = check_access_old(group, model.Action.EDIT, context)
    if not authorized:
        return {'success': False, 'msg': _('User %s not authorized to edit group %s') % (str(user),group.id)}
    else:
        return {'success': True}

def group_change_state(context, data_dict):
    model = context['model']
    user = context['user']
    group = get_group_object(context, data_dict)

    userobj = model.User.get( user )
    if not _groups_intersect( userobj.get_groups(), group.get_groups() ):
        return {'success': False, 'msg': _('User %s not authorized to change state of group') % str(user)}
    
    authorized = check_access_old(group, model.Action.CHANGE_STATE, context)
    if not authorized:
        return {'success': False, 'msg': _('User %s not authorized to change state of group %s') % (str(user),group.id)}
    else:
        return {'success': True}

def group_edit_permissions(context, data_dict):
    model = context['model']
    user = context['user']
    group = get_group_object(context, data_dict)

    # Only allow package update if the user and package groups intersect
    userobj = model.User.get( user )
    if not _groups_intersect( userobj.get_groups(), group.get_groups() ):
        return {'success': False, 'msg': _('User %s not authorized to edit permissions of group') % str(user)}
    
    authorized = check_access_old(group, model.Action.EDIT_PERMISSIONS, context)
    if not authorized:
        return {'success': False, 'msg': _('User %s not authorized to edit permissions of group %s') % (str(user),group.id)}
    else:
        return {'success': True}

def authorization_group_update(context, data_dict):
    model = context['model']
    user = context['user']
    authorization_group = get_authorization_group_object(context, data_dict)

    authorized = check_access_old(authorization_group, model.Action.EDIT, context)
    if not authorized:
        return {'success': False, 'msg': _('User %s not authorized to edit permissions of authorization group %s') % (str(user),authorization_group.id)}
    else:
        return {'success': True}

def authorization_group_edit_permissions(context, data_dict):
    model = context['model']
    user = context['user']
    authorization_group = get_authorization_group_object(context, data_dict)

    authorized = check_access_old(authorization_group, model.Action.EDIT_PERMISSIONS, context)
    if not authorized:
        return {'success': False, 'msg': _('User %s not authorized to edit permissions of authorization group %s') % (str(user),authorization_group.id)}
    else:
        return {'success': True}

def user_update(context, data_dict):
    model = context['model']
    user = context['user']
    user_obj = get_user_object(context, data_dict)

    if not (Authorizer().is_sysadmin(unicode(user)) or user == user_obj.name) and \
       not ('reset_key' in data_dict and data_dict['reset_key'] == user_obj.reset_key):
        return {'success': False, 'msg': _('User %s not authorized to edit user %s') % (str(user), user_obj.id)}

    # Only allow package update if the user and package groups intersect or user is editing self
    if (user != user_obj.name) and 
        not _groups_intersect( current_user.get_groups(), user_obj.get_groups() ):
        return {'success': False, 'msg': _('User %s not authorized to edit user') % str(user)}

    return {'success': True}

def revision_change_state(context, data_dict):
    model = context['model']
    user = context['user']

    authorized = Authorizer().is_authorized(user, model.Action.CHANGE_STATE, model.Revision)
    if not authorized:
        return {'success': False, 'msg': _('User %s not authorized to change state of revision' ) % str(user)}
    else:
        return {'success': True}

def task_status_update(context, data_dict):
    model = context['model']
    user = context['user']

    authorized =  Authorizer().is_sysadmin(unicode(user))
    if not authorized:
        return {'success': False, 'msg': _('User %s not authorized to update task_status table') % str(user)}
    else:
        return {'success': True}

## Modifications for rest api

def package_update_rest(context, data_dict):
    model = context['model']
    user = context['user']
    if user in (model.PSEUDO_USER__VISITOR, ''):
        return {'success': False, 'msg': _('Valid API key needed to edit a package')}

    return package_update(context, data_dict)

def group_update_rest(context, data_dict):
    model = context['model']
    user = context['user']
    if user in (model.PSEUDO_USER__VISITOR, ''):
        return {'success': False, 'msg': _('Valid API key needed to edit a group')}

    return group_update(context, data_dict)
