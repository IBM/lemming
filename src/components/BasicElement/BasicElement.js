import React from 'react';
import { BuildForward } from './BuildForward';
import { BuildBackward } from './BuildBackward';
import { LandmarksView } from './LandmarksView';
import { SelectView } from './SelectView';
import { IMPORT_OPTIONS } from './data/ImportOptions';
import {
  Grid,
  Column,
  Switch,
  ContentSwitcher,
  Button,
  ToastNotification,
  Modal,
  TabPanels,
  TabPanel,
  TabList,
  Tabs,
  Tab,
  StructuredListWrapper,
  StructuredListHead,
  StructuredListBody,
  StructuredListRow,
  StructuredListCell,
  InlineNotification,
  Link,
  Tile,
  RadioButton,
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
      domain: null,
      problem: null,
      plans: null,
      views: props.props.views,
      active_view: props.props.default_view,
      controls: {
        selected_domain: null,
        modal_open: false,
        upload_tab: 0,
      },
      notifications: {
        import_select: false,
        pddl_upload: false,
        plan_upload: false,
      },
    };
  }

  componentDidUpdate(prevProps, prevState) {}

  uploadFiles() {
    if (this.state.controls.upload_tab === 0) {
      if (!this.state.domain || !this.state.domain) {
        this.setState({
          ...this.state,
          notifications: {
            ...this.state.notifications,
            pddl_upload: true,
          },
        });
      } else {
        this.setState({
          ...this.state,
          controls: {
            ...this.state.controls,
            modal_open: false,
          },
        });
      }
    }

    if (this.state.controls.upload_tab === 1) {
      if (this.state.controls.selected_domain == null) {
        this.setState({
          ...this.state,
          notifications: {
            ...this.state.notifications,
            import_select: true,
          },
        });
      } else {
        this.setState({
          ...this.state,
          controls: {
            ...this.state.controls,
            modal_open: false,
          },
        });
      }
    }
  }

  logViewChange(e) {
    this.setState({
      active_view: e.name,
    });
  }

  changeTab(tabIndex) {
    this.setState({
      ...this.state,
      domain: null,
      problem: null,
      plans: null,
      controls: {
        ...this.state.controls,
        selected_domain: null,
        upload_tab: tabIndex,
      },
      notifications: {
        ...this.state.notifications,
        import_select: false,
        pddl_upload: false,
      },
    });
  }

  selectImport(itemIndex) {
    this.setState(
      {
        ...this.state,
        controls: {
          ...this.state.controls,
          selected_domain: itemIndex,
        },
      },
      console.log(this.state.controls.selected_domain)
    );
  }

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
          <Button
            kind="primary"
            size="sm"
            onClick={() => {
              this.setState({
                ...this.state,
                controls: { ...this.state.controls, modal_open: true },
              });
            }}>
            Start
          </Button>

          <Button style={{ marginLeft: '10px' }} kind="danger" size="sm">
            Plan
          </Button>

          <Modal
            passiveModal
            open={this.state.notifications.plan_upload}
            onRequestClose={() => {
              this.setState({
                ...this.state,
                notifications: {
                  ...this.state.notifications,
                  plan_upload: false,
                },
              });
            }}
            modalHeading="You can ask Lemming to generate the plans for you. Inshallah the domain and problem files are error free."
            modalLabel={
              <span className="text-danger">Could not parse plan file!</span>
            }
            size="xs"></Modal>

          <Modal
            preventCloseOnClickOutside
            onRequestClose={() => {
              this.setState({
                ...this.state,
                controls: { ...this.state.controls, modal_open: false },
              });
            }}
            onRequestSubmit={this.uploadFiles.bind(this)}
            open={this.state.controls.modal_open}
            modalHeading="Planning Task"
            modalLabel="Getting Started"
            primaryButtonText="Upload"
            size="sm">
            <Tabs selectedIndex={this.state.controls.upload_tab}>
              <TabList
                aria-label="List of tabs"
                contained
                activation="automatic">
                <Tab onClick={this.changeTab.bind(this, 0)}>Upload</Tab>
                <Tab onClick={this.changeTab.bind(this, 1)}>Import</Tab>
              </TabList>
              <TabPanels>
                <TabPanel>
                  <div>
                    Start by uploading a PDDL domain and problem file, and
                    optionally, a set of plans. Alternatively, you can request
                    Lemming to compute a set of plans.
                  </div>
                  <br />

                  <StructuredListWrapper ariaLabel="Structured list">
                    <StructuredListBody>
                      <StructuredListRow>
                        <StructuredListCell>Domain</StructuredListCell>
                        <StructuredListCell>
                          <input type="file" onChange={this.onFileChange} />
                        </StructuredListCell>
                      </StructuredListRow>
                      <StructuredListRow>
                        <StructuredListCell>Problem</StructuredListCell>
                        <StructuredListCell>
                          <input type="file" onChange={this.onFileChange} />
                        </StructuredListCell>
                      </StructuredListRow>
                      <StructuredListRow>
                        <StructuredListCell>Plans</StructuredListCell>
                        <StructuredListCell>
                          <input type="file" onChange={this.onFileChange} />
                        </StructuredListCell>
                      </StructuredListRow>
                    </StructuredListBody>
                  </StructuredListWrapper>

                  {this.state.notifications.pddl_upload && (
                    <InlineNotification
                      hideCloseButton
                      iconDescription="Close"
                      subtitle={
                        <span>
                          Both domain and problem files must be provided.
                        </span>
                      }
                      timeout={0}
                      title="MISSING FILES"
                      kind="error"
                      lowContrast
                    />
                  )}

                  <br />
                  <div>
                    You can also import from a set of illustrative examples{' '}
                    <Link
                      style={{ cursor: 'pointer' }}
                      onClick={this.changeTab.bind(this, 1)}>
                      here
                    </Link>
                    .
                  </div>
                </TabPanel>
                <TabPanel>
                  <StructuredListWrapper
                    selection
                    ariaLabel="Illustrative Domains">
                    <StructuredListHead>
                      <StructuredListRow head>
                        <StructuredListCell head>Domain</StructuredListCell>
                        <StructuredListCell head>
                          Description
                        </StructuredListCell>
                      </StructuredListRow>
                    </StructuredListHead>
                    <StructuredListBody>
                      {IMPORT_OPTIONS.map((item, i) => (
                        <StructuredListRow key={`row-${i}`}>
                          <StructuredListCell
                            onClick={this.selectImport.bind(this, i)}>
                            {item.name}
                          </StructuredListCell>
                          <StructuredListCell
                            onClick={this.selectImport.bind(this, i)}>
                            {item.description}
                          </StructuredListCell>
                          <StructuredListCell>
                            <br />
                            <RadioButton
                              checked={
                                i === this.state.controls.selected_domain
                              }
                              onClick={this.selectImport.bind(this, i)}
                              id={`row-${i}`}
                              title={`row-${i}`}
                              value={`row-${i}`}
                              name={item.name}
                              labelText={``}
                            />
                          </StructuredListCell>
                        </StructuredListRow>
                      ))}
                    </StructuredListBody>
                  </StructuredListWrapper>
                  {this.state.notifications.import_select && (
                    <InlineNotification
                      hideCloseButton
                      iconDescription="Close"
                      subtitle={<span>Please select a domain.</span>}
                      timeout={0}
                      title="NO SELECTION"
                      kind="error"
                      lowContrast
                    />
                  )}
                </TabPanel>
              </TabPanels>
            </Tabs>
          </Modal>

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
    this.state = {
      feedback: 'Welcome to Lemming! Get started by loading a planning task.',
      selected_landmarks: ['aaaa', 'bbbbb', 'cccccc'],
      unselected_landmarks: ['xxxxxx', 'yyyyyyyyyy', 'zzzz'],
    };
  }

  componentDidUpdate(prevProps, prevState) {}

  selectLandmark(landmark) {
    var selected_landmarks = this.state.selected_landmarks;
    var unselected_landmarks = this.state.unselected_landmarks;

    const index = unselected_landmarks.indexOf(landmark);
    unselected_landmarks.splice(index, 1);

    selected_landmarks.push(landmark);

    this.setState({
      ...this.state,
      selected_landmarks: selected_landmarks,
      unselected_landmarks: unselected_landmarks,
    });
  }

  deselectLandmark(landmark) {
    var selected_landmarks = this.state.selected_landmarks;
    var unselected_landmarks = this.state.unselected_landmarks;

    const index = selected_landmarks.indexOf(landmark);
    selected_landmarks.splice(index, 1);

    unselected_landmarks.push(landmark);

    this.setState({
      ...this.state,
      selected_landmarks: selected_landmarks,
      unselected_landmarks: unselected_landmarks,
    });
  }

  render() {
    return (
      <Grid>
        <Column lg={4} md={4} sm={4}>
          <Tile>{this.state.feedback}</Tile>

          <StructuredListWrapper ariaLabel="Selected Landmarks">
            <StructuredListHead>
              <StructuredListRow head>
                <StructuredListCell head>Selected Landmarks</StructuredListCell>
              </StructuredListRow>
            </StructuredListHead>
            <StructuredListBody className="landmarks-list">
              {this.state.selected_landmarks.map((item, i) => (
                <StructuredListRow key={item}>
                  <StructuredListCell
                    className="text-blue landmark-list-item"
                    onClick={this.deselectLandmark.bind(this, item)}>
                    {item}
                  </StructuredListCell>
                </StructuredListRow>
              ))}
              {this.state.unselected_landmarks.map((item, i) => (
                <StructuredListRow key={item}>
                  <StructuredListCell
                    className="text-secondary landmark-list-item"
                    onClick={this.selectLandmark.bind(this, item)}>
                    {item}
                  </StructuredListCell>
                </StructuredListRow>
              ))}
            </StructuredListBody>
          </StructuredListWrapper>
        </Column>
      </Grid>
    );
  }
}

export { PlanArea, FeedbackArea };
