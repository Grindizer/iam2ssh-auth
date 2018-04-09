import boto3
from contextlib import contextmanager

@contextmanager
def assume_role(role, session_name="NewSession"):
    """
    Usage :
        with assume_role("somerole") as readonly:
            iam = readonly.client('iam')
    """
    if not role:
        return (yield boto3.Session())
    client = boto3.client('sts')
    response = client.assume_role(RoleArn=role, RoleSessionName=session_name)
    yield boto3.Session(
        aws_access_key_id=response['Credentials']['AccessKeyId'],
        aws_secret_access_key=response['Credentials']['SecretAccessKey'],
        aws_session_token=response['Credentials']['SessionToken'])


def list_ssh_public_keys_for_group(group_name, iam_session):
    group = iam_session.get_group(GroupName=group_name)
    for user in group['Users']:
        user_name = user['UserName']
        sshkeys = iam_session.list_ssh_public_keys(UserName=user_name)
        for sshkey in sshkeys['SSHPublicKeys']:
            if sshkey['Status'] == 'Active':
                sshkey_id = sshkey['SSHPublicKeyId']
                public_key = iam_session.get_ssh_public_key(UserName=user_name,
                                                            SSHPublicKeyId=sshkey_id,
                                                            Encoding='SSH')
                yield public_key


def get_authorized_keys(group_name, source_role):
    with assume_role(source_role, 'authorizedkeysLookup') as iam_account:
        iam_session = iam_account.client('iam')
        for key in list_ssh_public_keys_for_group(group_name, iam_session):
            if 'SSHPublicKey' in key:
                yield key['SSHPublicKey']
