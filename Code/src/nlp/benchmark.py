from complete import compl
import time


def benchmark(file: str) -> float:

    with open(file) as f:
        content = f.readlines()

    time_total = [outer(x) for x in content]

    return (sum(time_total) * 1.0) / len(time_total)


def outer(word: str) -> float:
    start = time.time()
    compl(word)
    return (time.time() - start) * 1000.0


if __name__ == "__main__":
    print(benchmark("test.txt"))
