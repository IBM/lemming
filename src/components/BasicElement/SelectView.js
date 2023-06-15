import React from 'react';
import { generateDescription } from '../../components/Info';
import { GraphCanvas, lightTheme } from 'reagraph';
import { Grid, Column, Button } from '@carbon/react';

function generateNodes(state) {
  if (!state.graph || !state.graph.nodes) return [];
  return state.graph.nodes.map((item, id) => {
    return { ...item, label: '', description: item.label };
  });
}

function generateEdges(state) {
  if (!state.graph || !state.graph.links) return [];

  const edges = state.graph.links.map((item, id) => {
    return {
      ...item,
      id: id,
      size: 2,
    };
  });

  return edges;
}

const SelectView = props => {
  const nodes = generateNodes(props.state);
  const edges = generateEdges(props.state);
  const actives = props.state.choice_infos.map(
    item => item.node_with_multiple_out_edges
  );

  const onEdgeClick = edge => {
    props.onEdgeClick(edge);
  };

  const onNodeClick = node => {
    props.onNodeClick(node);
  };

  return (
    <Grid>
      <Column lg={16} md={8} sm={4}>
        <div className="canvas-holder">
          <GraphCanvas
            theme={{ ...lightTheme, canvas: { background: 'white' } }}
            labelType="edges"
            edgeLabelPosition="inline"
            layoutType="hierarchicalTd"
            nodes={nodes}
            edges={edges}
            actives={actives}
            onNodeClick={node => onNodeClick(node)}
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
                <div style={{ position: 'absolute', bottom: 10, left: 10 }}>
                  <Button size="sm" kind="tertiary" onClick={onClose}>
                    Close
                  </Button>
                </div>
              </div>
            )}
          />
        </div>
      </Column>
    </Grid>
  );
};

export { SelectView };
