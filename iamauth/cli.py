import sys
from cliff.app import App
from cliff.commandmanager import CommandManager
from cliff.lister import Lister
from . core import get_authorized_keys


class IamAuthApp(App):
    def __init__(self):
        super(IamAuthApp, self).__init__(
            description='Manage ssh authorized keys based on aws iam users.',
            version='0.1',
            command_manager=CommandManager('cliff.iamauth.commands'),
            deferred_help=True,
        )


class AuthorizedKeys(Lister):
    formatter_default = 'value'

    def get_parser(self, prog_name):
        parser = super(AuthorizedKeys, self).get_parser(prog_name)
        parser.add_argument('--group-name', '-g', help="The name of the group from which "
                                                       "to get the public ssh keys", required=True, dest='group')
        parser.add_argument('--source-account-role-arn', '-r', help="Thr ARN of the role to assume within the account "
                                                                    "that manages the iam users", default='',
                            dest='role')
        return parser

    def take_action(self, args):
        return (
            ('UserName', 'SSHPublicKeyId', 'Status', 'SSHPublicKeyBody'),
            (
                (key['UserName'], key['SSHPublicKeyId'], key['Status'], key['SSHPublicKeyBody'])
                for key in get_authorized_keys(args.group, args.role)
            )
        )


def main(argv=sys.argv[1:]):
    app = IamAuthApp()
    return app.run(argv)

if __name__ == '__main__':
    main()
