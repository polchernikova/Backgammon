from model import Model


def main():
    m = Model(units=40, lamda=0.7, alpha=0.1)
    m.train()


if __name__ == "__main__":
    main()
