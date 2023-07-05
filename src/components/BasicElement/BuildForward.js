import React, { useRef, useState } from 'react';
import {
    generateDescription,
    parseEdgeName,
    generateNodes,
    generateEdges,
    getActiveNodes,
    getBasisNodes,
    rawNodeTransform,
} from '../../components/Info';
import { GraphCanvas } from 'reagraph';
import { Grid, Column, Button, Tile } from '@carbon/react';

const init_feedback =
    "Build a plan backward from the goal. Right click on the nodes and edges to find what's in them. Click on an edge to enforce all plans with that action.";

const BuildForward = props => {
    const nodes = generateNodes(props.state);
    const edges = generateEdges(props.state);
    const actives = getActiveNodes(props.state);

    const ref = useRef(null);
    const [feedback_text, setFeedbackText] = useState(init_feedback);

    const onEdgeClick = edge => {
        const label = parseEdgeName(edge.label);
        props.onEdgeClick(label);
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
                    </div>
                )}

                <div className="canvas-holder">
                    {nodes.length > 0 && (
                        <GraphCanvas
                            ref={ref}
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

export { BuildForward };
