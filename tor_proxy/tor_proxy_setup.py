from faker import Faker

fake = Faker(["en_US", "en_GB", "en_CA", "en_AU", "en_NZ", "en_IE", "en_IN"])

# Set the number of uniquely named proxies to generate and the IP change interval
NUM_PROXIES = 5
IP_CHANGE_SECONDS = 60


def generate_files(num_proxies):
    names = set()
    while len(names) < num_proxies:
        name = fake.first_name().lower()
        names.add(name)

    names = list(names)
    warning = "# Generated by tor_proxy_setup script.\n\n"

    # Generate docker-compose.yml
    with open("docker-compose.yml", "w") as f:
        f.write(warning)
        f.write("services:\n")

        for index, name in enumerate(names):
            f.write(f"  tor-{name}:\n")
            f.write(f"    container_name: 'tor-{name}'\n")
            f.write("    image: 'pickapp/tor-proxy:latest'\n")
            f.write("    ports:\n")
            f.write(f"      - '{9990+index}:8888'\n")
            f.write("    environment:\n")
            f.write(f"      - IP_CHANGE_SECONDS={IP_CHANGE_SECONDS}\n")
            f.write("    restart: always\n")

    # Generate proxy_list.txt
    with open("proxy_list.txt", "w") as f:
        f.write(warning)

        for index, name in enumerate(names):
            f.write(f"http://127.0.0.1:{9990+index}\n")


if __name__ == "__main__":
    generate_files(NUM_PROXIES)
