// Function to shuffle an array.
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

// Return a random array containing 0 to maxSize - 1.
export function getRandomArray(maxSize) {
    const newArray = [...Array(maxSize).keys()];
    shuffleArray(newArray);
    return newArray;
}