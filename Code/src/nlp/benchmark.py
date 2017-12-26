from complete import autocomplete
import time


def benchmark(file: str) -> float:
    """
    Benchmark the average time it takes to find the next word from a file
    :param file: A file that lists the words to complete, separated by newline
    :return: the average time to predict the words
    """
    with open(file) as f:
        content = f.readlines()

    time_total = [outer(x) for x in content]

    return (sum(time_total) * 1.0) / len(time_total)


def outer(word: str) -> float:
    """
    A wrapper for the autocomplete function, to make it time each call
    :param word: A word to complete
    :return: time it takes to complete the word
    """
    start = time.time()
    autocomplete(word)
    return (time.time() - start) * 1000.0


if __name__ == "__main__":
    print(benchmark("test.txt"))
