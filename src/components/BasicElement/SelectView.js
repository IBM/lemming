import React, { useRef, useState } from 'react';
import {
    generateDescription,
    generateEdgeKey,
    parseEdgeName,
    generateNodes,
    generateEdges,
    getActiveNodes,
    getBasisNodes,
    rawNodeTransform,
} from '../../components/Info';
import { GraphCanvas, lightTheme } from 'reagraph';
import { Grid, Column, Button, Tile, Toggle } from '@carbon/react';

const init_feedback =
    "Right click on the nodes and edges to find what's in them. Click on an edge to enforce all plans with that action. Use commit mode to commit multiple selections together.";

const SelectView = props => {
    const nodes = generateNodes(props.state);
    const edges = generateEdges(props.state);
    const actives = getActiveNodes(props.state);

    const ref = useRef(null);
    const [commits] = useState([]);

    const [commit_mode, setCommitMode] = useState(false);
    const [feedback_text, setFeedbackText] = useState(init_feedback);

    const setCommits = edge => {
        if (!edge) {
            commits.splice(0, commits.length);
        } else {
            const indexOf = commits.indexOf(edge);

            if (indexOf > -1) {
                commits.splice(indexOf, 1);
            } else {
                commits.push(edge);
            }
        }

        if (commits.length > 0) {
            const commit_msg =
                'Selected edges: <strong>' +
                commits.map(item => item.name).join(', ') +
                "</strong>. Don't forget to commit!";
            setFeedbackText(commit_msg);
        } else {
            setFeedbackText(init_feedback);
        }
    };

    const onEdgeClick = edge => {
        const label = parseEdgeName(edge.label);
        const selection_item = { name: label, key: generateEdgeKey(edge) };

        if (commit_mode) {
            setCommits(selection_item);
        } else {
            props.onEdgeClick(selection_item);
        }
    };

    const commitChanges = e => {
        if (commits.length > 0) props.commitChanges(commits);

        setCommits();
    };

    const onFocus = e => {
        const basis_nodes = getBasisNodes(props.state);

        if (basis_nodes) {
            const random_idx = Math.floor(Math.random() * basis_nodes.length);
            const basis_node = basis_nodes[random_idx];

            const raw_graph_node = props.state.graph.nodes.filter(
                item => item.id === basis_node
            )[0];

            setFeedbackText(
                generateDescription(rawNodeTransform(raw_graph_node))
            );
            ref.current?.centerGraph([basis_node]);
            ref.current?.zoomIn();
        }
    };

    return (
        <Grid>
            <Column lg={16} md={8} sm={4}>
                {nodes.length > 0 && !props.no_feedback && (
                    <div className="hover-zone">
                        <Toggle
                            aria-label="toggle commit mode"
                            id="toggle-commit-mode"
                            size="sm"
                            labelText=""
                            labelA="Commit Mode OFF"
                            labelB="Commit Mode ON"
                            toggled={commit_mode}
                            onClick={() => setCommitMode(!commit_mode)}
                        />
                        <br />
                        <br />

                        <Tile className="hover-zone-tile">
                            <div
                                dangerouslySetInnerHTML={{
                                    __html: feedback_text,
                                }}
                            />
                        </Tile>
                        <br />
                        <Button
                            style={{ width: '100px' }}
                            kind="tertiary"
                            size="sm"
                            onClick={onFocus}>
                            Focus
                        </Button>

                        {commit_mode && (
                            <Button
                                style={{ marginLeft: '10px', width: '100px' }}
                                kind="tertiary"
                                size="sm"
                                onClick={commitChanges}>
                                Commit
                            </Button>
                        )}
                    </div>
                )}

                <div className="canvas-holder">
                    {nodes.length > 0 && (
                        <GraphCanvas
                            ref={ref}
                            theme={{
                                ...lightTheme,
                                canvas: { background: 'white' },
                            }}
                            labelType="edges"
                            edgeLabelPosition="inline"
                            layoutType="hierarchicalTd"
                            nodes={nodes}
                            edges={edges}
                            actives={actives}
                            onNodeClick={node =>
                                setFeedbackText(generateDescription(node))
                            }
                            onEdgeClick={edge => onEdgeClick(edge)}
                            contextMenu={({ data, additional, onClose }) => (
                                <div
                                    className="node-pop"
                                    style={{
                                        background: 'white',
                                        width: 250,
                                        height: 150,
                                        border: 'solid 1px #0d62fe',
                                        borderRadius: 2,
                                        padding: 10,
                                        textAlign: 'left',
                                        marginTop: '25px',
                                        fontSize: 'smaller',
                                        lineHeight: 'normal',
                                    }}>
                                    <div
                                        dangerouslySetInnerHTML={{
                                            __html: generateDescription(data),
                                        }}
                                    />
                                    <br />
                                    <br />
                                    <div
                                        style={{
                                            position: 'absolute',
                                            bottom: 10,
                                            left: 10,
                                        }}>
                                        <Button
                                            size="sm"
                                            kind="tertiary"
                                            onClick={onClose}>
                                            Close
                                        </Button>
                                    </div>
                                </div>
                            )}
                        />
                    )}
                </div>
            </Column>
        </Grid>
    );
};

export { SelectView };
