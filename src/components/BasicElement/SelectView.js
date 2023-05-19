import { React, useRef } from 'react';
import { GraphCanvas, lightTheme, useSelection } from 'reagraph';
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
  const graphRef = useRef(null);

  const onEdgeClick = edge => {
    props.onEdgeClick(edge);
  };

  const { actives, onNodeClick, onCanvasClick } = useSelection({
    ref: graphRef,
    nodes: nodes,
    edges: edges,
    type: 'multi',
    actives: [],
    pathSelectionType: 'out',
    focusOnSelect: false,
    onEdgeClick: onEdgeClick,
  });

  return (
    <Grid>
      <Column lg={16} md={8} sm={4}>
        <div className="canvas-holder">
          <GraphCanvas
            ref={graphRef}
            theme={{ ...lightTheme, canvas: { background: '#f4f4f4' } }}
            labelType="edges"
            edgeLabelPosition="inline"
            layoutType="hierarchicalTd"
            nodes={nodes}
            edges={edges}
            actives={actives}
            onCanvasClick={onCanvasClick}
            onNodeClick={onNodeClick}
            onEdgeClick={edge => onEdgeClick(edge)}
            contextMenu={({ data, additional, onClose }) => (
              <div
                className="node-pop"
                style={{
                  background: 'white',
                  width: 250,
                  height: 250,
                  border: 'solid 1px #0d62fe',
                  borderRadius: 2,
                  padding: 10,
                  textAlign: 'left',
                }}>
                <div>{data.data.description}</div>
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
