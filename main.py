import sys

from serveripfinder import ServerIPFinder


def main():
    if len(sys.argv) < 2:
        print('This program captures network packets to get server IP addresses for realms and multiplayer games.')
        print('usage: ipfinder interface')
        return

    finder = ServerIPFinder()
    input(
        '--- Start the capture ---\n'
        'Before you start the capture, join the server to get an IP address.\n'
        'Press Enter to continue...\n'
    )
    print('Capturing...')
    finder.get_destinations(sys.argv[1])
    print()
    print('--- Servers ---')
    print('IP             | Port')
    for ip, port in finder.destinations.items():
        print('{:<16} {}'.format(ip, port))
    print()
    print('--- Check if MCBE server ---')
    print('Ping to check if the destination is a Minecraft Bedrock Edtion server.')
    input('Press Enter to continue...\n')
    print('Checking...')
    servers = finder.get_mc_servers()
    print()
    print('--- Valid servers ---')
    for server in servers:
        print("{}:{}".format(server[0], server[1]))
        print("{}({}) {}/{}".format(
            server[2].server_name,
            server[2].game_version,
            server[2].num_players,
            server[2].max_players)
        )
        print(server[2].motd)
        print()


if __name__ == "__main__":
    main()
