import React from 'react';
import { SelectView } from './SelectView';
import { stringSimilarity } from 'string-similarity-js';
import Autosuggest from 'react-autosuggest';
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
    ContainedListItem,
} from '@carbon/react';

const config = require('../../config.json');
const link_to_server = config.link_to_server;

const default_state = {
    text_input: '',
    ltl_formulas: [],
    suggestions: [],
  selected_formula: 0,
};

const getCachedSuggestions = nl_prompts => {
  return nl_prompts
    .map(item => item.paraphrases.concat([item.utterance]))
    .reduce((options, item) => options.concat(item), []);
};

const getInitState = state => {
  return {
    ...default_state,
    ...state,
    domain_name: state.domain_name,
    domain: state.domain,
    problem: state.problem,
    plans: state.plans,
    cached_suggestions: getCachedSuggestions(state.nl_prompts),
    suggestions: [],
  };
};

class NL2LTLIntegration extends React.Component {
  constructor(props) {
    super(props);
    this.state = getInitState(props.state);
  }

    handleKeyDown(e) {
        if (e.key === 'Enter') {
            fetch(link_to_server + '/nl2ltl', {
                method: 'POST',
                body: JSON.stringify({
          domain_name: this.state.domain_name,
          utterance: this.state.text_input,
        }),
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

    update_planner_payload(planner_payload, new_formula) {
        this.props.update_planner_payload(planner_payload, new_formula);
    }

    onEdgeClick(edge) {}

    confirmFormula() {
        const new_formula = this.state.ltl_formulas[
            this.state.selected_formula
        ];
        var cached_formulas = this.state.cached_formulas;
        cached_formulas.push(new_formula);

        fetch(link_to_server + '/ltl_compile', {
            method: 'POST',
            body: JSON.stringify({
                domain: this.state.domain,
                problem: this.state.problem,
                plans: this.state.plans,
                formulas: cached_formulas,
            }),
            headers: { 'Content-Type': 'application/json' },
        })
            .then(res => res.json())
            .then(data => {
                this.setState(
                    {
                        ...this.state,
                        ...default_state,
                    },
                    () => this.update_planner_payload(data, new_formula)
                );
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

    onSuggestionsFetchRequested = ({ value }) => {
        this.setState({
            suggestions: this.getSuggestions(value),
        });
    };

    onSuggestionsClearRequested = () => {
        this.setState({
            suggestions: [],
        });
    };

    onChange(event, { newValue }) {
        this.setState({
            ...this.state,
            text_input: newValue.toString(),
        });
    }

    getSuggestions(value) {
        const inputValue = value.trim().toLowerCase();
        var matched_objects = this.state.cached_suggestions.map(item => {
            return {
                value: item,
                match: stringSimilarity(item.toLowerCase(), inputValue),
            };
        });

        matched_objects.sort((a, b) => b.match - a.match);
        matched_objects = matched_objects.slice(0, 10);

        return inputValue.length === 0
            ? this.state.cached_suggestions
            : matched_objects.map(item => item.value);
    }

    getSuggestionValue = suggestion => suggestion;

    renderSuggestion = suggestion => (
        <ContainedListItem className="suggested-option">
            {suggestion}
        </ContainedListItem>
    );

    renderInputComponent = inputProps => (
        <TextInput
            {...inputProps}
            id="nl2ltl"
            invalidText="A valid value is required."
            labelText={
                <span>
                    Constrain the set of plans by describing LTL control rules
                    in natural language. Learn more about NL2LTL{' '}
                    <a
                        href="https://github.com/IBM/nl2ltl"
                        target="_blank"
                        rel="noreferrer">
                        here
                    </a>
                    .
                </span>
            }
            placeholder="Write your control rule in English"
            onKeyDown={this.handleKeyDown.bind(this)}
        />
    );

    render() {
        const inputProps = {
            value: this.state.text_input,
            onChange: this.onChange.bind(this),
        };

        return (
            <Grid>
                <Column lg={16} md={8} sm={4}>
                    <div style={{ marginTop: '20px' }}>
                        <Autosuggest
                            suggestions={this.state.suggestions}
                            onSuggestionsFetchRequested={this.onSuggestionsFetchRequested.bind(
                                this
                            )}
                            onSuggestionsClearRequested={this.onSuggestionsClearRequested.bind(
                                this
                            )}
                            getSuggestionValue={this.getSuggestionValue.bind(
                                this
                            )}
                            inputProps={inputProps}
                            renderInputComponent={this.renderInputComponent.bind(
                                this
                            )}
                            renderSuggestion={this.renderSuggestion.bind(this)}
                        />

                        <SelectView
                            state={this.state}
                            onEdgeClick={this.onEdgeClick.bind(this)}
                            no_feedback={true}
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
                        <StructuredListWrapper
                            selection
                            ariaLabel="Translated Formulas">
                            <StructuredListHead>
                                <StructuredListRow head>
                                    <StructuredListCell head>
                                        Formula
                                    </StructuredListCell>
                                </StructuredListRow>
                            </StructuredListHead>
                            <StructuredListBody>
                                {this.state.ltl_formulas.map((item, i) => (
                                    <StructuredListRow key={`row-${i}`}>
                                        <StructuredListCell
                                            onClick={this.selectFormula.bind(
                                                this,
                                                i
                                            )}>
                                            <strong>{item.formula}</strong>
                                            <div style={{ marginTop: '10px' }}>
                                                <em>Description:</em>{' '}
                                                {item.description}
                                            </div>
                                            <div style={{ marginTop: '10px' }}>
                                                <em>Confidence:</em>{' '}
                                                {item.confidence}
                                            </div>
                                        </StructuredListCell>
                                        <StructuredListCell>
                                            <br />
                                            <RadioButton
                                                checked={
                                                    i ===
                                                    this.state.selected_formula
                                                }
                                                onClick={this.selectFormula.bind(
                                                    this,
                                                    i
                                                )}
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
