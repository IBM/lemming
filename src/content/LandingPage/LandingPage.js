import React from 'react';
import GitHubButton from 'react-github-btn';
import { isMobile } from 'react-device-detect';
import { Document, LogoGithub } from '@carbon/icons-react';
import { PlanArea, FeedbackArea } from '../../components/BasicElement';
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

class LandingPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = config;
  }

  render() {
    return (
      <>
        <Grid>
          <Column lg={4} md={4} sm={4}>
            <Grid>
              <Column lg={1} md={1} sm={1}>
                <img
                  alt="A Giant Lemming"
                  src={generateURL('shared', 'lemming', 'png')}
                  className="logo"
                  width="100%"
                />
              </Column>
              <Column lg={3} md={3} sm={3}>
                <h5>
                  <span className="text-blue">{this.state.metadata.name}</span>:{' '}
                  {this.state.metadata.title_text}
                </h5>
              </Column>
            </Grid>

            <br />
            <p style={{ fontSize: 'small' }}>{this.state.metadata.info_text}</p>

            <br />
            <ButtonSet stacked>
              <Button
                kind="tertiary"
                className="buttonset"
                size="sm"
                renderIcon={Document}
                href={generateURL(
                  'shared',
                  this.state.metadata.primary_link,
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
                href={this.state.metadata.link_to_code}
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
                            e.currentTarget.offsetHeight > e.pageY / 4
                              ? 0
                              : e.pageY / 2,
                          behavior: 'smooth',
                        });
                      }}>
                      <StructuredListWrapper ariaLabel="Structured list">
                        <StructuredListBody>
                          {this.state.metadata.secondary_links.map(
                            (item, i) => (
                              <StructuredListRow key={i}>
                                <StructuredListCell>
                                  <Button
                                    target="_blank"
                                    size="sm"
                                    href={item.link}
                                    kind="ghost"
                                    hasIconOnly
                                    iconDescription={item.name}
                                    renderIcon={Document}></Button>
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
              {this.state.metadata.citation_text}
            </CodeSnippet>

            {!isMobile && (
              <Grid>
                <Column className="footer" lg={16} md={8} sm={4}>
                  <p
                    style={{
                      fontSize: 'small',
                      marginBottom: '10px',
                    }}>
                    Follow us on GitHub. Your love <br /> keeps us going!{' '}
                    <span role="img" aria-label="hugging face">
                      &#129303;
                    </span>
                  </p>

                  <GitHubButton
                    href={this.state.metadata.link_to_code}
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
                    <Link href="https://research.ibm.com" target="_blank">
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
                  <span>This application only runs on a widescreen.</span>
                }
                title="Please switch to widescreen."
              />
            ) : (
              <Grid>
                <Column lg={10} md={8} sm={4}>
                  <PlanArea props={this.state} />
                </Column>
                <Column lg={2} md={4} sm={4}>
                  <FeedbackArea />
                </Column>
              </Grid>
            )}
          </Column>
        </Grid>
      </>
    );
  }
}

export default LandingPage;
