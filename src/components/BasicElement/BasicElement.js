import React from 'react';
import { BuildForward } from './BuildForward';
import { BuildBackward } from './BuildBackward';
import { LandmarksView } from './LandmarksView';
import { SelectView } from './SelectView';
import {
  Grid,
  Column,
  Switch,
  ContentSwitcher,
  Button,
  ToastNotification,
} from '@carbon/react';

const components = {
  BuildForward: BuildForward,
  BuildBackward: BuildBackward,
  LandmarksView: LandmarksView,
  SelectView: SelectView,
};

class PlanArea extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      views: props.props.views,
      active_view: props.props.default_view,
    };
  }

  componentDidUpdate(prevProps, prevState) {}

  logViewChange = e => {
    this.setState({
      active_view: e.name,
    });
  };

  render() {
    return (
      <Grid>
        <Column lg={6} md={6} sm={4}>
          <ContentSwitcher
            onChange={e => this.logViewChange(e)}
            size="sm"
            selectedIndex={this.state.views
              .map(e => e.name)
              .indexOf(this.state.active_view)}>
            {this.state.views.map((view, id) => (
              <Switch key={id} name={view.name} text={view.name} />
            ))}
          </ContentSwitcher>
          <br />
        </Column>

        <Column lg={12} md={8} sm={4}>
          <Button kind="primary" size="sm">
            Start
          </Button>

          {this.state.views.map((view, id) => {
            if (this.state.active_view === view.name) {
              const Component = components[view.name.replace(/\s/g, '')];

              if (view.disabled) {
                return (
                  <ToastNotification
                    lowContrast
                    hideCloseButton
                    key={id}
                    type="error"
                    subtitle={
                      <span>
                        The authors have disabled the {view.name}. Please check
                        out the other viewing options for now.
                      </span>
                    }
                    title="DISABLED"
                  />
                );
              } else {
                return <Component key={id} props={this.state} />;
              }
            }

            return null;
          })}
        </Column>
      </Grid>
    );
  }
}

class FeedbackArea extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  componentDidUpdate(prevProps, prevState) {}

  render() {
    return (
      <Grid>
        <Column lg={4} md={4} sm={4}></Column>
      </Grid>
    );
  }
}

export { PlanArea, FeedbackArea };
