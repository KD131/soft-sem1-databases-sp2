from graphdatascience import GraphDataScience
from modules.secrets import NEO4J_AUTH, NEO4J_URI


def main():
    gds = GraphDataScience(NEO4J_URI, NEO4J_AUTH)
    print(gds.version())

if __name__ == "__main__":
    main()