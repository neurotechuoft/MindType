from autocomplete import autocompl


def benchmark(file: str) -> float:

    with open(file) as f:
        content = f.readlines()

    time = [autocompl(x) for x in content]

    return (sum(time) * 1.0) / len(time)


if __name__ == "__main__":
    print(benchmark("test.txt"))
