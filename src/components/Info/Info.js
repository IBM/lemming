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
        if (
            atoms[i].indexOf('NegatedAtom') === -1 &&
            atoms[i].indexOf('Atom') > -1
        )
            description.push(atoms[i].split(' ')[1]);

    return description.join('<br/>');
}

function parseEdgeName(raw_string) {
    const reg = /"(.*)"/g;
    const trimmed_raw_string = raw_string.trim();
    const regexec = reg.exec(trimmed_raw_string);

    if (regexec && regexec.length > 1) return regexec[1].trim();

    return trimmed_raw_string;
}

function rawNodeTransform(raw_node) {
    return {
        ...raw_node,
        label: '',
        description: raw_node.label,
        data: { description: raw_node.label },
    };
}

function getDanglyNodes(state) {
    var node_names = state.graph.nodes.map(item => item.id);
    node_names = new Set(node_names);

    for (var i = 0; i < state.graph.links.length; i++) {
        var target = state.graph.links[i].target;
        if (node_names.has(target)) node_names.delete(target);
    }

    return node_names;
}

function generateNodes(state) {
    if (!state.graph || !state.graph.nodes) return [];

    var dangly_nodes = getDanglyNodes(state);
    var transformed_nodes = state.graph.nodes.map((item, id) => {
        return rawNodeTransform(item);
    });

    if (dangly_nodes.size > 1)
        transformed_nodes.push({
            id: 'MORE',
            label: 'MORE',
            description: 'MORE',
            data: { description: 'MORE' },
        });

    return transformed_nodes;
}

function generateEdges(state) {
    if (!state.graph || !state.graph.links) return [];

    var edges = state.graph.links.map((item, id) => {
        return {
            ...item,
            id: id,
            size: 2,
        };
    });

    var dangly_nodes = getDanglyNodes(state);
    var dangly_edges = [];

    if (dangly_nodes.size > 1)
        dangly_edges = Array.from(dangly_nodes).map((item, i) => {
            return {
                id: state.graph.links.length + i,
                key: 0,
                label: 'BUILD',
                size: 2,
                source: 'MORE',
                target: item,
            };
        });

    edges = edges.concat(dangly_edges);
    return edges;
}

function getBasisNodes(state, all_flag) {
    var basis_nodes = [];

    if (state.choice_infos.length > 0) {
        var transform = state.choice_infos.filter(
            item => item.is_available_for_choice
        );

        if (transform.length > 0 && !all_flag) transform = [transform[0]];

        basis_nodes = transform
            .map(item => item.nodes_with_multiple_out_edges)
            .reduce((bag, item) => bag.concat(item), []);
    }

    return basis_nodes;
}

function getActiveNodes(state, all_flag) {
    if (!state.graph || !state.graph.nodes) return [];

    const basis_nodes = getBasisNodes(state, all_flag);
    return basis_nodes === null
        ? []
        : state.graph.links
              .filter(item => basis_nodes.indexOf(item.source) > -1)
              .map(item => item.target)
              .concat(basis_nodes);
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
    generateDescription,
    generateStateDescription,
    generateNodes,
    generateEdges,
    getActiveNodes,
    getBasisNodes,
    rawNodeTransform,
    parseEdgeName,
    generateURL,
    shuffleArray,
};
