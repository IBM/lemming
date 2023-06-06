import React from 'react';
import {
  Grid,
  Column,
  TextInput,
  Modal,
  StructuredListWrapper,
  StructuredListHead,
  StructuredListBody,
  StructuredListRow,
  StructuredListCell,
  RadioButton,
} from '@carbon/react';

const config = require('../../config.json');
const link_to_server = config.link_to_server;

const default_state = {
  text_input: '',
  ltl_formulas: [],
  selected_formula: 0,
};

class NL2LTLIntegration extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      ...default_state,
      domain: props.state.domain,
      problem: props.state.problem,
      plans: props.state.plans,
    };
  }

  componentDidUpdate(prevProps, prevState) {}

  onChange(e) {
    this.setState({
      ...this.state,
      text_input: e.target.value,
    });
  }

  handleKeyDown(e) {
    if (e.key === 'Enter') {
      fetch(link_to_server + '/nl2ltl', {
        method: 'POST',
        body: JSON.stringify({ utterance: this.state.text_input }),
        headers: { 'Content-Type': 'application/json' },
      })
        .then(res => res.json())
        .then(data => {
          this.setState({
            ...this.state,
            ltl_formulas: data,
          });
        })
        .catch(err => console.error(err));
    }
  }

  update_planner_payload(planner_payload) {
    this.props.update_planner_payload(planner_payload);
  }

  confirmFormula() {
    fetch(link_to_server + '/ltl_compile', {
      method: 'POST',
      body: JSON.stringify({
        formula: this.state.ltl_formulas[this.state.selected_formula],
        domain: this.state.domain,
        problem: this.state.problem,
        plans: this.state.plans,
      }),
      headers: { 'Content-Type': 'application/json' },
    })
      .then(res => res.json())
      .then(data => {
        this.update_planner_payload(data);

        this.setState({
          ...this.state,
          ...default_state,
        });
      })
      .catch(err => console.error(err));
  }

  onRequestClose() {
    this.setState({
      ...this.state,
      ...default_state,
    });
  }

  selectFormula(itemIndex) {
    this.setState({
      ...this.state,
      selected_formula: itemIndex,
    });
  }

  render() {
    return (
      <Grid>
        <Column lg={16} md={8} sm={4}>
          <div style={{ marginTop: '10px' }}>
            <TextInput
              helperText={
                <span>
                  Learn more about NL2LTL{' '}
                  <a
                    href="https://github.com/IBM/nl2ltl"
                    target="_blank"
                    rel="noreferrer">
                    here
                  </a>
                  .
                </span>
              }
              id="nl2ltl"
              invalidText="A valid value is required."
              labelText="Constrain the set of plans using LTL described in natural language."
              placeholder="Write your control rule in English"
              onKeyDown={this.handleKeyDown.bind(this)}
              onChange={this.onChange.bind(this)}
              value={this.state.text_input}
            />
          </div>

          <Modal
            preventCloseOnClickOutside
            onRequestSubmit={this.confirmFormula.bind(this)}
            onRequestClose={this.onRequestClose.bind(this)}
            open={this.state.ltl_formulas.length > 0}
            modalHeading="Translated Formula"
            modalLabel="Confirmation"
            primaryButtonText="Submit"
            secondaryButtonText="Cancel"
            size="sm">
            <StructuredListWrapper selection ariaLabel="Translated Formulas">
              <StructuredListHead>
                <StructuredListRow head>
                  <StructuredListCell head>Formula</StructuredListCell>
                </StructuredListRow>
              </StructuredListHead>
              <StructuredListBody>
                {this.state.ltl_formulas.map((item, i) => (
                  <StructuredListRow key={`row-${i}`}>
                    <StructuredListCell
                      onClick={this.selectFormula.bind(this, i)}>
                      <strong>{item.formula}</strong>
                      <div style={{ marginTop: '10px' }}>
                        <em>Description:</em> {item.description}
                      </div>
                      <div style={{ marginTop: '10px' }}>
                        <em>Confidence:</em> {item.confidence}
                      </div>
                    </StructuredListCell>
                    <StructuredListCell>
                      <br />
                      <RadioButton
                        checked={i === this.state.selected_formula}
                        onClick={this.selectFormula.bind(this, i)}
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
          </Modal>
        </Column>
      </Grid>
    );
  }
}

export { NL2LTLIntegration };
