function generateDescription(data) {
  if (data.label) {
    return parseEdgeName(data.label);
  } else if (data.data.description) {
    return generateStateDescription(data.data.description);
  }

  return '';
}

function generateStateDescription(raw_string) {
  const atoms = raw_string.split('\n');
  var description = [];

  for (var i = 0; i < atoms.length; i++)
    if (atoms[i].indexOf('NegatedAtom') === -1 && atoms[i].indexOf('Atom') > -1)
      description.push(atoms[i].split(' ')[1]);

  return description.join('<br/>');
}

function parseEdgeName(raw_string) {
  const reg = /"(.*)"/g;
  const label = reg.exec(raw_string)[1].trim();

  return label;
}

function generateURL(dir, file, ext) {
  return `${process.env.PUBLIC_URL}${dir}/${file}.${ext}`;
}

// From: https://stackoverflow.com/questions/2450954
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

export {
  generateURL,
  shuffleArray,
  generateDescription,
  generateStateDescription,
  parseEdgeName,
};
