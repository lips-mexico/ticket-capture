from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def supervisor_required(function = None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='home'):

    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_supervisor,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    if function:
        return actual_decorator(function)
    return actual_decorator

def typist_required(function = None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_typist,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    if function:
        return actual_decorator(function)
    return actual_decorator

def classifier_required(function = None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_classifield,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    if function:
        return actual_decorator(function)
    return actual_decorator