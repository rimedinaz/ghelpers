"""
Grouping of common functions used in Google Cloud Platform, intended to help other processes.
@maintainer: Richard Medina (rimedinaz at gmail dot com)
"""


def get_default_project():
    try:
        import google.auth
        default_credentials, default_project = google.auth.default()
    except Exception as e:
        print(e)
        default_project = None

    import os
    if default_project:
        return default_project
    elif 'GCP_PROJECT' in os.environ:
        return os.environ['GCP_PROJECT']
    elif 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
        import json
        with open(os.environ['GOOGLE_APPLICATION_CREDENTIALS'], 'r') as fp:
            credentials = json.load(fp)
        return credentials['project_id']
    else:
        raise Exception('Failed to determine project_id')


def get_default_account():
    import google.auth
    default_credentials, default_project = google.auth.default()
    return default_credentials.service_account_email


def get_default_credentials():
    import google.auth
    default_credentials, default_project = google.auth.default()
    return default_credentials


def get_secret(secret_name, project_id=None, version="latest"):
    """
    Access a secret from Google Secret Manager
    :param string secret_name: A Secret Manager secret name
    :param string project_id: Google Cloud project ID, otherwise use default
    :param string version: Define a specific version to use, otherwise use latest
    :return: A plaintext secret value
    """

    if project_id is None:
        project_id = get_default_project()

    from google.cloud import secretmanager
    client = secretmanager.SecretManagerServiceClient()
    secret = f"projects/{project_id}/secrets/{secret_name}/versions/{version}"

    try:
        response = client.access_secret_version(request={
            "name": secret
        })
    except Exception as e:
        return e

    return response.payload.data.decode("UTF-8").strip()

def get_secrets(secret_name, format='yaml'):
    """
    Get secrets as Python Dict
    :param secret_name:
    :param format:
    :return:
    """
    if format == 'yaml':
        import yaml
        yaml_text = get_secret(secret_name)
        secrets = yaml.safe_load(yaml_text)
        return secrets
    else:
        raise Exception(f"Format {format} not supported")

