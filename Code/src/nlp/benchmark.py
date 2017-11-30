from trie_run import external_run


def benchmark(file: str) -> float:

    with open(file) as f:
        content = f.readlines()

    time = [external_run(x) for x in content]

    return (sum(time) * 1.0) / len(time)


if __name__ == "__main__":
    print(benchmark("test.txt"))
