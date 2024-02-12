import React from 'react';
import { BuildForward } from './BuildForward';
import { BuildBackward } from './BuildBackward';
import { SelectView } from './SelectView';
import { NL2LTLIntegration } from './NL2LTLIntegration';
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
    Toggle,
    StructuredListWrapper,
    StructuredListHead,
    StructuredListBody,
    StructuredListRow,
    StructuredListCell,
    InlineNotification,
    Link,
    Tile,
    RadioButton,
    Loading,
    NumberInput,
    Tag,
} from '@carbon/react';

const config = require('../../config.json');
const link_to_server = config.link_to_server;

const components = {
    BuildForward: BuildForward,
    BuildBackward: BuildBackward,
    SelectView: SelectView,
    NL2LTLIntegration: NL2LTLIntegration,
};

function getPlanHashesFromChoice(action_name, plans) {
    return plans
        .filter(plan => plan.actions.indexOf(action_name) > -1)
        .map(item => item.plan_hash);
}

function getDomainName(domain_string) {
    const reg = /.*\(domain (.*)\).*/g;
    const reg_exec = reg.exec(domain_string);

    if (reg_exec !== null && reg_exec.length > 1) return reg_exec[1];
}

class PlanArea extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            views: config.views,
            active_view: config.default_view,
            selectedFile: null,
            selectedFileType: null,
            domain_name: null,
            domain: null,
            problem: null,
            plans: [],
            nl_prompts: [],
            cached_formulas: [],
            graph: null,
            feedback:
                'Welcome to Lemming! Get started by loading a planning task.',
            cached_landmarks: [],
            remaining_plans: [],
            selected_landmarks: new Set(),
            unselected_landmarks: new Set(),
            choice_infos: [],
            controls: {
                selected_domain: null,
                modal_open: false,
                upload_tab: 0,
                num_plans: 10,
                quality_bound: 1.2,
                select_by_name: true,
            },
            notifications: {
                import_select: false,
                pddl_upload: false,
                no_plans_error: false,
                viz_loading: false,
            },
            turn: 0,
        };
    }

    onFileChange(file_type, e) {
        this.setState(
            {
                ...this.state,
                selectedFile: e.target.files[0],
                selectedFileType: file_type,
            },
            () => {
                if (!this.state.selectedFile) return;

                const data = new FormData();
                data.append('file', this.state.selectedFile);

                fetch(link_to_server + '/file_upload', {
                    method: 'POST',
                    body: data,
                })
                    .then(res => res.json())
                    .then(data => {
                        if (this.state.selectedFileType === 'plans') {
                            data = JSON.parse(data);

                            this.setState({
                                ...this.state,
                                remaining_plans: data,
                                plans: data,
                            });
                        } else {
                            this.setState({
                                ...this.state,
                                [this.state.selectedFileType]: data,
                                plans: [],
                            });
                        }
                    })
                    .catch(err => console.error(err));
            }
        );
    }

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
                this.setState(
                    {
                        ...this.state,
                        turn: 0,
                        graph: null,
                        cached_landmarks: [],
                        selected_landmarks: [],
                        unselected_landmarks: [],
                        choice_infos: [],
                        controls: {
                            ...this.state.controls,
                            modal_open: false,
                        },
                    },
                    () => {
                        this.getLandmarks();
                    }
                );
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
                fetch(
                    link_to_server +
                        '/import_domain/' +
                        IMPORT_OPTIONS[this.state.controls.selected_domain]
                            .name,
                    {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                    }
                )
                    .then(res => res.json())
                    .then(data => {
                        const planning_task = data['planning_task'];
                        this.setState(
                            {
                                ...this.state,
                                turn: 0,
                                domain_name:
                                    IMPORT_OPTIONS[
                                        this.state.controls.selected_domain
                                    ].name,
                                domain: planning_task['domain'],
                                problem: planning_task['problem'],
                                remaining_plans: data['plans'],
                                plans: data['plans'],
                                nl_prompts: data['nl_prompts'],
                                graph: null,
                                cached_landmarks: [],
                                selected_landmarks: [],
                                unselected_landmarks: [],
                                choice_infos: [],
                                controls: {
                                    ...this.state.controls,
                                    modal_open: false,
                                },
                            },
                            () => {
                                this.getLandmarks();
                            }
                        );
                    })
                    .catch(err => console.error(err));
            }
        }
    }

    logViewChange(e) {
        this.props.changeView(e);
        this.setState({ active_view: e.name }, () => {
            this.generateViz();
        });
    }

    changeTab(tabIndex) {
        this.setState({
            ...this.state,
            domain: null,
            problem: null,
            plans: [],
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

    update_planner_payload(planner_payload, new_formula) {
        const planning_task = planner_payload['planning_task'];
        const plans = planner_payload['plans'];

        var cached_formulas = this.state.cached_formulas;

        if (cached_formulas.indexOf(new_formula) === -1)
            cached_formulas.push(new_formula);

        this.setState(
            {
                ...this.state,
                domain: planning_task.domain,
                problem: planning_task.problem,
                plans: plans,
                remaining_plans: plans,
                cached_formulas: cached_formulas,
            },
            () => {
                this.generateViz();
            }
        );
    }

    getPlans(e) {
        this.setState({
            ...this.state,
            plans: [],
            notifications: {
                ...this.state.notifications,
                viz_loading: true,
            },
        });

        const get_plans_endpoint = link_to_server + '/get_plans';
        const payload = {
            domain: this.state.domain,
            problem: this.state.problem,
            num_plans: this.state.controls.num_plans,
            quality_bound: this.state.controls.quality_bound,
        };

        fetch(get_plans_endpoint, {
            method: 'POST',
            body: JSON.stringify(payload),
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(res => res.json())
            .then(data => {
                this.setState(
                    {
                        ...this.state,
                        turn: 0,
                        remaining_plans: data.plans,
                        plans: data.plans,
                        selected_landmarks: [],
                        unselected_landmarks: [],
                        notifications: {
                            ...this.state.notifications,
                            viz_loading: false,
                        },
                    },
                    () => {
                        const feedback = this.generateFeedback();
                        this.setState({
                            ...this.state,
                            feedback: feedback,
                        });

                        this.generateViz();
                    }
                );
            })
            .catch(err => {
                console.error(err);

                this.setState({
                    ...this.state,
                    notifications: {
                        ...this.state.notifications,
                        no_plans_error: true,
                        viz_loading: false,
                    },
                });
            });
    }

    getLandmarks() {
        if (!this.state.domain || !this.state.problem) return;

        const feedback = this.generateFeedback();
        if (feedback)
            this.setState({
                ...this.state,
                feedback: feedback,
                notifications: {
                    ...this.state.notifications,
                    viz_loading: true,
                },
            });

        const landmarks_endpoint = link_to_server + '/get_landmarks/rhw';
        const payload = {
            domain: this.state.domain,
            problem: this.state.problem,
        };

        fetch(landmarks_endpoint, {
            method: 'POST',
            body: JSON.stringify(payload),
            headers: { 'Content-Type': 'application/json' },
        })
            .then(res => res.json())
            .then(data => {
                this.setState(
                    {
                        ...this.state,
                        cached_landmarks: data.landmarks,
                        notifications: {
                            ...this.state.notifications,
                            viz_loading: false,
                        },
                    },
                    () => {
                        this.generateViz();
                    }
                );
            })
            .catch(err => {
                console.error(err);
            });
    }

    generateViz() {
        if (!this.state.plans || this.state.plans.length === 0) return;

        const viz_endpoint =
            link_to_server +
            '/generate_' +
            this.state.active_view.toLowerCase().replace(/\s/g, '_');

        var cache_plans = this.state.plans;
        const selection_infos = this.state.selected_landmarks.map((item, i) => {
            const plan_hashes = getPlanHashesFromChoice(item, cache_plans);
            cache_plans = cache_plans.filter(
                item => plan_hashes.indexOf(item.plan_hash) > -1
            );

            return {
                selected_first_achiever: item,
                selected_plan_hashes: plan_hashes,
            };
        });

        var payload = {
            domain: this.state.domain,
            problem: this.state.problem,
            plans: this.state.plans,
            landmarks: this.state.cached_landmarks,
            selection_infos: selection_infos,
        };

        if (this.state.active_view === 'Select View') {
            payload.selection_priority = this.state.views.filter(
                item => item.name === 'Select View'
            )[0].selection_priority;
        } else {
            payload.selection_priority = null;
        }

        fetch(viz_endpoint, {
            method: 'POST',
            body: JSON.stringify(payload),
            headers: { 'Content-Type': 'application/json' },
        })
            .then(res => res.json())
            .then(data => {
                const unselected_landmarks =
                    this.state.turn > 0
                        ? this.state.unselected_landmarks
                        : data.choice_infos.reduce(
                              (choices, item) =>
                                  item.landmark
                                      ? choices.concat(
                                            item.landmark.first_achievers
                                        )
                                      : [],
                              []
                          );

                this.setState({
                    ...this.state,
                    remaining_plans: data.plans,
                    graph: data.networkx_graph,
                    choice_infos: data.choice_infos,
                    unselected_landmarks: unselected_landmarks,
                    notifications: {
                        ...this.state.notifications,
                        viz_loading: false,
                    },
                });
            })
            .catch(err => {
                console.error(err);
            });
    }

    selectImport(itemIndex) {
        this.setState({
            ...this.state,
            controls: {
                ...this.state.controls,
                selected_domain: itemIndex,
            },
        });
    }

    generateFeedback() {
        var feedback = '';

        if (this.state.domain) {
            const domain_name = getDomainName(this.state.domain);
            feedback += `Have fun with the ${domain_name} domain!`;
        }

        if (this.state.plans.length > 0) {
            const max_cost = this.state.plans.reduce(
                (max_cost, item) =>
                    item.cost > max_cost ? item.cost : max_cost,
                0
            );
            const min_cost = this.state.plans.reduce(
                (min_cost, item) =>
                    item.cost <= min_cost ? item.cost : min_cost,
                Infinity
            );
            const num_plans = this.state.plans.length;

            if (num_plans > 1)
                feedback += ` You have ${num_plans} plans to select from with minimum cost ${min_cost} and maximal cost ${max_cost}.`;
        }

        return feedback;
    }

    selectLandmarks(landmarks) {
        var selected_landmarks = this.state.selected_landmarks;
        var unselected_landmarks = this.state.unselected_landmarks;

        for (var i = 0; i < landmarks.length; i++) {
            if (selected_landmarks.indexOf(landmarks[i]) === -1)
                selected_landmarks.push(landmarks[i]);

            if (unselected_landmarks.indexOf(landmarks[i]) > -1)
                unselected_landmarks.splice(
                    unselected_landmarks.indexOf(landmarks[i]),
                    1
                );
        }

        this.setState(
            {
                ...this.state,
                selected_landmarks: selected_landmarks,
                unselected_landmarks: unselected_landmarks,
                turn: this.state.turn + 1,
            },
            () => {
                this.generateViz();
            }
        );
    }

    deselectLandmarks(landmarks) {
        var selected_landmarks = this.state.selected_landmarks;
        var unselected_landmarks = this.state.unselected_landmarks;

        for (var i = 0; i < landmarks.length; i++) {
            if (unselected_landmarks.indexOf(landmarks[i]) === -1)
                unselected_landmarks.push(landmarks[i]);

            if (selected_landmarks.indexOf(landmarks[i]) > -1)
                selected_landmarks.splice(
                    selected_landmarks.indexOf(landmarks[i]),
                    1
                );
        }

        this.setState(
            {
                ...this.state,
                selected_landmarks: selected_landmarks,
                unselected_landmarks: unselected_landmarks,
                turn: this.state.turn + 1,
            },
            () => {
                this.generateViz();
            }
        );
    }

    deleteUserPrompt(formula) {
        var cached_formulas = this.state.cached_formulas;
        const index = cached_formulas.indexOf(formula);

        if (index > -1) cached_formulas.splice(index, 1);

        this.setState(
            {
                ...this.state,
                cached_formulas: cached_formulas,
                turn: this.state.turn + 1,
            },
            () => {
                this.generateViz();
            }
        );
    }

    onNumPlansChange(e, any, value) {
        const num_plans = value || any.value;
        this.setState({
            ...this.state,
            controls: {
                ...this.state.controls,
                num_plans: num_plans,
            },
        });
    }

    onQualityBoundChange(e) {
        this.setState({
            ...this.state,
            controls: {
                ...this.state.controls,
                quality_bound: e.target.value,
            },
        });
    }

    onEdgeClick(edge) {
        this.selectLandmarks([edge]);
    }

    commitChanges(commits) {
        this.selectLandmarks(Array.from(commits));
    }

    setSelectionMode(e) {
        this.setState({
            ...this.state,
            controls: {
                ...this.state.controls,
                select_by_name: !this.state.controls.select_by_name,
            },
        });
    }

    render() {
        return (
            <Grid>
                <Column lg={12} md={6} sm={4}>
                    <ContentSwitcher
                        onChange={e => this.logViewChange(e)}
                        size="sm"
                        selectedIndex={this.state.views
                            .map(e => e.name)
                            .indexOf(this.state.active_view)}>
                        {this.state.views.map((view, id) => (
                            <Switch
                                key={id}
                                name={view.name}
                                text={view.name}
                            />
                        ))}
                    </ContentSwitcher>
                    <br />

                    <Grid>
                        <Column lg={12} md={8} sm={4}>
                            <Button
                                kind="primary"
                                size="sm"
                                onClick={() => {
                                    this.setState({
                                        ...this.state,
                                        controls: {
                                            ...this.state.controls,
                                            modal_open: true,
                                        },
                                    });
                                }}>
                                Start
                            </Button>

                            {this.state.domain && this.state.problem && (
                                <>
                                    <Button
                                        style={{ marginLeft: '10px' }}
                                        kind="danger"
                                        size="sm"
                                        onClick={this.getPlans.bind(this)}>
                                        Plan
                                    </Button>

                                    <div className="number-input">
                                        <NumberInput
                                            size="sm"
                                            hideLabel
                                            helperText="Number of plans"
                                            iconDescription="Number of plans"
                                            id="num_plans"
                                            invalidText="NaN / Too high."
                                            label=""
                                            max={50}
                                            min={1}
                                            step={1}
                                            value={
                                                this.state.controls.num_plans
                                            }
                                            onChange={this.onNumPlansChange.bind(
                                                this
                                            )}
                                        />
                                    </div>

                                    <div className="number-input">
                                        <NumberInput
                                            hideLabel
                                            hideSteppers
                                            size="sm"
                                            helperText="Quality Bound"
                                            iconDescription="Quality Bound"
                                            id="quality_bound"
                                            invalidText="Invalid input."
                                            label=""
                                            min={1}
                                            value={
                                                this.state.controls
                                                    .quality_bound
                                            }
                                            onChange={this.onQualityBoundChange.bind(
                                                this
                                            )}
                                        />
                                    </div>
                                </>
                            )}

                            {this.state.plans.length > 0 && (
                                <Button
                                    style={{ marginLeft: '10px' }}
                                    kind="tertiary"
                                    size="sm"
                                    href={`data:text/json;charset=utf-8,${encodeURIComponent(
                                        JSON.stringify(
                                            this.state.remaining_plans,
                                            0,
                                            4
                                        )
                                    )}`}
                                    download={'plans.json'}>
                                    Export
                                </Button>
                            )}

                            <Modal
                                passiveModal
                                open={this.state.notifications.no_plans_error}
                                onRequestClose={() => {
                                    this.setState({
                                        ...this.state,
                                        notifications: {
                                            ...this.state.notifications,
                                            no_plans_error: false,
                                        },
                                    });
                                }}
                                modalHeading="Try again with different files and inshallah it works out."
                                modalLabel={
                                    <span className="text-danger">
                                        Failed to generate plans!
                                    </span>
                                }
                                size="xs"></Modal>

                            <Modal
                                preventCloseOnClickOutside
                                onRequestClose={() => {
                                    this.setState({
                                        ...this.state,
                                        controls: {
                                            ...this.state.controls,
                                            modal_open: false,
                                        },
                                    });
                                }}
                                onRequestSubmit={this.uploadFiles.bind(this)}
                                open={this.state.controls.modal_open}
                                modalHeading="Planning Task"
                                modalLabel="Getting Started"
                                primaryButtonText="Upload"
                                size="sm">
                                <Tabs
                                    selectedIndex={
                                        this.state.controls.upload_tab
                                    }>
                                    <TabList
                                        aria-label="List of tabs"
                                        contained
                                        activation="automatic">
                                        <Tab
                                            onClick={this.changeTab.bind(
                                                this,
                                                0
                                            )}>
                                            Upload
                                        </Tab>
                                        <Tab
                                            onClick={this.changeTab.bind(
                                                this,
                                                1
                                            )}>
                                            Import
                                        </Tab>
                                    </TabList>
                                    <TabPanels>
                                        <TabPanel>
                                            <div>
                                                Start by uploading a PDDL domain
                                                and problem file, and
                                                optionally, a set of plans.
                                                Alternatively, you can request
                                                Lemming to compute a set of
                                                plans.
                                            </div>
                                            <br />

                                            <StructuredListWrapper ariaLabel="Structured list">
                                                <StructuredListBody>
                                                    <StructuredListRow>
                                                        <StructuredListCell>
                                                            Domain
                                                        </StructuredListCell>
                                                        <StructuredListCell>
                                                            <input
                                                                type="file"
                                                                onChange={this.onFileChange.bind(
                                                                    this,
                                                                    'domain'
                                                                )}
                                                            />
                                                        </StructuredListCell>
                                                    </StructuredListRow>
                                                    <StructuredListRow>
                                                        <StructuredListCell>
                                                            Problem
                                                        </StructuredListCell>
                                                        <StructuredListCell>
                                                            <input
                                                                type="file"
                                                                onChange={this.onFileChange.bind(
                                                                    this,
                                                                    'problem'
                                                                )}
                                                            />
                                                        </StructuredListCell>
                                                    </StructuredListRow>
                                                    <StructuredListRow>
                                                        <StructuredListCell>
                                                            Plans
                                                        </StructuredListCell>
                                                        <StructuredListCell>
                                                            <input
                                                                type="file"
                                                                onChange={this.onFileChange.bind(
                                                                    this,
                                                                    'plans'
                                                                )}
                                                            />
                                                        </StructuredListCell>
                                                    </StructuredListRow>
                                                </StructuredListBody>
                                            </StructuredListWrapper>

                                            {this.state.notifications
                                                .pddl_upload && (
                                                <InlineNotification
                                                    hideCloseButton
                                                    iconDescription="Close"
                                                    subtitle="Both domain and problem files must be provided."
                                                    timeout={0}
                                                    title="MISSING FILES"
                                                    kind="error"
                                                    lowContrast
                                                />
                                            )}

                                            <br />
                                            <div>
                                                You can also import from a set
                                                of illustrative examples{' '}
                                                <Link
                                                    style={{
                                                        cursor: 'pointer',
                                                    }}
                                                    onClick={this.changeTab.bind(
                                                        this,
                                                        1
                                                    )}>
                                                    here
                                                </Link>
                                                .
                                            </div>
                                        </TabPanel>
                                        <TabPanel>
                                            {this.state.notifications
                                                .import_select && (
                                                <InlineNotification
                                                    hideCloseButton
                                                    iconDescription="Close"
                                                    subtitle="Please select a domain"
                                                    timeout={0}
                                                    title="NO SELECTION"
                                                    kind="error"
                                                    lowContrast
                                                />
                                            )}
                                            <StructuredListWrapper
                                                selection
                                                ariaLabel="Illustrative Domains">
                                                <StructuredListHead>
                                                    <StructuredListRow head>
                                                        <StructuredListCell
                                                            head>
                                                            Domain
                                                        </StructuredListCell>
                                                        <StructuredListCell
                                                            head>
                                                            Description
                                                        </StructuredListCell>
                                                    </StructuredListRow>
                                                </StructuredListHead>
                                                <StructuredListBody>
                                                    {IMPORT_OPTIONS.map(
                                                        (item, i) => (
                                                            <StructuredListRow
                                                                key={`row-${i}`}>
                                                                <StructuredListCell
                                                                    onClick={this.selectImport.bind(
                                                                        this,
                                                                        i
                                                                    )}>
                                                                    {item.name}
                                                                </StructuredListCell>
                                                                <StructuredListCell
                                                                    onClick={this.selectImport.bind(
                                                                        this,
                                                                        i
                                                                    )}>
                                                                    {
                                                                        item.description
                                                                    }
                                                                </StructuredListCell>
                                                                <StructuredListCell>
                                                                    <br />
                                                                    <RadioButton
                                                                        checked={
                                                                            i ===
                                                                            this
                                                                                .state
                                                                                .controls
                                                                                .selected_domain
                                                                        }
                                                                        onClick={this.selectImport.bind(
                                                                            this,
                                                                            i
                                                                        )}
                                                                        id={`row-${i}`}
                                                                        title={`row-${i}`}
                                                                        value={`row-${i}`}
                                                                        name={
                                                                            item.name
                                                                        }
                                                                        labelText={``}
                                                                    />
                                                                </StructuredListCell>
                                                            </StructuredListRow>
                                                        )
                                                    )}
                                                </StructuredListBody>
                                            </StructuredListWrapper>
                                        </TabPanel>
                                    </TabPanels>
                                </Tabs>
                            </Modal>

                            {this.state.views.map((view, id) => {
                                if (this.state.active_view === view.name) {
                                    const Component =
                                        components[
                                            view.name.replace(/\s/g, '')
                                        ];

                                    if (view.disabled) {
                                        return (
                                            <div key={id}>
                                                <br />
                                                <br />
                                                <ToastNotification
                                                    lowContrast
                                                    hideCloseButton
                                                    key={id}
                                                    type="error"
                                                    subtitle={`The authors have disabled the ${view.name}. Please
                          check out the other viewing options for now.`}
                                                    title="DISABLED VIEW"
                                                />
                                            </div>
                                        );
                                    } else {
                                        return (
                                            <div key={id}>
                                                {this.state.notifications
                                                    .viz_loading && (
                                                    <div
                                                        style={{
                                                            marginTop: '30%',
                                                            marginLeft: '45%',
                                                        }}>
                                                        <Loading
                                                            description="Active loading indicator"
                                                            withOverlay={false}
                                                        />
                                                    </div>
                                                )}

                                                {!this.state.notifications
                                                    .viz_loading &&
                                                    this.state.graph && (
                                                        <>
                                                            <br />
                                                            <Toggle
                                                                aria-label="toggle commit mode"
                                                                id="toggle-selection-mode"
                                                                size="sm"
                                                                labelText=""
                                                                labelA="Select by EDGE"
                                                                labelB="Select by NAME"
                                                                toggled={
                                                                    this.state
                                                                        .controls
                                                                        .select_by_name
                                                                }
                                                                onClick={this.setSelectionMode.bind(
                                                                    this
                                                                )}
                                                            />

                                                            <Component
                                                                key={id}
                                                                onEdgeClick={this.onEdgeClick.bind(
                                                                    this
                                                                )}
                                                                commitChanges={this.commitChanges.bind(
                                                                    this
                                                                )}
                                                                state={
                                                                    this.state
                                                                }
                                                                update_planner_payload={this.update_planner_payload.bind(
                                                                    this
                                                                )}
                                                            />
                                                        </>
                                                    )}
                                            </div>
                                        );
                                    }
                                }

                                return null;
                            })}
                        </Column>
                    </Grid>
                </Column>
                <Column lg={4} md={2} sm={1}>
                    <FeedbackArea
                        state={this.state}
                        selectLandmarks={this.selectLandmarks.bind(this)}
                        deselectLandmarks={this.deselectLandmarks.bind(this)}
                        deleteUserPrompt={this.deleteUserPrompt.bind(this)}
                    />
                </Column>
            </Grid>
        );
    }
}

class FeedbackArea extends React.Component {
    constructor(props) {
        super(props);
        this.state = props.state;
    }

    componentDidUpdate(prevProps, prevState) {}

    static getDerivedStateFromProps(props, state) {
        return props.state;
    }

    selectLandmark(landmark) {
        this.props.selectLandmarks([landmark]);
    }

    deselectLandmark(landmark) {
        this.props.deselectLandmarks([landmark]);
    }

    deleteUserPrompt(prompt) {
        this.props.deleteUserPrompt(prompt);
    }

    getNumPlans(item) {
        const plan_hashes = getPlanHashesFromChoice(
            item,
            this.state.remaining_plans
        );
        return plan_hashes.length;
    }

    render() {
        return (
            <>
                <Tile style={{ fontSize: 'small', lineHeight: 'initial' }}>
                    {this.state.feedback}
                </Tile>

                <StructuredListWrapper ariaLabel="Choices">
                    {this.state.active_view !== 'NL2LTL Integration' &&
                        this.state.choice_infos.length > 0 && (
                            <>
                                <StructuredListHead>
                                    <StructuredListRow head>
                                        <StructuredListCell head>
                                            Choices
                                        </StructuredListCell>
                                    </StructuredListRow>
                                </StructuredListHead>
                                <StructuredListBody className="landmarks-list">
                                    {this.state.selected_landmarks.map(
                                        (item, i) => (
                                            <StructuredListRow key={item}>
                                                <StructuredListCell
                                                    className="text-blue landmark-list-item"
                                                    onClick={this.deselectLandmark.bind(
                                                        this,
                                                        item
                                                    )}>
                                                    {item}
                                                    <Tag
                                                        className="count-tag"
                                                        size="sm"
                                                        type="cool-gray"
                                                        title={this.getNumPlans(
                                                            item
                                                        ).toString()}>
                                                        {' '}
                                                        {this.getNumPlans(
                                                            item
                                                        )}{' '}
                                                    </Tag>
                                                </StructuredListCell>
                                            </StructuredListRow>
                                        )
                                    )}
                                </StructuredListBody>
                                <StructuredListBody className="landmarks-list">
                                    {this.state.unselected_landmarks.map(
                                        (item, i) => (
                                            <StructuredListRow key={item}>
                                                <StructuredListCell
                                                    className="text-silver landmark-list-item"
                                                    onClick={this.selectLandmark.bind(
                                                        this,
                                                        item
                                                    )}>
                                                    {item}
                                                    <Tag
                                                        className="count-tag"
                                                        size="sm"
                                                        type="cool-gray"
                                                        title={this.getNumPlans(
                                                            item
                                                        ).toString()}>
                                                        {' '}
                                                        {this.getNumPlans(
                                                            item
                                                        )}{' '}
                                                    </Tag>
                                                </StructuredListCell>
                                            </StructuredListRow>
                                        )
                                    )}
                                </StructuredListBody>
                                <Tile
                                    style={{
                                        fontSize: 'small',
                                        lineHeight: 'initial',
                                        backgroundColor: 'white',
                                        color: 'gray',
                                    }}>
                                    This list shows all available choices of
                                    interest, with ones currently selected by
                                    you in blue. Click to toggle selection.
                                </Tile>
                            </>
                        )}

                    {this.state.active_view === 'NL2LTL Integration' &&
                        this.state.cached_formulas.length > 0 && (
                            <>
                                <StructuredListHead>
                                    <StructuredListRow head>
                                        <StructuredListCell head>
                                            Constraints
                                        </StructuredListCell>
                                    </StructuredListRow>
                                </StructuredListHead>
                                <StructuredListBody className="landmarks-list">
                                    {this.state.cached_formulas.map(
                                        (item, i) => (
                                            <StructuredListRow key={item}>
                                                <StructuredListCell className="text-blue">
                                                    {item.user_prompt}
                                                </StructuredListCell>
                                            </StructuredListRow>
                                        )
                                    )}
                                </StructuredListBody>
                            </>
                        )}
                </StructuredListWrapper>
            </>
        );
    }
}

export { PlanArea, FeedbackArea };
