import argparse
from xia_framework import Cosmos, Foundation


def main():
    # Top level parser
    parser = argparse.ArgumentParser(description='Foundation tools')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Create the parser for the "bigbang" command
    parser_bigbang = subparsers.add_parser('bigbang', help='Execute the Big Bang command')
    parser_bigbang.add_argument('-n', '--realm_name', type=str, help='Realm name to Bigbang')
    parser_bigbang.add_argument('-p', '--realm_project', type=str, help='Realm project to Bigbang')

    # Create the parser for the "birth" command
    parser_birth = subparsers.add_parser('birth', help='Create the current repo related foundation')
    parser_birth.add_argument('-n', '--foundation_name', type=str, help='Foundation name to birth')

    # Create the parser for the "prepare" command
    parser_prepare = subparsers.add_parser('prepare', help='Prepare current configurations')
    parser_prepare.add_argument('--skip_terraform', action='store_true', help='Skip Terraform steps')

    # Create the parser for the "init-module" command
    parser_install = subparsers.add_parser('init-module', help='Install a module')
    parser_install.add_argument('-m', '--module_class', type=str, help='Name of the module class to install')
    parser_install.add_argument('-p', '--package', type=str, help='Name of the package to install')

    # Create the parser for the "create-app" command
    parser_create = subparsers.add_parser('create-app', help='Create an application')
    parser_create.add_argument('-n', '--app_name', type=str, help='Name of the application to create')

    # Parse the arguments
    args = parser.parse_args()

    # Handle different commands
    cosmos = Cosmos()
    foundation = Foundation()
    if args.command == 'bigbang':
        cosmos.bigbang(cosmos_name=args.realm_project, realm_name=args.realm_name)
    if args.command == 'birth':
        foundation.birth(foundation_name=args.foundation_name)
    if args.command == 'prepare':
        foundation.prepare(args.skip_terraform)
    elif args.command == 'init-module':
        foundation.init_module(package=args.package, module_class=args.module_class)
    elif args.command == 'create-app':
        foundation.create_app(app_name=args.app_name)
    else:
        # If no command is provided, show help
        parser.print_help()


if __name__ == "__main__":
    main()
