import React from 'react';
import GitHubButton from 'react-github-btn';
import { isMobile } from 'react-device-detect';
import { Document, LogoGithub } from '@carbon/icons-react';
import { PlanArea } from '../../components/BasicElement';
import { generateURL } from '../../components/Info';
import {
    Button,
    ButtonSet,
    CodeSnippet,
    Link,
    ToastNotification,
    Accordion,
    AccordionItem,
    Grid,
    Column,
    StructuredListWrapper,
    StructuredListBody,
    StructuredListRow,
    StructuredListCell,
} from '@carbon/react';

const config = require('../../config.json');
const LandingPage = props => (
    <>
        <Grid>
            <Column lg={4} md={4} sm={4}>
                <img
                    alt="A Giant Lemming"
                    src={generateURL('shared', 'lemming', 'png')}
                    className="logo"
                    width="25%"
                />

                <br />
                <br />
                <h4>
                    <span className="text-blue">{config.metadata.name}</span>
                </h4>
                <h3>{config.metadata.title_text}</h3>

                <br />
                <p style={{ fontSize: 'small' }}>{config.metadata.info_text}</p>

                <br />
                <ButtonSet stacked>
                    <Button
                        kind="tertiary"
                        className="buttonset"
                        size="sm"
                        renderIcon={Document}
                        href={generateURL(
                            'shared',
                            config.metadata.primary_link,
                            'pdf'
                        )}
                        target="_blank">
                        Read
                    </Button>
                    <br />
                    <Button
                        kind="tertiary"
                        className="buttonset tertiary-secondary"
                        renderIcon={LogoGithub}
                        size="sm"
                        href={config.metadata.link_to_code}
                        target="_blank">
                        Contribute
                    </Button>
                    <br />

                    <Grid>
                        <Column lg={4} md={4} sm={4}>
                            <Accordion align="start">
                                <AccordionItem
                                    className="see-also-accordion"
                                    title="See also"
                                    onClick={e => {
                                        window.scrollTo({
                                            top:
                                                e.currentTarget.offsetHeight >
                                                e.pageY / 4
                                                    ? 0
                                                    : e.pageY / 2,
                                            behavior: 'smooth',
                                        });
                                    }}>
                                    <StructuredListWrapper ariaLabel="Structured list">
                                        <StructuredListBody>
                                            {config.metadata.secondary_links.map(
                                                (item, i) => (
                                                    <StructuredListRow key={i}>
                                                        <StructuredListCell>
                                                            <Button
                                                                target="_blank"
                                                                size="sm"
                                                                href={item.link}
                                                                kind="ghost"
                                                                hasIconOnly
                                                                iconDescription={
                                                                    item.name
                                                                }
                                                                renderIcon={
                                                                    Document
                                                                }></Button>
                                                        </StructuredListCell>
                                                        <StructuredListCell>
                                                            {item.name}{' '}
                                                            <span className="text-secondary">
                                                                {' '}
                                                                | {item.venue}
                                                            </span>
                                                        </StructuredListCell>
                                                    </StructuredListRow>
                                                )
                                            )}
                                        </StructuredListBody>
                                    </StructuredListWrapper>
                                </AccordionItem>
                            </Accordion>
                        </Column>
                    </Grid>
                </ButtonSet>
                <br />
                <CodeSnippet type="multi">
                    {config.metadata.citation_text}
                </CodeSnippet>

                {!isMobile && (
                    <Grid>
                        <Column className="footer" lg={16} md={8} sm={4}>
                            <p
                                style={{
                                    fontSize: 'small',
                                    marginBottom: '10px',
                                }}>
                                Follow us on GitHub. Your love <br /> keeps us
                                going!{' '}
                                <span role="img" aria-label="hugging face">
                                    &#129303;
                                </span>
                            </p>

                            <GitHubButton
                                href={config.metadata.link_to_code}
                                data-size="small"
                                data-show-count="true"
                                aria-label="Star repository on GitHub">
                                Star
                            </GitHubButton>

                            <div
                                style={{
                                    marginTop: '20px',
                                    marginBottom: '10px',
                                }}>
                                App built by{' '}
                                <Link
                                    href="https://research.ibm.com"
                                    target="_blank">
                                    IBM Research
                                </Link>
                            </div>
                        </Column>
                    </Grid>
                )}
            </Column>
            <Column lg={12} md={8} sm={4}>
                {isMobile ? (
                    <ToastNotification
                        lowContrast
                        hideCloseButton
                        type="error"
                        subtitle={
                            <span>
                                This application only runs on a widescreen.
                            </span>
                        }
                        title="Please switch to widescreen."
                    />
                ) : (
                    <Grid>
                        <Column lg={16} md={8} sm={4}>
                            <PlanArea />
                        </Column>
                    </Grid>
                )}
            </Column>
        </Grid>
    </>
);

export default LandingPage;
