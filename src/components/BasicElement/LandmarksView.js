import React from 'react';
import { Grid, Column } from '@carbon/react';
import { generateURL } from '../../components/Info';

class LandmarksView extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  componentDidUpdate(prevProps, prevState) {}

  render() {
    return (
      <Grid>
        <Column lg={16} md={8} sm={4}>
          <img
            alt="design"
            src={generateURL('shared', 'landmark-view', 'png')}
            width="50%"
          />
        </Column>
      </Grid>
    );
  }
}

export { LandmarksView };
