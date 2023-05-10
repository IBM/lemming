function generateURL(dir, file, ext) {
  return `${process.env.PUBLIC_URL}${dir}/${file}.${ext}`;
}

function shuffleArray(array) {
  var newArray = [...array];
  let i = newArray.length - 1;
  for (; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    const temp = newArray[i];
    newArray[i] = newArray[j];
    newArray[j] = temp;
  }
  return newArray;
}

export { generateURL, shuffleArray };
